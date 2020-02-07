# import facebook
#
#
# user_token = 'EAACvOn8XIecBANY5ILkeZAIwWHyFUsDQZAmppxVsPgveZC4Q0GTJsc8twYMinGUawLvQhYpxqpKOLtDKKPsI6jvM2fiNzp3z1cYLYY7EpBzpK2SM7FdIhjnZApwwBMKAUGgr40P4FO2OhJNf1r2nZCHlF6Sio2ctSpX6CKPgg5yPiV2An64xa1IIQwNZAnrfybBgZBUK8p4zgZDZD'
# app_token = '192665775186407|sJAXHrZ4oWR8nKqXnUdwB8XSHvo'
#
# graph = facebook.GraphAPI(access_token=app_token, version="3.1")
#
# print(graph.__dict__)
#
#
# group_id = 'amazingplacespics'
# data = graph.get_object(group_id)
# print(data)



# from bs4 import BeautifulSoup
import requests
#
# x = requests.get('https://www.facebook.com/groups/amazingplacespics/')
# print(x.text)
# soup = BeautifulSoup(x.text, 'html.parser')
# elem = soup.find('div', {'class': 'groupSkyAux'})
# print(elem)
#
# print('История' in x.text)
# with open('tmp.html', 'w') as out:
# 	out.write(x.text)


# url = 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110'
# data = {
#     'lsd': lsd,
#     'charset_test': csettest,
#     'version': version,
#     'ajax': ajax,
#     'width': width,
#     'pxr': pxr,
#     'gps': gps,
#     'm_ts': mts,
#     'li': li,
# }
# data['email'] = 'email'
# data['pass'] = 'pass'





def colon_separated_data_to_dict(file_path):
    data = dict()
    for i in open(file_path, 'r').readlines():
        k, v = i.split(':', maxsplit=1)
        data[k.strip()] = v.strip()
    return data


def get_consent_cookies():
    url = 'https://www.facebook.com/cookie/consent/'
    'cookie: datr=3_4pXjTgRoM93yRkazwtJxHQ; sb=dAwqXirv3Tn58J0EInpoxmzc; ; wd=1436x971; locale=ru_RU; fr=5Ul8esus4LnzDUV9g.AWXH_urCQHppLFh6Uqs4lIxxoL0.BdXJCI.1Y.F45.0.0.BeOVtt.AWU2IuO8'


def get_login_cookies(session, login_data):
    u1 = 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110'
    u2 = 'https://m.facebook.com/login.php'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    cookies = session.get(u1, headers=headers).cookies
    r = session.post(
        u1,
        data={'email': 'insense.insights@gmail.com', 'pass': '*R5pdgg821'},
        headers=headers,
        cookies=cookies
    )
    r.raise_for_status()
    print(r.cookies)
    print(r.headers)
    print(r.status_code)
    if r.status_code == 302:
        cookies = r.cookies
        r = session.post(
            r.headers['location'],
            # data={'email': 'insense.insights@gmail.com', 'pass': '*R5pdgg821'},
            headers=headers,
            cookies=cookies
        )
    with open('login.html', 'w') as out:
        out.write(r.text)
    # assert 'c_user' in r.cookies
    return r.cookies


if __name__ == '__main__':
    x = requests.get('https://www.facebook.com/')
    print(x.cookies)
    url = 'https://www.facebook.com/common/referer_frame.php'
    headers = colon_separated_data_to_dict('step1.sec')
    q = requests.get(url, headers=headers, cookies=x.cookies)
    print(q.status_code)
    print(q.text)
    print(q.cookies)
    print(q.headers)
    exit()
    s = requests.Session()
    login_file = 'login.sec'
    cookies = get_login_cookies(s, colon_separated_data_to_dict(login_file))

    x = s.get('https://www.facebook.com/groups/amazingplacespics/', cookies=cookies)
    # print(x.text)
    with open('tmp.html', 'w') as out:
        out.write(x.text)
# "*t6pdgg8211"