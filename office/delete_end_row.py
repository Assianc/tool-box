import os
import openpyxl

# 获取目录 D:\ths 下的所有 Excel 文件
excel_files = [os.path.join('D:\\ths\\delete_end_row', f) for f in os.listdir('D:\\ths\\delete_end_row') if
               f.endswith('.xlsx')]

# 循环处理每个 Excel 文件
for excel_file in excel_files:
    # 打开要处理的 Excel 文件
    wb = openpyxl.load_workbook(excel_file)

    # 获取要处理的工作表
    sheet = wb.active

    # 获取最后一行号
    last_row_num = sheet.max_row

    # 删除最后一行
    sheet.delete_rows(last_row_num)

    # 保存修改后的文件
    wb.save(excel_file)
