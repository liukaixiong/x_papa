# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt as xlwt

from common.excelUtils import excelUtils
from x_weibo.spiders.utils.spiderConstants import spiderConstants


class SWeiboPipeline(object):
    is_first = {}
    sheet_header = {}
    sheet_list = {}
    ins_excelUtils = excelUtils()

    def open_spider(self, spider):
        self.wk = xlwt.Workbook()

    def process_item(self, items, spider):
        print("-----------insert----------->>>" + items[spiderConstants.group_type])
        self.ins_excelUtils.objectToExcel(self.wk, items)
        return items

    def close_spider(self, spider):
        self.wk.save('test_data.xlsx')
        print(spider)
        # self.sheet1.close()
