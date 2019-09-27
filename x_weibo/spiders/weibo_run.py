import scrapy
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 爬取单个帐号下面的微博信息
from x_weibo.spiders.abs.DefaultWeiBoProcess import DefaultWeiBoProcess


class WeiBoRun(Spider):
    # logging.basicConfig(level=logging.NOTSET,
    #                     format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    name = "weibo_run"
    base_url = "https://weibo.cn"

    def start_requests(self):
        urls = [
            'https://weibo.cn/topgirls8?filter=1'
            # 'https://weibo.com/topgirls8?is_all=1'
            # 'https://weibo.com/u/6116808854?from=usercardnew&refer_flag=0000020001_'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_html, method='GET', dont_filter=True)

    def parse_html(self, response):
        # 爬取用户信息
        weibo = DefaultWeiBoProcess()
        yield weibo.cn_process_user_response(response=response)
        # 爬取用户微博
        yield from weibo.cn_process_weibo(response=response)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('weibo_run')
    process.start()
