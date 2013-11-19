# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.db import connection
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def trans(x):
    if type(x) == int or type(x) == long:
        return str(x)
    else:
        return x

def findCommodityByContent(request, content):
    cursor = connection.cursor()
    txt = '%'+content.encode('utf-8')+'%'
    cursor.execute("select * from seu_commodity where title like %s", [txt])
    rows = cursor.fetchall()

    returndata = []

    for row in rows:
        # print row
        tempdata = {}
        tempdata['id'] = trans(row[0])
        tempdata['title'] = trans(row[1])

        # returndata.append(tempdata)
        returnurl = 'http://www.seuknower.com/market/commodity/%s' % tempdata['id']
        returnstr = tempdata['title'] + ' ' + returnurl + '\n'

        returndata.append(returnstr)

    return HttpResponse(json.dumps(returndata, ensure_ascii=False), mimetype='application/json')
