# -*- coding:utf-8 -*-
import json
import urllib
from BeautifulSoup import BeautifulSoup
import datetime
from django.http import HttpResponse

def getJwcInfor(request):
    baseUrl = 'http://jwc.seu.edu.cn'

    uFile = urllib.urlopen('http://jwc.seu.edu.cn/')
    html = uFile.read().decode('utf-8')

    soup = BeautifulSoup(html)
    # 去除头尾不相关的超链接，主要是要获取下面channel中那几中情况下面的超链接
    target = soup.findAll('a', {'target': '_blank', 'class': 'font3'})[5:-4]

    inforList = []
    for i in target:
        if i in target[:7]:
            channel = u'教务信息'
        elif i in target[7:14]:
            channel = u'学籍管理'
        elif i in target[14:21]:
            channel = u'实践教学'
        elif i in target[21:25]:
            channel = u'合作办学'
        elif i in target[25:29]:
            channel = u'教学研究'
        else:
            channel = u'教学评估'
        # 通过这种方法来获取属性中的值
        relUrl = i['href']
        page = urllib.urlopen(baseUrl + relUrl)
        pageHtml = page.read().decode('utf-8')
        pageSoup = BeautifulSoup(pageHtml)
        title = pageSoup.find('td', {'bgcolor': '#E6E6E6'}).text
        uplodeDate = pageSoup.find('td',  {'align': 'right'}).text[5:]
        # 你可以传一个True值,这样可以匹配每个id的name：也就是匹配每个id。
        linkList = pageSoup.findAll('a', {'id': True, 'target': '_blank'})
        attachmentList = []
        for i in linkList:
            link = baseUrl + i['href']
            # 直接获取最中间的纯文本
            name = i.text
            attachmentList.append([name, link])

        print uplodeDate[0]
        inforList.append([uplodeDate, channel, title, attachmentList])
    # 对info列表从大到小进行排序(reverse=True)，排序的键是更新日期的第一个数字 cleantha--->按更新的日期的第一个数字进行排序不合适把= =
    return HttpResponse(json.dumps(sorted(inforList, key=lambda uplodeDate: uplodeDate[0], reverse=True), ensure_ascii=False), mimetype='application/json')
