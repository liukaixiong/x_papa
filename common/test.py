from x_weibo import weibo_login_user


def get_all_cookies():
    cookies_info = weibo_login_user.login_cookies
    for cookie in cookies_info:
        yield cookie


if __name__ == '__main__':
    cookies = get_all_cookies()
    try:
        while True:
            s = next(cookies)
            print(s)
    except StopIteration as e:
        print("结束了 。。。 ")
