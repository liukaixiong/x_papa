import xlwt

from common.excelUtils import excelUtils
from x_weibo.spiders.abs.AbstractDBProcess import AbstractDBProcess

"""
    Excel 导出
"""


class ExcelDBProcess(AbstractDBProcess):
    ins_excelUtils = excelUtils()

    def connect(self):
        self.db_obj = xlwt.Workbook()

    def process_item(self, items, spider):
        self.ins_excelUtils.objectToExcel(self.db_obj, items)

    def close_spider(self, spider):
        self.db_obj.save('test_data.xlsx')
