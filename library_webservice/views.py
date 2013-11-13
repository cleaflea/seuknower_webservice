# __author__ = 'cleantha'

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

@csrf_exempt
def check_account(request):
    username = request.POST['username']
    pwd = request.POST['password']
    # username = '08010422'
    # pwd = '08010422'
    service = library_service.LibraryService(username, pwd)
    status = service.check_account()
    return HttpResponse(str(status))

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

    return HttpResponse(json.dumps(book_list, ensure_ascii=False), mimetype='application/json')
