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
    def get_search_result_list(self,strText,page=1, strSearchType='title', doctype='ALL', match_flag='forward', \
                               displaypg='20', sort='desc', orderby='CATA_DATE', showmode='list', dept='ALL'):

        html = self.crawler.get_search_result_page(strText,page, strSearchType, doctype, match_flag, \
                            displaypg, sort, orderby, showmode, dept)
        books = page_parser.get_search_book_list(html)
        book_list = []
        for book in books:
            book_list.append(book.to_json_obj())
        return book_list