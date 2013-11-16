# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

import page_crawler
import page_parser
import custom_exception

ServerError = "Server Error"
AccountError = "Account Error"
RequestError = "Request Error"

@csrf_exempt
def check_account(reqeust):
    try:
        try:
            card_number = reqeust.POST['card_number']
            passwd = reqeust.POST['password']
        except:
            return HttpResponse(RequestError)
        state = page_crawler.login(card_number, passwd)
        if state.get_login_status():
            return HttpResponse("True")
        else:
            return HttpResponse("False")
    except Exception,e:
        return HttpResponse(ServerError)

def tyxPc(request, cardNumber, password):
    try:
        html = page_crawler.crawl_paocao_page(cardNumber, password)
        if html == "体育系故障，请稍后再试":
            return HttpResponse("体育系故障，请稍后再试")
        pc_number = page_parser.get_paocao_number(html)
        return HttpResponse(pc_number)
    except custom_exception.AccountError, e:
        return HttpResponse(AccountError)
    except Exception, e:
        return HttpResponse(ServerError)