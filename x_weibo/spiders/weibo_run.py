import logging
from time import sleep

import scrapy
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 爬取单个帐号下面的微博信息
from x_weibo.spiders.abs.DefaultWeiBoProcess import DefaultWeiBoProcess


class WeiBoRun(Spider):
    logging.basicConfig(level=logging.NOTSET,
                        format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    name = "weibo_run"
    base_url = "https://weibo.cn"
    # 爬取用户信息
    weibo = DefaultWeiBoProcess()

    def start_requests(self):
        urls = [
            'https://weibo.cn/topgirls8?page=7'
            # 'https://weibo.cn/comment/I89NOfaDC',
            # 'https://weibo.cn/comment/I8LvN5WbV',
            # 'https://weibo.cn/comment/I8KY3fCBH',
            # 'https://weibo.cn/comment/I8C5idsDI'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_html, method='GET', dont_filter=True)

    def parse_html(self, response):
        if response.status == 200:
            # 表示从单条微博开始爬取
            url = response.url
            if url.find("comment") > 0:
                comment_no = url[url.rindex("/") + 1:]
                yield from self.weibo.cn_process_weibo_by_single(comment_no)
            else:
                yield self.weibo.cn_process_user_response(response=response)
                # 爬取用户微博
                yield from self.weibo.cn_process_weibo_by_all(response=response)
        else:
            logging.info(" 爬取太过频繁,休眠一段时间再继续.")
            sleep(5)
            reset_response = self.weibo.get_response(response.url)
            yield from self.parse_html(reset_response)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('weibo_run')
    process.start()
