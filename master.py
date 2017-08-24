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
        self.load_path = 'D:\Pixiv_mark'

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
    def get_pic_info(self,url,flag):
        if flag :
            return 0
        else:





    def work(self):
        self.login(self)
        Mark_Total = self.get_total(self)
        Mark_page_num = int(Mark_Total)/20
        #求出收藏页数

        for page_num in Mark_page_num:
            Elements = self.get_html(self,self.mark_url)
            for Pic_url,flag  in Elements.items():
                Pic_info = self.get_pic_info(Pic_url,flag)



def main():
    pixiv = Pixiv()
    pixiv.pixiv_id=input('输入pixiv 账号：')
    pixiv.password=input('输入密码：')
    pixiv.work()


if __name__ == '__main__':
    main()