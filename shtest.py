import xlrd
import numpy as np
import pandas as pd
from io import StringIO

CSV_data=pd.read_csv('table.csv',delimiter=",",encoding='gbk')
print(CSV_data.head())

EXCEL_data=pd.read_excel('table.xls')
print(EXCEL_data.head())