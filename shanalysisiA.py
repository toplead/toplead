import xlrd

import numpy as np
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from pandas import options                                     # noqa: E402
options.io.excel.xls.writer = 'xlwt'


CSV_data=pd.read_csv('table.csv',delimiter=",",encoding='gbk')
#print(CSV_data.head())

EXCEL_data=pd.read_excel('table.xls',na_values='--')#recognize NULL str
#print(EXCEL_data.head())

#print(CSV_data.dtypes)
#print(EXCEL_data.dtypes)

datesplit=EXCEL_data['时间'].str.split(',',expand=True)
new_name=['日期','星期']
datesplit.columns=new_name
#print(datesplit.head())

EXCEL_data=pd.concat([datesplit,EXCEL_data],axis=1)
EXCEL_data.pop('时间')



EXCEL_data.set_index('日期',inplace=True)#set index,and make it avalibale

#EXCEL_data.interpolate(inplace=True).iloc[1:,:]
#print(EXCEL_data.head())
# statistic week catologue
EXCEL_data['开盘'].plot.hist(alpha=0.5)
#plt.show()
result=EXCEL_data.groupby('星期',sort=False).describe()
result.to_excel('group.xls',sheet_name='sheet1',engine='xlsxwriter')

# caculate ma
EXCEL_data.insert(10,'threema',EXCEL_data.收盘.rolling(3).mean())
EXCEL_data.insert(11,'ninema',EXCEL_data.收盘.rolling(9).mean())
EXCEL_data.insert(12,'twentyonema',EXCEL_data.收盘.rolling(21).mean())
EXCEL_data.insert(13,'fiftyfivema',EXCEL_data.收盘.rolling(55).mean())

EXCEL_data.dropna(how='any',inplace=True)

# maperiod
EXCEL_data['mark3']=np.where(EXCEL_data.收盘>EXCEL_data.threema,1,0)
EXCEL_data['mark9']=np.where(EXCEL_data.收盘>EXCEL_data.ninema,1,0)
EXCEL_data['mark21']=np.where(EXCEL_data.收盘>EXCEL_data.twentyonema,1,0)
EXCEL_data['mark55']=np.where(EXCEL_data.收盘>EXCEL_data.fiftyfivema,1,0)

EXCEL_data['p%']=((EXCEL_data.收盘-EXCEL_data.fiftyfivema)+(EXCEL_data.ninema-EXCEL_data.twentyonema)+(EXCEL_data.ninema-EXCEL_data.fiftyfivema))/EXCEL_data.fiftyfivema
EXCEL_data['s%']=((EXCEL_data.ninema-EXCEL_data.twentyonema)+(EXCEL_data.ninema-EXCEL_data.fiftyfivema))/EXCEL_data.fiftyfivema

EXCEL_data['cumsum3']=EXCEL_data['mark3'].cumsum()
#EXCEL_data['count3']=EXCEL_data.GroupBy('mark3').count()
zero_count=EXCEL_data[EXCEL_data['mark3']==0].groupby('cumsum3').size()
zero_count_index=EXCEL_data[EXCEL_data['mark3']==0].groupby('cumsum3',as_index=False).first()
#zero_count_index=list(zero_count_index['日期'])
print(zero_count_index)
#sub_zero_court=zero_court[1]
one_count=zero_count.index.to_series().diff()
#col_count=zero_count.append(one_count)


#print(zero_count)
new_zero_one=pd.merge(zero_count.rename('zero'),one_count.rename('one'),left_index=True,right_index=True)
#print(one_count)
#EXCEL_data['count3']=EXCEL_data.groupby('mark3').transform(zero_court)
with pd.ExcelWriter("shdata.xls") as writer:
    EXCEL_data.to_excel(writer,sheet_name='sheet1')
    new_zero_one.to_excel(writer,sheet_name='sheet2')
   
EXCEL_data.to_excel('ma.xls',sheet_name='sheet1',engine='xlsxwriter')
#zero_count.to_excel('ma.xls',sheet_name='sheet2',engine='xlsxwriter')
#one_count.to_excel('ma.xls',sheet_name='sheet2',engine='xlsxwriter')