# -*- encoding:utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import render_to_response

import library_service, config
import custom_exception
from django.views.decorators.csrf import csrf_exempt

REQUEST_PARAMS_ERROR = "request params error"
REQUEST_POST_ERROR = "request post data error"
SERVER_ERROR = "server error"
ACOUNT_ERROR = "username or password error"

'''到时候客户端的写交互代码的时候一定要把上面四个定义的ERROR都做一个容错判断，不然会有异常要让app崩溃的'''

@csrf_exempt
def check_account(request):
    username = request.POST['username']
    pwd = request.POST['password']
    # username = '08010422'
    # pwd = '08010422'
    service = library_service.LibraryService(username, pwd)
    status = service.check_account()
    return HttpResponse(str(status))

# 搜索图书
def search_book(request):
    service = library_service.LibraryService()
    try:
        strText = request.GET["strText"]
    except Exception,e:
        return HttpResponse(REQUEST_PARAMS_ERROR)

    try:
        page = request.GET["page"]
    except Exception,e:
        # config.logger.error(e)
        page = None

    try:
        if page:
            book_list = service.get_search_result_list(strText, page)
        else:
            book_list = service.get_search_result_list(strText)
    except Exception,e:
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)

    # book_list = service.get_search_result_list(strText=strText)
    return HttpResponse(json.dumps(book_list, ensure_ascii=False), mimetype='application/json')

# 查看图书详细信息
def book_detail(request):
    service = library_service.LibraryService()

    try:
        marc_no = request.GET["marc_no"]
    except Exception,e:
        return HttpResponse(REQUEST_PARAMS_ERROR)

    try:
        book_detail = service.get_book_detail(marc_no)
    except Exception,e:
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)

    return HttpResponse(json.dumps(book_detail, ensure_ascii=False))

# 如果不加这个装饰器的话由于csrf保护机制将无法从客户端正常post数据
# 查看已借图书
@csrf_exempt
def check_render_books(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)

    service = library_service.LibraryService(username, passwd)
    try:
        books = service.get_render_book_list()
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)

    return HttpResponse(json.dumps(books, ensure_ascii=False))
# 续借图书
@csrf_exempt
def renew_book(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
        barcode = request.POST["barcode"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)

    service = library_service.LibraryService(username, passwd)
    try:
        result = service.renew_book(barcode)
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR+str(e))

    return HttpResponse(json.dumps({"result":result}))
# 查看自己已经预约的书籍
@csrf_exempt
def check_appointed_books(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)

    service = library_service.LibraryService(username, passwd)
    try:
        books = service.get_appointed_books()
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)

    return HttpResponse(json.dumps(books, ensure_ascii=False))

# 取消预约
@csrf_exempt
def cancel_appoint(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
        call_no = request.POST["call_no"]
        marc_no = request.POST["marc_no"]
        loca = request.POST["loca"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)

    service = library_service.LibraryService(username, passwd)
    try:
        result = service.cancel_appoint(call_no, marc_no, loca)
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    return HttpResponse(json.dumps({'result':result}))

# 获取一本书的预约信息
@csrf_exempt
def appoint_info(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
        marc_no = request.POST['marc_no']
        # username = '08010422'
        # passwd = '08010422'
        # marc_no = '0000792503'
    except:
        return HttpResponse(REQUEST_PARAMS_ERROR)

    service = library_service.LibraryService(username, passwd)
    try:
        detail = service.get_appoint_book_info(marc_no)
        #detail = service.get_appoint_book_info('0000519601')
        print detail
        print 'cleantha'
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        #print e
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)

    return HttpResponse(json.dumps(detail, ensure_ascii=False))

# 预约一本书
@csrf_exempt
def appoint_book(request):
    try:
        #callnol, location, check, take_loca='90001'
        username = request.POST["username"]
        passwd = request.POST["password"]
        call_no = request.POST["call_no"]
        location = request.POST["location"]
        check = request.POST["check"]
        take_loca = request.POST['take_loca']
        # username = '08010422'
        # passwd = '08010422'
        # call_no = 'TP393.092/2105'
        # location = '90013'
        # check = '1'
        # take_loca = '90001'

    except:
        return HttpResponse(REQUEST_POST_ERROR)

    service = library_service.LibraryService(username, passwd)
    try:
        result = service.appoint_book(call_no, location, check, take_loca)
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        print e
        # config.logger.error(e)
        return HttpResponse(SERVER_ERROR)

    return HttpResponse(json.dumps({"result":result}))
