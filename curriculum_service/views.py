# -*- coding: utf-8 -*-

from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup
import urllib
import json
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

        # 这个解析的方法是一个比较讨巧的方法，一般情况是对td做contents之后得到的列表中<br>是出现在奇数位置的，而和课程相关的信息是出现在偶数位置的，并且当一个td中有两个课程的时候另一个课程的开始位置是6，如果有三次课就是9这也是下面代码判断j%3的作用
        # 当时上面的是理想情况，理想情况就是一门课的信息就是课名时间和上课地点，但是假如td里面的课程没有课程地点这个信息，那之后的课程信息都会出现在contents列表的奇数位置，而不是偶数位置了，这个就需要在偶数位置如果是<br>的时候再插入一个标签，下面代码插入的是<br>，这样就可以保证后面的课程信息又是出现在偶数位置了
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
                    # 这里的作用就是为了处理像这样没有上课地点，情况，这样就要填充一个br或者其他的东西来让和课程有关的信息出现在contents列表中的偶数位置
                    # <td class="line_topleft" rowspan="2"   align="center">工业系统认识1<br>[6-6周]11-13节<br><br>电路基础<br>[1-16周]11-12节<br>九龙湖教七-203<br>&nbsp;</td>
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

def getCurriculumByDay(request, cardNumber, academicYear, weekday):
    print 'weekday--->' + weekday
    params = urllib.urlencode(
        {'queryStudentId': cardNumber, 'queryAcademicYear': academicYear})
    uFile = urllib.urlopen(
        "http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action", params)
    # decode(utf-8) turn to normal unicode that can encode to other protocal
    html = uFile.read().decode('utf-8')

    pat = re.compile(ur'没有找到该学生信息', re.U)
    match = pat.search(html)
    if match:
        return HttpResponse('没有找到该学生信息')

    soup = BeautifulSoup(html)

    weekday = int(weekday)

    # 周一到周五
    if weekday != 6 and weekday != 0:

        print 'weekday'

        table = soup.findAll("td", rowspan="5")
        br = BeautifulSoup('<br/>')

        morningCourse = []
        for j in [k for k in xrange(len(table[weekday].contents[:-1])) if not (k % 2)]:
            if not j % 3:
                # temp = []
                morningCourse.append(table[weekday].contents[j])
            if table[weekday].contents[j] != br.br:
                # temp.append(table[3].contents[j])
                pass
            else:
                table[weekday].contents.insert(j, br.br)
                # temp.append('')

        for morning in morningCourse:
            print morning

        afternoonCourse = []
        for j in [k for k in xrange(len(table[weekday+6].contents[:-1])) if not (k % 2)]:
            if not j % 3:
                afternoonCourse.append(table[weekday+6].contents[j])
            if table[weekday+6].contents[j] != br.br:
                # temp.append(table[i].contents[j])
                pass
            else:
                table[weekday+6].contents.insert(j, br.br)
                # temp.append('')

        for afternoon in afternoonCourse:
            print afternoon

        table = soup.findAll('td', rowspan='2')

        eveningCourse = []
        for j in [k for k in xrange(len(table[weekday].contents[:-1])) if not (k % 2)]:
            if not j % 3:
                # temp = []
                eveningCourse.append(table[weekday].contents[j])
            if table[weekday].contents[j] != br.br:
                # temp.append(table[i].contents[j])
                pass
            else:
                table[weekday].contents.insert(j, br.br)
                # temp.append('')

        for evening in eveningCourse:
            print evening

        return HttpResponse(json.dumps([morningCourse, afternoonCourse, eveningCourse], ensure_ascii=False), mimetype='application/json')

    # 周六
    if weekday == 6:

        print 'saturday'

        table = soup.findAll('td', rowspan='2')
        br = BeautifulSoup('<br/>')

        saturdayCourse = []
        for i in [j for j in xrange(len(table[7].contents[:-1])) if not (j % 2)]:
            if not i % 3:
                # temp = []
                saturdayCourse.append(table[7].contents[i])
            if table[7].contents[i] != br.br:
                # temp.append(table[7].contents[i])
                pass
            else:
                table[7].contents[i].insert(j, br.br)
                # temp.append('')

        return HttpResponse(json.dumps(saturdayCourse, ensure_ascii=False), mimetype='application/json')


    # 周日
    if weekday == 0:

        print 'sunday'

        table = soup.findAll('td', rowspan='2')
        br = BeautifulSoup('<br/>')

        sundayCourse = []
        for i in [j for j in xrange(len(table[9].contents[:-1])) if not (j % 2)]:
            if not i % 3:
                # temp = []
                sundayCourse.append(table[9].contents[i])
            if table[9].contents[i] != br.br:
                # temp.append(table[9].contents[i])
                pass
            else:
                table[9].contents[i].insert(j, br.br)
                # temp.append('')
        for sunday in sundayCourse:
            print sunday

        return HttpResponse(json.dumps(sundayCourse, ensure_ascii=False), mimetype='application/json')

