import jsonpath
import requests
import random

from x_weibo import weibo_login_user

session = requests.session()
user_agents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
    'Mobile/13B143 Safari/601.1]',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.23 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.23 Mobile Safari/537.36']

headers = {
    'User_Agent': random.choice(user_agents),
    'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
    'Origin': 'https://passport.weibo.cn',
    'Host': 'passport.weibo.cn'
}
post_data = {
    'username': '',
    'password': '',
    'savestate': '1',
    'ec': '0',
    'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
    'entry': 'mweibo'
}
# 这个入口仍然有效
login_url = 'https://passport.weibo.cn/sso/login'


def login(username, password):
    # username = input('请输入用户名:\n')
    # password = input('请输入密码：\n')
    post_data['username'] = username
    post_data['password'] = password
    r = session.post(login_url, data=post_data, headers=headers)
    if r.status_code != 200:
        return "login_error"
    else:
        print("模拟登陆成功,当前登陆账号为：" + post_data['username'])
    return r


def batch_login():
    user_info = weibo_login_user.login_user
    cookie_list = {}
    for username in user_info:
        result = login(username, user_info[username])
        if result == "login_error":
            print("登录失败 : " + username)
        else:
            cookie_value = result.headers["set-cookie"]
            cookie_list[username] = cookie_value
    return cookie_list


if __name__ == '__main__':
    cookie = batch_login()
    cookie_value = cookie["17621253557"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Cookie': cookie_value
    }
    get = requests.get("https://weibo.cn/topgirls8", headers=headers)
    print(get.text)
