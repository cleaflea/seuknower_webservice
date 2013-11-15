# -*- encoding:utf-8 -*-

import page_crawler
import page_parser

class LibraryService:
    def __init__(self, username='', password=''):
        self.crawler = page_crawler.PageCrawler(username, password)

    def check_account(self):
        state = self.crawler.login()
        return state.get_status()

    # 同过chrome开发者工具中的network选项就可以看到提交的那些参数
    # 查看搜索到的图书列表
    def get_search_result_list(self,strText,page=1, strSearchType='title', doctype='ALL', match_flag='forward', \
                               displaypg='20', sort='desc', orderby='CATA_DATE', showmode='list', dept='ALL'):

        html = self.crawler.get_search_result_page(strText,page, strSearchType, doctype, match_flag, \
                            displaypg, sort, orderby, showmode, dept)
        books = page_parser.get_search_book_list(html)
        book_list = []
        for book in books:
            book_list.append(book.to_json_obj())
        return book_list
    # 查看特定书籍的信息，主要是还是否有可借的
    def get_book_detail(self, marc_no):
        html = self.crawler.get_search_detail_page(marc_no)
        book = page_parser.get_search_book_detail(html)
        return book.to_json_obj()
    # 查看已借图书
    def get_render_book_list(self):
        html = self.crawler.get_rendered_book_page()
        books = page_parser.get_render_book_list(html)
        # print book_list
        book_list = []
        for book in books:
            book_list.append(book.to_json_obj())
        return book_list
    # 续借图书
    def renew_book(self, barcode):
        html = self.crawler.renew_book(barcode)
        if page_parser.is_renew_success(html):
            return True
        else:
            return False
    # 查看自己已经预约的书籍
    def get_appointed_books(self):
        html = self.crawler.get_appointed_books_page()
        book_list = page_parser.get_appointed_books(html)
        books = [b.to_json_obj() for b in book_list]
        return books

    # 取消一本已经预约书籍的预约
    def cancel_appoint(self, call_no, marc_no, loca):
        html = self.crawler.cancel_appoint(call_no, marc_no, loca)
        if page_parser.is_cancel_appoint_success(html):
            return True
        else:
            return False

    # 获取一本书的预约信息
    def get_appoint_book_info(self, marc_no):
        html = self.crawler.get_appoint_info_page(marc_no)
        books = page_parser.get_appoint_list(html)
        book_list = [b.to_json_obj() for b in books]
        print book_list
        return book_list

    # 预约一本书
    def appoint_book(self, call_no, location, check, take_loca='90001', preg_days='30', pregKeepDay='7'):
        html = self.crawler.appoint_book(call_no, location, check, preg_days, take_loca, pregKeepDay)
        if page_parser.is_appoint_success(html):
            return True
        else:
            return False
