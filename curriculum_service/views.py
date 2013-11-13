# -*- coding: utf-8 -*-

from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
import urllib
import json
import re

# return the term
def getCurriculumTerm(request):
    uFile = urllib.urlopen('http://xk.urp.seu.edu.cn/jw_service/service/lookCurriculum.action')
    html = uFile.read().decode('utf-8')
    # html = uFile.read()

    soup = BeautifulSoup(html)
    terms = soup.findAll('option')
    termList = [term.text for term in terms]

    return HttpResponse(json.dumps(termList, ensure_ascii=False), mimetype='application/json')

def parserHtml(request, cardNumber, academicYear):
    params = urllib.urlencode(
        {'queryStudentId': cardNumber, 'queryAcademicYear': academicYear})
    uFile = urllib.urlopen(
        "http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action", params)
    # decode(utf-8) turn to normal unicode that can encode to other protocal
    html = uFile.read().decode('utf-8')

    # match chinese should use ur not r
    pat = re.compile(ur'没有找到该学生信息', re.U)
    match = pat.search(html)
    if match:
        return HttpResponse('没有找到该学生信息')
    else:
        soup = BeautifulSoup(html)
        # 去除合计这一项
        sidebarCourses = soup.findAll('td', height='34', width='35%')[:-1]
        sidebarCourseList = [
            sidebarCourse for sidebarCourse in sidebarCourses if sidebarCourse.text != u'&nbsp;']
        # cleantha--->连续用两次nextsibling是bs3的bug？
        lecturerList = [
            i.nextSibling.nextSibling.text[6:] for i in sidebarCourseList]
        creditList = [
            i.nextSibling.nextSibling.nextSibling.nextSibling.text[6:] for i in sidebarCourseList]
        weekList = [
            i.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.text[6:] for i in sidebarCourseList]
        sidebarList = []
        # xrange is faster than range
        # 把边上的课程名称对应的老师学分和上课周次存起来
        for i in xrange(len(sidebarCourseList)):
            sidebarList.append(
                [sidebarCourseList[i].text, lecturerList[i], creditList[i], weekList[i]])

        # 选择上午和下午的课并且包括上午和下午字符串
        table = soup.findAll("td", rowspan="5")
        br = BeautifulSoup('<br/>')

        morningCourseList = []
        for i in xrange(1, 6):
            morningCourse = []
            # filter the last elem is a $nbsp;
            # k%2==0 condition to filter the <br />
            # 把和一个课程相关的做成一个list然后一天的做成一个list然后一个礼拜的再做成一个list
            temp = []
            for j in [k for k in xrange(len(table[i].contents[:-1])) if not (k % 2)]:
                if not j % 3:
                    temp = []
                    morningCourse.append(temp)
                if table[i].contents[j] != br.br:
                    temp.append(table[i].contents[j])
                # 如果是没有上课地点的课那么本应该写上课地点的位置上是一个br
                else:
                    # cleantha--->这是要干嘛= =
                    table[i].contents.insert(j, br.br)
                    temp.append('')
            morningCourseList.append(morningCourse)

        afternoonCourseList = []
        for i in xrange(7, 12):
            afternoonCourse = []
            temp = []
            for j in [k for k in xrange(len(table[i].contents[:-1])) if not (k % 2)]:
                if not j % 3:
                    temp = []
                    afternoonCourse.append(temp)
                if table[i].contents[j] != br.br:
                    temp.append(table[i].contents[j])
                else:
                    table[i].contents.insert(j, br.br)
                    temp.append('')
            afternoonCourseList.append(afternoonCourse)

        table = soup.findAll('td', rowspan='2')

        eveningCourseList = []
        for i in xrange(1, 6):
            eveningCourse = []
            temp = []
            for j in [k for k in xrange(len(table[i].contents[:-1])) if not (k % 2)]:
                if not j % 3:
                    temp = []
                    eveningCourse.append(temp)
                if table[i].contents[j] != br.br:
                    temp.append(table[i].contents[j])
                else:
                    table[i].contents.insert(j, br.br)
                    temp.append('')
            eveningCourseList.append(eveningCourse)

        courseList = [
            morningCourseList, afternoonCourseList, eveningCourseList]
        for i in courseList:
            for j in i:
                for k in j:
                    print k[1]
                    k.insert(1, k[1].split(']')[0][1:-1])
                    k[2] = k[2].split(']')[1][:-1]

        saturdayCourse = []
        for i in [j for j in xrange(len(table[7].contents[:-1])) if not (j % 2)]:
            if not i % 3:
                temp = []
                saturdayCourse.append(temp)
            if table[7].contents[i] != br.br:
                temp.append(table[7].contents[i])
            else:
                table[7].contents[i].insert(j, br.br)
                temp.append('')

        # cleantha--->怎么处理周末的方法和处理周中课程的不一样，周末课程难道会有时候不显示周次和上课时间？
        for i in saturdayCourse:
            try:
                if i[1][:1] == '[':
                    i.insert(1, i[1].split(']')[0][1:-1])
                    i[2] = i[2].split(']')[1][:-1]
                else:
                    i.insert(1, ' ')
            except:
                pass
        sundayCourse = []
        for i in [j for j in xrange(len(table[9].contents[:-1])) if not (j % 2)]:
            if not i % 3:
                temp = []
                sundayCourse.append(temp)
            if table[9].contents[i] != br.br:
                temp.append(table[9].contents[i])
            else:
                table[9].contents[i].insert(j, br.br)
                temp.append('')
        for i in sundayCourse:
            try:
                if i[1][:1] == '[':
                    i.insert(1, i[1].split(']')[0][1:-1])
                    i[2] = i[2].split(']')[1][:-1]
                else:
                    i.insert(1, ' ')
            except:
                pass

        courseList.append(saturdayCourse)
        courseList.append(sundayCourse)
        return HttpResponse(json.dumps([sidebarList, courseList], ensure_ascii=False), mimetype='application/json')

