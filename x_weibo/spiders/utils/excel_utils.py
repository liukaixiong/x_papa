# # 导入xlwt库用于写excel文件
# import xlwt
#
# # 初始化并创建一个工作簿
# book = xlwt.Workbook()
# # 创建一个名为sheetname的表单
# sheet = book.add_sheet('sheetname')
# # 在row_n行col_n列处单元格内写入value值
# for i in range(0, 10):
#     index = str(i)
#     sheet.write(0, i, "某某某_" + index)
# # 将工作簿以bookname命名并保存
# book.save('bookname.xls')
#
# # 合并单元格：将由row_start,row_finish行,col_start,col_finish列构成的区域单元格合并并写入value值
# # sheet.write_merge(row_start,row_finish,col_start,col_finish,value)
