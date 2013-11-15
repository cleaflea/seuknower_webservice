# -*- coding: utf-8 -*-

# 用于解析页面

import re

import BeautifulSoup

import book
import custom_exception

class PageParser:
     def isHonePage(self, html):
        pass

def is_login_page(html):
    '''Judge the page is library-login page or not.

    Because if the user login failed, the site will redirect to this page, so the method can
    also judge if the user login successfully.

    Since there is only one login-page, just judge it using the caption "登录我的图书馆".

    Args:
        html: The page html string.

    Returns:
        True or False.

    Raises:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        result = soup.findAll('caption')
        for cap in result:
            if "<caption>登录我的图书馆</caption>" == str(cap):
                # print "it is login page"
                return True
        # print "it is not login page"
        return False
    except Exception,e:
        raise custom_exception.ParseException("login page")

# 路遇&#x，研究一下发现就是Unicode不同之处在于%u换成了&#x，还有就是后面多了个分号
def decode_strange_str(s):
    s = s.replace('&#x','\u').replace(';','').replace('&nbsp','')
    u = s.decode('unicode-escape')
    return u

# 就是取标签中的内容，看代码是取多层嵌套标签下的文本内容，但是暂时含没有发现一定要用这个方法的地方
def extract_string(node):
    '''Extract all strings under one Tag.

    It is properly to use this function to extract strings under one node only when the strings are
    split from a entirety in meaning.

    Args:
        node: BeautifulSoup node.
    Returns:
        All the split strings will be combined into a entirety of unicode type.
    '''
    u = u''
    if type(node) == BeautifulSoup.Tag:
        for i in node.contents:
            u += extract_string(i)
    else:
        u += node.string
    return u

# 只要把不用remove处理过的打印出来看就行了，可以发现这些contents里有几个u'\n'，是要去除的
def __remove_navi_string(tag_list):
    '''Remove NavigableString in tag.contents especially u'\n'.

    Args:
        tag_list: the list of tags and nav_string gotten from tag.contents.
    '''

    tag_type = BeautifulSoup.Tag
    for tag in tag_list:
        if type(tag) is not tag_type:
            tag_list.remove(tag)
    return tag_list

def get_search_book_list(html):
    '''Extract info from search result page.

    Args:
        html: the page resource string.

    Returns:
        If extract successfully, return the list of BookSearchItem obj, else return None.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_divs = soup.findAll('div',{'class':'list_books', 'id':'list_books'})
        book_list = []
        for book_div in book_divs:
            # print book_div
            book_item = book.BookSearchItem(
                book_div.h3.a['href'].encode('utf-8').strip()[17:],
                decode_strange_str(book_div.h3.a.string[2:]).encode('utf-8').strip(),
                # decode_strange_str(book_divs[0].h3.a.string[2:]).encode('utf-8').strip(),
                book_div.find('span',{'class':'doc_type_class'}).string.encode('utf-8').strip(),
                decode_strange_str(book_div.h3.contents[2].string).encode('utf-8').strip(),
                decode_strange_str(book_div.p.contents[2].string).encode('utf-8').strip(),
                decode_strange_str(book_div.p.contents[4].string).encode('utf-8').strip(),
                book_div.p.span.contents[1].string.encode('utf-8').strip(),
                book_div.p.span.contents[5].string.encode('utf-8').strip()
            )
            book_list.append(book_item)
            print book_item
        return book_list
    except Exception,e:
        raise custom_exception.ParseException("search-result page")

