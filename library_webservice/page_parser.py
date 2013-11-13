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
                decode_strange_str(book_divs[0].h3.a.string[2:]).encode('utf-8').strip(),
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
