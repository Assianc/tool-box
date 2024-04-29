import pandas as pd

# 读取SAS7BDAT文件
sas_data = pd.read_sas('hhinc_10.sas7bdat')

# 将数据保存为CSV文件
sas_data.to_csv('hhinc.csv', index=False)
