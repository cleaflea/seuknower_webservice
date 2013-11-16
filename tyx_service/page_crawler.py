# -*- encoding: utf-8 -*-
import cookielib
import urllib
import urllib2

import config
import page_parser
import custom_exception


def login(cardNumber, password):
    # 抓包看看header和response就知道是怎么一回事情了
    # response返回的是奇怪而古老的内容，估计是淘汰的web技术了，反正len出来就是524，如果登陆失败len出来时1000多
    data = {
        'xh': str(cardNumber),
        'mm': str(password),
        'method': 'login'
    }
    cookieJar = cookielib.CookieJar()
    cookieHandler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookieHandler)
    urllib2.install_opener(opener)
    reqLogin = urllib2.Request(config.TYX_LOGIN_URL, urllib.urlencode(data))
    try:
        resLogin = urllib2.urlopen(reqLogin, timeout=config.TIME_OUT)
        html = resLogin.read()
        if len(html) == 524:
            state = page_parser.LoginState(True, opener)
        else:
            state = page_parser.LoginState(False, None)
    except:
        state = "体育系故障，请稍后再试"
    finally:
        return state

def crawl_paocao_page(cardNumber, password):
    '''
    Returns:
        html page.

    Raises:
        AccountError:
        urllib2.HTTPError:
        urllib2.URLError:
    '''
    state = login(cardNumber, password)
    if state == "体育系故障，请稍后再试":
        return state
    if state.get_login_status():
        urllib2.install_opener(state.get_opener())
        reqLoad = urllib2.Request(config.TYX_PC_URL)
        resLoad = urllib2.urlopen(reqLoad, timeout=config.TIME_OUT)
        html = resLoad.read()
        return html
    else:
        raise custom_exception.AccountError()
