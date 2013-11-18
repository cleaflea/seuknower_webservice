# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.db import connection
import json

def trans(x):
    if type(x) == int or type(x) == long:
        return str(x)
    else:
        return x

# 根据提交的文本模糊匹配问题的标题并且返回相应的问题列表
def findQuestionByContent(request, content):
    questionContent = content
    cursor = connection.cursor()
    # 必须要encode一下，不然又是蛋疼的python中unicode编码问题
    txt = '%'+questionContent.encode('utf-8')+'%'
    cursor.execute("select * from seu_question where title like %s", [txt])
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

        returndata.append(tempdata)

    return HttpResponse(json.dumps(returndata, ensure_ascii=False), mimetype='application/json')

    # print rows
    # print type(rows)
    # print 'id--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[0])
    # print 'title--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[1])
    # print 'intro--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[2])
    # print 'u_id--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[3])
    # print 'create_time--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[4])
    # print 'type--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[5])
    # print 'best_answer--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[6])
    # print 'anonymous--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[7])
    # print 'answer_count--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[8])
    # print 'has_answer--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[9])
    # print 'focus_count--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[10])
    # print 'click--->' + (lambda x: str(x) if type(x) == int or type(x) == long else x)(rows[11])
