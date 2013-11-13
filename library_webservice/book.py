# -*- encoding: utf-8 -*-

class BookSearchItem:
    # 编号，书名，图书类型(中文，外文)，索书号(TN,TP什么的)，作者，出版社，馆藏副本，可借副本
    def __init__(self,marc_no, title, doctype, isbn, author, publisher, store_num, lendable_num):
        self.__marc_nol = marc_no
        self.__title = title
        self.__doctype = doctype
        self.__isbn = isbn
        self.__author = author
        self.__publisher = publisher
        self.__store_num = store_num
        self.__lendable_num = lendable_num

    def __str__(self):
        return '\nmarc_no :' + self.__marc_nol + \
            '\n书名:' + self.__title + \
            '\n责任者:' + self.__author + \
            '\n文档类型:' + self.__doctype + \
            '\nisbn: ' + self.__isbn + \
            '\n出版社:' + self.__publisher + \
            '\n馆藏副本' + self.__store_num + \
            '\n可借副本' + self.__lendable_num

    def to_json_obj(self):
        return {"marc_no":self.__marc_nol, "title":self.__title, "doctype":self.__doctype,
                "isbn":self.__isbn, "author":self.__author, "publisher":self.__publisher,
                "store_num":self.__store_num, "lendable_num":self.__lendable_num }