def get_search_book_detail(html):
    '''Extract info from book detail page.

    Args:
        html: the page resource string.

    Returns:
        If extract successfully, return the list of BookSearchDetail obj, else return None.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_intro = soup.findAll('dl', {'class':'booklist'})
        # print len(book_intro)
        detail = book.BookSearchDetail()
        for i in range(len(book_intro)-1):
            intro_item = book_intro[i]
            detail.add_info(extract_string(intro_item.dt), decode_strange_str(extract_string(intro_item.dd)))

        store_table = soup.find('table', {'width':"670", 'border':"0", 'align':"center",
                                              'cellpadding':"2", 'cellspacing':"1",
                                              'bgcolor':"#d2d2d2"})
        store_items = store_table.findAll('tr')[1:]
        for store_item in store_items:
            items = store_item.findAll('td')

            # print type(items[0].string.encode('utf-8'))
            search_num = items[0].string.encode('utf-8').strip()
            barcode = items[1].string.encode('utf-8').strip()
            years = items[2].string.encode('utf-8').strip()
            campus = items[3].string.encode('utf-8').strip()
            room = items[4].string.encode('utf-8').strip()
            lend = extract_string(items[5]).encode('utf-8').strip()
            try:
                store = book.BookStore(search_num, barcode, years, campus, room, lend)
                detail.add_store(store)
            except Exception, e:
                print e

        # print store_items
        # print detail
        return detail
    except:
        raise custom_exception.ParseException("book-detail page")

def get_render_book_list(html):
    '''Extract book info from the rendered book page.

    Args:
        html: The page-string of render book.

    Returns:
        If extract successfully, it will return the list of 'book.BookIntro' object, else return None.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_table = soup.findAll('table',{ 'width' : "100%", 'border' : "0", 'cellpadding' : "5",
                                            'cellspacing' : "1", 'bgcolor' : "#CCCCCC"})
        if not book_table:
            return []

        def __get_book_tags(tag_list):
            __remove_navi_string(tag_list)
            tag_list.remove(tag_list[0])
            return tag_list
        book_tags = book_table[0].contents
        __get_book_tags(book_tags)
        book_list = []
        for book_tag in book_tags:
            book_info_tags = book_tag.contents
            __remove_navi_string(book_info_tags)
            book_intro = book.BookRenderItem(book_info_tags[0].string.strip().encode('utf-8'),
                                        decode_strange_str(book_info_tags[1].a.string).strip().encode('utf-8'),
                                        decode_strange_str(book_info_tags[1].contents[1].string).strip().encode('utf-8')[1:].strip(),
                                        book_info_tags[2].string.strip().encode('utf-8'),
                                        book_info_tags[3].font.string.strip().encode('utf-8'),
                                        book_info_tags[4].string.strip().encode('utf-8'),
                                        book_info_tags[5].string.strip().encode('utf-8'),
                                        book_info_tags[6].string.strip().encode('utf-8')
                                        )
            print book_intro
            book_list.append(book_intro)
        return book_list
    except:
        raise custom_exception.ParseException("render-book page")

def is_renew_success(html):
    '''Judge if the page is the renew-success returns.

    Args:
        Renew operation's return html.

    Returns:
        True if yes, or False.

    Raise:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        all_string = extract_string(soup.font)
        # import config
        # config.logger.error(type(all_string))
        # config.logger.error(all_string)
        # index = all_string.encode('utf-8').find("不得续借")
        index = all_string.find(u'不得续借')
        if index == -1:
            return True
        else:
            return False
    except Exception,e:
        # config.logger.error(e)
        # raise custom_exception.ParseException('renew result page')
        raise
    # print refuse

def get_appointed_books(html):
    '''

    Returns:
        list of book.AppointedBookItem or [].

    Raises:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_table = soup.find('table', {'width':"100%", 'border':"0", 'cellpadding':"5",
                               'cellspacing':"1", 'bgcolor':"#CCCCCC"})
        # print book_table
        if not book_table:
            return []
        book_trs = book_table.findAll('tr')
        book_trs.remove(book_trs[0])
        # print book_trs
        book_list = []
        for b in book_trs:
            book_tds = b.findAll('td')
            book_item = book.AppointedBookItem(
                extract_string(book_tds[0]).encode('utf-8').strip(),
                decode_strange_str(extract_string(book_tds[1])).encode('utf-8').strip(),
                decode_strange_str(extract_string(book_tds[2])).encode('utf-8').strip(),
                extract_string(book_tds[3]).encode('utf-8').strip(),
                extract_string(book_tds[4]).encode('utf-8').strip(),
                extract_string(book_tds[5]).encode('utf-8').strip(),
                extract_string(book_tds[6]).encode('utf-8').strip(),
                extract_string(book_tds[7]).encode('utf-8').strip()
            )
            # print extract_string(book_tds[7]).encode('utf-8').strip()
            contain_data = book_tds[8].div.input['onclick']
            # pattern = re.compile(r"\((\'.*\'?)\,(\'.*\'?)\,(\'.*\'?)\,(\'.*\'?)\)")
            # 最后一部分最后没有逗号，且都是非贪婪匹配
            pattern = re.compile(r"\((\'.*\'?\,){3}(\'.*\'?)\)")
            match = pattern.search(contain_data)
            # 执行字符串中的python代码，此处是执行以后输出了python对象，是一个元组对象，原本只是普通的python字符串
            data_list = eval(match.group())
            data = {"marc_no":data_list[0], "call_no":data_list[1], "loca":data_list[3]}
            book_item.set_data(data)
            print book_item
            book_list.append(book_item)
        return book_list
    except Exception,e:
        raise custom_exception.ParseException("appointed-book page")

