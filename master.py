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

    def work(self):



def main():
    pixiv = Pixiv()
    pixiv.pixiv_id=input('输入pixiv 账号：')
    pixiv.password=input('输入密码：')
    pixiv.work()



if __name__ == '__main__':
    main()