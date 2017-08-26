# *-* coding :utf-8 -*-
# by melon_rind_cat
#

import requests
from bs4 import BeautifulSoup
import os
import re
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

se = requests.session()

class Pixiv():
    def __int__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.mark_url = 'https://www.pixiv.net/bookmark.php?rest=show&p='
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
        self.path = 'D:\Pixiv_mark'

    #登录模块
    def login(self):
        post_key_html = se.get(self.base_url,headers=self.headers).text
        # 获取登录界面
        post_key_soup = BeautifulSoup(post_key_html,'lxml')
        self.post_key = post_key_soup.find('input')['value']
        #捕获postkey
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        }
        se.post(self.login_url,data=data,headers=self.headers)

    #获取url的页面
    def get_html(self,url):
        return se.get(url=url,header=self.header)


    #获取收藏页中的图片信息,返回图片链接和是否为多图
    def get_mark_items(self,html):
        section_soup = BeautifulSoup(html,'lxml')
        section_list = section_soup.find_all('li',attrs={'class':'image-item'})
        #获取当前收藏页中所有图片信息
        Elements = {}
        for items in section_list:
            Pic_url = self.main_url + items.find('a')['href']
            if 'multiple' in items.find('a')['class']:
                Elements[Pic_url] = 1
            else:
                Elements[Pic_url] = 0
        return Elements
        #返回一个元素

    #获取收藏图片数量
    def get_total(self):
        Mark_HtmlSource = self.get_html(self.mark_url).text
        #获取收藏页面的源代码
        Pattern = re.compile('<span class="count-badge">(.*?)件</span>',re.S)
        #comlile的正则匹配，re.S为完全匹配，返回一个对象模式
        Total = re.search(pattern = Pattern,string = Mark_HtmlSource).group(1)
        #search调用compile的规则查找，group(1)为匹配到的第一个字符
        print u'一共有' + str(Total) + u'件收藏'
        return Total

    #获取图片主页的信息
    def get_Img_info(self,url,flag):
        if flag :
            return 0
        else:
            Img_html = self.get_html()
            Img_soup = BeautifulSoup(Img_html,'lxml')
            Pattern = re.compile('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=(.*?)',re.S)
            Img_id = re.search(pattern=Pattern, string=url).group(1)

            Img_info = Img_soup.find('div',attrs={'id':'wrapper'}).find('div',attrs={'class':'wrapper'})
            flag = self.download_Img(Img_info,url,Img_id)
            if not flag:
                print u'该图片已存在'
                return 2
            else:
                return 1


    def download_Img(self,Img_info,Img_id,href):
        try:
            title = Img_info.find('img')['alt']
            print title
            src = Img_info.find('img')['data-src']
            src_headers = self.headers
            src_headers['Referer'] = href
        except:
            print u'图片地址获取失败'
            return False
        try:
            html = requests.get(src,header=src_headers)
            Img_data = html.content
        except:
            print u'图片获取失败'
            return False
        title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_') \
            .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
        title = title + str(Img_id) +'.jpg'
        is_exists = os.path.exists(path=self.path + '/' + title)
        if not is_exists :
            with open(title,'ab') as f:
                f.write(Img_data)
            print u'图片保存成功'
            return 1
        if is_exists:
            return 0
        


    def mkdir(self):
        self.path = self.path.strip()
        is_exist = os.path.exists(path=self.path)
        if not is_exist:
            print u'创建一个名字为 ' + path + ' 的文件夹'
            os.makedirs(self.path)
            os.chdir(self.path)
            return False
        else:
            print u'名字为 ' + path + ' 的文件夹已经存在'
            os.chdir(self.path)
            return False


    def work(self):
        self.login(self)
        Mark_Total = self.get_total(self)
        Mark_page_num = int(Mark_Total)/20
        #求出收藏页数
        self.mkdir(self.path)

        for page_num in Mark_page_num:
            Elements = self.get_html(self,self.mark_url)
            for Img_url,flag  in Elements.items():
                flag = self.get_Img_info(Img_url,flag)
                if flag == 2:
                    break
                    break



def main():
    pixiv = Pixiv()
    pixiv.pixiv_id=input('输入pixiv 账号：')
    pixiv.password=input('输入密码：')
    pixiv.work()


if __name__ == '__main__':
    main()