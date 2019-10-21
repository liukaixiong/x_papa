import logging

import requests

from x_weibo.spiders.abs.AbstractWeiBoProcess import AbstractWeiBoProcess

"""
    与scrapy结合，这里没有做过多的实现，主要是一些递归方面的问题。
    例如 ： 我爬取了一条微博信息，但是我想知道微博下面有哪些评论，评论的用户有哪些？
"""


class DefaultWeiBoProcess(AbstractWeiBoProcess):
    logging.basicConfig(level=logging.NOTSET,
                        format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

    def rs_process_user(self, result):
        return result

    def rs_weibo_user_info(self, result):
        logging.debug(" - rs_weibo_user_info -")
        return result

    def rs_weibo_object(self, result):
        logging.debug(" - rs_weibo_object -")
        result_id = result["微博编号"]
        yield result
        yield from self.cn_weibo_comments(result_id)

    def rs_weibo_list(self, result):
        return result

    def rs_weibo_comments_object(self, pinlun, result_object):
        logging.debug(" - rs_weibo_comments_object -")
        user_id = result_object["用户编号"]
        weibo_info = {}
        weibo_info["来源编号"] = result_object["微博编号"]
        weibo_info["来源类型"] = result_object["groupType"]
        yield self.cn_process_user_info(user_id, weibo_info)
        yield result_object

    def rs_weibo_comments_list(self, pinglun_list, result_list):
        logging.debug(" - rs_weibo_comments_object -")


if __name__ == '__main__':
    process = DefaultWeiBoProcess()
    # process = DefaultWeiBoProcess()
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    #     'Cookie': '_T_WM=88819513180; ALF=1571883517; SCF=Amp0K_iWqOQXNBAacw3C0u_dVbzxhJVtBjTuuLjNPTIU8hWx_R9rBWZ8hNrMx4RY9OdBmG5hw89iTUXr25S1qB8.; SUB=_2A25wjQ7ZDeThGeNI6VUQ9y3NyzyIHXVQcZKRrDV6PUJbktANLRnjkW1NSJ3XCaB4ggZa0iiZR2KUTAfhHkkbE24g; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFdc7grDhZy8BfuLoHqaYFI5JpX5K-hUgL.Fo-ceoMpS0epeh52dJLoI0YLxKBLBo.LBK5LxKqL1heLB-qLxK-L1K5LB-eLxKBLB.BLBK5LxKnLB-qLBoBLxKqL122LBo2LxKqLB-BL1h.t; SUHB=0wnlkNF2YzH2q2; SSOLoginState=1569291913'
    # }
    # resp = requests.get("https://weibo.cn/5571847982", headers=headers)
    # process.cn_process_user_info("1684756320")
    # process.cn_process_user_response(resp)
    # comments = process.cn_weibo_comments("IblMftNTq", page=12, min_like_count=10)
    # while True:
    #     next(comments)
    # single = process.cn_process_weibo_by_single("IbBAJBFt6")
    # while True:
    #     obj = next(single)
    #     print("===================", obj)
    single = process.com_process_weibo_by_single("", "")
    while True:
        next(single)
