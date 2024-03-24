import os
import pandas as pd

# 设置 Excel 文件夹路径和 CSV 文件夹路径
excel_folder = r'D:\ths\delete_end_row'
csv_folder = r'D:\ths\csv'

# 获取 Excel 文件夹中的所有文件
excel_files = [f for f in os.listdir(excel_folder) if f.endswith('.xlsx')]

# 循环处理每个 Excel 文件
for file in excel_files:
    # 读取 Excel 文件
    excel_file_path = os.path.join(excel_folder, file)
    df = pd.read_excel(excel_file_path)

    # 构造 CSV 文件路径
    csv_file_path = os.path.join(csv_folder, file.replace('.xlsx', '.csv'))

    # 将数据保存为 CSV 文件
    df.to_csv(csv_file_path, index=False)
