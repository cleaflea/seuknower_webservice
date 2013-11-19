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

# 根据提交的文本模糊匹配问题的标题并且返回相应的问题列表
def findEventByContent(request, content):
    eventContent = content
    cursor = connection.cursor()
    # 必须要encode一下，不然又是蛋疼的python中unicode编码问题
    txt = '%'+eventContent.encode('utf-8')+'%'
    cursor.execute("select * from seu_event where title like %s", [txt])
    rows = cursor.fetchall()

    returndata = []

    for row in rows:
        # print row
        tempdata = {}
        tempdata['id'] = trans(row[0])
        tempdata['title'] = trans(row[1])
        tempdata['intro'] = trans(row[2])
        tempdata['u_id'] = trans(row[3])
        tempdata['create_time'] = trans(row[4])
        tempdata['type'] = trans(row[5])
        tempdata['best_answer'] = trans(row[6])
        tempdata['anonymous'] = trans(row[7])
        tempdata['answer_count'] = trans(row[8])
        tempdata['has_answer'] = trans(row[9])
        tempdata['focus_count'] = trans(row[10])
        tempdata['click'] = trans(row[11])

        # returndata.append(tempdata)
        returnurl = 'http://www.seuknower.com/question/%s' % tempdata['id']
        returnstr = tempdata['title'] + ' ' + returnurl + '\n'

        returndata.append(returnstr)

    return HttpResponse(json.dumps(returndata, ensure_ascii=False), mimetype='application/json')

def findEventLatest(request):
    cursor = connection.cursor()
    cursor.execute("select * from seu_event order by create_time desc limit 1")
    row = cursor.fetchone()

    returndata = []

    tempdata = {}
    tempdata['id'] = trans(row[0])
    tempdata['title'] = trans(row[1])

    # returndata.append(tempdata)
    returnurl = 'http://www.seuknower.com/event/%s' % tempdata['id']
    returnstr = tempdata['title'] + ' ' + returnurl + '\n'

    returndata.append(returnstr)

    return HttpResponse(json.dumps(returndata, ensure_ascii=False), mimetype='application/json')