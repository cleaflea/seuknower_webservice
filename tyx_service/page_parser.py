# -*- encoding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import json
import datetime

import page_crawler
import custom_exception


class LoginState:
    def __init__(self, status, opener):
        self.__status = status
        self.__opener = opener

    def get_login_status(self):
        return self.__status

    def get_opener(self):
        return self.__opener

# 查看网页源代码加上审查元素就明白了
def get_paocao_number(html):
    '''
    Raises:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup(html)
        table = soup.findAll("td", {"class": "Content_Form"})
        pc = table[7].text
        return pc
    except:
        raise custom_exception.ParseException("跑操次数页面")