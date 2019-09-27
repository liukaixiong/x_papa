import logging

from x_weibo.spiders.abs.AbstractWeiBoProcess import AbstractWeiBoProcess


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
        yield from self.cn_weibo_comments(result_id)
        yield result

    def rs_weibo_list(self, result):
        return result

    def rs_weibo_comments_object(self, pinlun, result_object):
        logging.debug(" - rs_weibo_comments_object -")
        user_id = result_object["用户编号"]
        yield self.cn_process_user_info(user_id)
        yield result_object

    def rs_weibo_comments_list(self, pinglun_list, result_list):
        logging.debug(" - rs_weibo_comments_object -")


if __name__ == '__main__':
    process = DefaultWeiBoProcess()
    process.cn_process_user_info("1684756320")