def is_cancel_appoint_success(html):
    # python中简单的在字符串中学找子字符串
    if html.find("已取消") != -1:
        return True
    else:
        return False

def is_appoint_success(html):
    '''Judge if the page is the return of appoint successfully.
    '''
    # python中简单的在字符串中学找子字符串
    if html.find("预约成功") != -1:
        return True
    else:
        return False

def get_appoint_list(html):
    '''Get appoint books.

    Args: appoint-books page html.

    Returns:
        Appoint books list.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        renew_table = soup.find('table', {'width':"98%", 'border':"0", 'align':"center",
                                          'cellpadding':"2", 'cellspacing':"1",
                                          'bgcolor':"#CCCCCC", 'class':"table-line"})
        items = renew_table.findAll('tr')
        #print items
        appoint_item_list = []
        # 会根据馆藏地又多个而有多个<tr></tr>
        for i in range(1, len(items)-1):
            item = items[i]
            td_items = item.findAll('td')
            print item
            print '-----------------'

            print 'cleantha'

            places = []
            # 馆藏地编号和校区编号由图书馆代码得来，take_loca:
            # 90001-九龙湖总借还处, 00916-丁家桥中文借书处, 00940-四牌楼总借还处
            # 就是从这几个option中得到的，直接明文写在html页面中了
            tmp = td_items[6].findAll('option')
            for tag in tmp:
                places.append(tag['value'].encode('utf-8').strip())
            appoint_item = book.AppointInfoItem(
                td_items[0].string.encode('utf-8').strip(),
                td_items[1].string.encode('utf-8').strip(),
                td_items[7].findAll('input')[1]['value'].encode('utf-8').strip(),
                td_items[2].string.encode('utf-8').strip(),
                td_items[3].string.encode('utf-8').strip(),
                td_items[4].string.encode('utf-8').strip(),
                extract_string(td_items[5]).encode('utf-8').strip(),
                places,
                # td_items[7].findAll('input')[3]['disabled'].encode('utf-8').strip()
                # 如果可以预约的话那么radio那里是没有disabled这个属性的，
                # 如果不这样处理则会由于找不到disabled这个属性而抛出异常引发servererror 哈哈有一个bug
                (lambda x : 1 if x==3 else 0)(len(td_items[7].findAll('input')[3].attrs))
            )
            print appoint_item
            appoint_item_list.append(appoint_item)
        return appoint_item_list
    except:
        raise custom_exception.ParseException("appoint-books page")

def get_appoint_list(html):
    '''Get appoint books.

    Args: appoint-books page html.

    Returns:
        Appoint books list.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        renew_table = soup.find('table', {'width':"98%", 'border':"0", 'align':"center",
                                          'cellpadding':"2", 'cellspacing':"1",
                                          'bgcolor':"#CCCCCC", 'class':"table-line"})
        items = renew_table.findAll('tr')
        #print items
        appoint_item_list = []
        # 会根据馆藏地又多个而有多个<tr></tr>
        for i in range(1, len(items)-1):
            item = items[i]
            td_items = item.findAll('td')
            print item
            print '-----------------'
            places = []
            # 馆藏地编号和校区编号由图书馆代码得来，take_loca:
            # 90001-九龙湖总借还处, 00916-丁家桥中文借书处, 00940-四牌楼总借还处
            # 就是从这几个option中得到的，直接明文写在html页面中了
            tmp = td_items[6].findAll('option')
            for tag in tmp:
                places.append(tag['value'].encode('utf-8').strip())
            appoint_item = book.AppointInfoItem(
                td_items[0].string.encode('utf-8').strip(),
                td_items[1].string.encode('utf-8').strip(),
                td_items[7].findAll('input')[1]['value'].encode('utf-8').strip(),
                td_items[2].string.encode('utf-8').strip(),
                td_items[3].string.encode('utf-8').strip(),
                td_items[4].string.encode('utf-8').strip(),
                extract_string(td_items[5]).encode('utf-8').strip(),
                places,
                # td_items[7].findAll('input')[3]['disabled'].encode('utf-8').strip()
                # 如果可以预约的话那么radio那里是没有disabled这个属性的，
                # 如果不这样处理则会由于找不到disabled这个属性而抛出异常引发servererror 哈哈有一个bug
                (lambda x : 1 if x==3 else 0)(len(td_items[7].findAll('input')[3].attrs))
            )
            print appoint_item
            appoint_item_list.append(appoint_item)
        return appoint_item_list
    except:
        raise custom_exception.ParseException("appoint-books page")

def is_appoint_success(html):
    '''Judge if the page is the return of appoint successfully.
    '''
    if html.find("预约成功") != -1:
        return True
    else:
        return False