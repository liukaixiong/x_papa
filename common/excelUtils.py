import xlwt

from x_weibo.spiders.utils.spiderConstants import spiderConstants


class excelUtils(object):
    is_first = {}
    sheet_header = {}
    sheet_list = {}

    def writeObjectExcel(self, filename, items):
        workhook = xlwt.Workbook()
        self.objectToExcel(workhook, items)
        workhook.save(filename)

    # 可以构建多sheet的写入方法，动态将key转化成header。
    def objectToExcel(self, workbook, items):
        group_type = items[spiderConstants.group_type]
        first = self.is_first.get(group_type)
        sheet_info = self.sheet_list.get(group_type)
        sheet_header = self.sheet_header.get(group_type)
        if first is None:
            sheet_info = self.sheet_list[group_type] = workbook.add_sheet(group_type, cell_overwrite_ok=True)
            sheet_header = self.sheet_header[group_type] = list(items.keys())
            for i in range(0, len(sheet_header)):
                sheet_info.write(0, i, sheet_header[i])
            self.is_first[group_type] = False
        row_count = sheet_info.last_used_row + 1
        for k in items.keys():
            try:
                if sheet_header.__contains__(k) == False:
                    sheet_header.append(k)
                    sheet_info.write(0, len(sheet_header) - 1, k)
                sheet_info.write(row_count, sheet_header.index(k), items[k])
            except Exception as e:
                print(e)
                e.with_traceback()