# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from x_weibo.spiders.abs.WeiBoMysqlDBProcess import WeiBoMysqlDBProcess


class SWeiboPipeline(object):
    db = WeiBoMysqlDBProcess()

    def open_spider(self, spider):
        self.db.connect()

    def process_item(self, items, spider):
        self.db.process_item(items, spider)
        return items

    def close_spider(self, spider):
        # self.db_obj.save('test_data.xlsx')
        # self.db.close_spider(spider)
        print(spider)
        # self.sheet1.close()
