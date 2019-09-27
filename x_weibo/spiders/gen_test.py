import logging

import requests

#
# def fib(max):
#     n, a, b = 0, 0, 1
#     while n < max:
#         yield b
#         a, b = b, a + b
#         n = n + 1
#     return 'done'
#
#
# def req():
#     request = requests.request(method="GET", url="http://www.baidu.com")
#     print(request.content.decode())

logging.basicConfig(level=logging.NOTSET,
                    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# 将信息打印到控制台上
logging.debug(u"苍井空")
logging.info("麻生希 %s - ccc","aaa")
logging.warning(u"小泽玛利亚")
logging.error(u"桃谷绘里香")
logging.critical(u"泷泽萝拉")

# if __name__ == '__main__':
    # req()
