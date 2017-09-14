# -*- coding:utf-8 -*-
import datetime
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

se = requests.session()


class Pixiv():
    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.rank_url = 'https://www.pixiv.net/ranking.php?mode=daily'
        self.main_url = 'https://pixiv.net/'
        self.headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.pixiv_id = ''
        self.password = ''
        self.post_key = []
        self.return_to = 'https://www.pixiv.net'
        self.load_path = 'D:\Pixiv_rank'
        self.ip_list = ['']

    def login(self):
        post_key_html = se.get(self.base_url, headers=self.headers).text
        # print post_key_html
        # 获取登录页面
        post_key_soup = BeautifulSoup(post_key_html, 'lxml')
        self.post_key = post_key_soup.find('input')['value']
        # 捕获postkey
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        }
        se.post(self.login_url, data=data, headers=self.headers)

    def get_html(self, url, timeout, proxy=None, num_entries=5):
        if proxy is None:
            try:
                return se.get(url, headers=self.headers, timeout=timeout)
            except:
                if num_entries > 0:
                    print u'网页出错，5秒后重新获取，剩余获取次数' + str(num_entries) + '次'
                    time.sleep(5)
                    return self.get_html(url, timeout, num_entries=num_entries - 1)
                else:
                    print u'开始使用代理'
                    time.sleep(5)
                    ip = ''.join(str(random.choice(self.ip_list))).strip()
                    now_proxy = {'http': ip}
                    return self.get_html(url, timeout, proxy=now_proxy)
        else:
            try:
                return se.get(url, headers=self.headers, proxies=proxy, timeout=timeout)
            except:
                if num_entries > 0:
                    print u'正在更换代理，5秒后重新获取第' + str(num_entries) + '次'
                    time.sleep(5)
                    ip = ''.join(str(random.choice(self.ip_list))).strip()
                    now_proxy = {'http': ip}
                    return self.get_html(url, timeout, proxy=now_proxy, num_entries=num_entries - 1)
                else:
                    print u'使用代理失败'
                    return self.get_html(url, timeout)

    def get_img(self, html, date):
        section_soup = BeautifulSoup(html, 'lxml')
        section_list = section_soup.find_all('div', attrs={'class': 'ranking-image-item'})
        # 获取榜单中的section的列表
        print 'succeed'
        i = 1
        print section_list.__len__()
        for num in section_list:
            print num
            # num_html=BeautifulSoup(num,'lxml')
            # img_item=num.find('div',attrs={'class':'ranking-image-item'})
            # print img_item
            href = num.find('a')['href']
            img_id = num.find('img')['data-id']
            print href
            # 提取href中的图片地址
            jump_to_url = self.main_url + href
            jump_to_html = self.get_html(jump_to_url, 3).text
            img_soup = BeautifulSoup(jump_to_html, 'lxml')
            # 获取图片主页面
            img_info = img_soup.find('div', attrs={'id': 'wrapper'}).find('div', attrs={'class': 'wrapper'})
            # 获取图片信息
            print img_info
            if img_soup is None:
                continue
            self.download_img(img_info, jump_to_url, date, i, img_id)
            i = i + 1

    def download_img(self, img_info, href, date, no, id):
        try:
            title = img_info.find('img')['alt']
            print title

            title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_') \
                .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
            title = '#' + str(no) + ' ' + title + ' id-' + id
            # 去掉那些不能在文件名里面的.记得加上strip()去掉换行
            if os.path.exists(os.path.join(self.load_path, str(date), title + '.jpg')):
                print u'该图已存在 2333'
                return False
            src = img_info.find('img')['data-src']
            src_headers = self.headers
            src_headers['Referer'] = href
        except:
            print u'图片地址获取失败'
            return False

        try:
            html = requests.get(src, headers=src_headers)
            img = html.content
        except:
            print u'图片获取失败'
            return False

        print u'正在保存名字为: ' + title + ' 的图片'

        with open(title + '.jpg', 'ab') as f:  # 图片要用b
            f.write(img)
        print u'保存该图片完毕'

    def mkdir(self, path):
        path = path.strip()
        is_exist = os.path.exists(os.path.join(self.load_path, path))
        if not is_exist:
            print u'创建一个名字为 ' + path + ' 的文件夹'
            os.makedirs(os.path.join(self.load_path, path))
            os.chdir(os.path.join(self.load_path, path))
            return False
        else:
            print u'名字为 ' + path + ' 的文件夹已经存在'
            os.chdir(os.path.join(self.load_path, path))
            return False

    def work(self):
        t = datetime.datetime.now()
        time = str(t.year) + '_' + str(t.month) + '_' + str(t.day)

        self.login()
        self.mkdir(time)
        now_html = self.get_html(self.rank_url, 3)

        self.get_img(now_html.text, time)
        print time + u'文件夹已保存完毕'


pixiv = Pixiv()

pixiv.work()
