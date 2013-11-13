# -*- encoding: utf-8 -*-

# 用于抓取页面
import sys
import time

import urllib2
import cookielib
import urllib

import config
import login_state
import page_parser
import custom_exception

class PageCrawler:

    def __init__(self, u='', p=''):
        self.__username = u
        self.__password = p
        self.__state = None

    def login(self):
        '''Log in the seu-library to get the cookie info.

        Args type will not be checked and not matter what type the args are, they will
        be converted into string without ensure correct. Correct username and password of
        string type are expected.

         Args:
            username: the login username, usually the original student number, it is expected
            with string type, eg: '07010115'
            password: the login password, it is also expected with string type.

        Returns:
            if login successfully, it will return a opener builded by urllib2.build_opener() and contains the cookie info
            if login success

        Raises:
            urllib2.HTTPError:
            urllib2.URLError:
        '''

        verify_url = config.LOGIN_URL
        # store the cookie
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        # with the network tab in chrome developtool can find these get params
        data = {'number' : self.__username,
                'passwd' : self.__password,
                'select' : 'cert_no',
                'returnUrl' : ''}

        req = urllib2.Request(verify_url, urllib.urlencode(data))
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        res = urllib2.urlopen(req, timeout = config.TIME_OUT)
        if res.getcode() == 200 and not page_parser.is_login_page(res.read()):  # it seems that response-code == 200 is not necessary
            state = login_state.LoginState(True, opener)
        else:
            state = login_state.LoginState(False, None)
        self.__state = state
        return state

    def get_search_result_page(self,strText,page=1, strSearchType='title', doctype='ALL', match_flag='forward', \
                               displaypg='20', sort='desc', orderby='CATA_DATE', showmode='list', dept='ALL'):
        '''Search book result page.

        Args:
            strSearchType搜索类型:
                title(题名), author(责任者), keyword(主题词), isbn(ISBN/ISSN), asordno(订购号), coden(分类号),
                callno(索书号), publisher(出版社) ,series(丛书名), tpinyin(题名拼音), apinyin(责任者拼音)
            doctype文档类型: (String)
                All(所有), 01(中文图书), 02(西文图书), 11(中文期刊), 12(西文期刊)
            match_flag检索模式:
                forward(前方一致), full(完全匹配), any(任意匹配)
            displaypg(每页显示个数):
                20, 30, 50, 100
            sort(结果排序):
                CATA_DATE(入藏日期), M_TITLE(题名), M_AUTHOR(责任者), M_CALL_NO(索书号), M_PUBLISHER(出版社),
                M_PUB_YEAR(出版日期)
            orderby:
                asc(升序), desc(降序)
            showmode结果显示:
                list(详细显示), table(表格显示)
            dept(选择校区):
                ALL(所有校区), 00(总馆), 01(九龙湖), 02(四牌楼), 03(丁家桥)

        Returns:
            If request successfully, return the html, else return None.

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
        '''
        ori_url = "http://www.lib.seu.edu.cn:8080/opac/openlink.php?"
        params = {"strSearchType":strSearchType,  'strText':strText.encode('utf-8'), 'page':str(page),
                  'doctype':doctype, 'match_flag':match_flag, 'displaypg':displaypg,
                  'sort':sort, 'orderby':orderby, 'showmode':showmode, 'dept':dept}
        params_str = urllib.urlencode(params)
        search_url = ori_url + params_str
        req = urllib2.Request(search_url)
        res = urllib2.urlopen(req, timeout=config.TIME_OUT)
        return res.read()
