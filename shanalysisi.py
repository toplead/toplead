import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from pandas import options                                     # noqa: E402
options.io.excel.xls.writer = 'xlwt'


CSV_data=pd.read_csv('table.csv',delimiter=",",encoding='gbk')
print(CSV_data.head())

EXCEL_data=pd.read_excel('table.xls',na_values='--')#recognize NULL str
print(EXCEL_data.head())

print(CSV_data.dtypes)
print(EXCEL_data.dtypes)

datesplit=EXCEL_data['时间'].str.split(',',expand=True)
new_name=['日期','星期']
datesplit.columns=new_name
print(datesplit.head())

EXCEL_data=pd.concat([datesplit,EXCEL_data],axis=1)
EXCEL_data.pop('时间')



EXCEL_data.set_index('日期',inplace=True)#set index,and make it avalibale

#EXCEL_data.interpolate(inplace=True).iloc[1:,:]
print(EXCEL_data.head())
# statistic week catologue
EXCEL_data['开盘'].plot.hist(alpha=0.5)
plt.show()
result=EXCEL_data.groupby('星期',sort=False).describe()
result.to_excel('group.xls')
# caculate ma
EXCEL_data.insert(10,'threema',EXCEL_data.收盘.rolling(3).mean())
EXCEL_data.insert(11,'ninema',EXCEL_data.收盘.rolling(9).mean())
EXCEL_data.insert(12,'twentyonema',EXCEL_data.收盘.rolling(21).mean())
EXCEL_data.insert(13,'fiftyfivema',EXCEL_data.收盘.rolling(55).mean())

# maperiod
EXCEL_data['mark3']=np.where(EXCEL_data.收盘>EXCEL_data.threema,1,0)
EXCEL_data['mark9']=np.where(EXCEL_data.收盘>EXCEL_data.ninema,1,0)
EXCEL_data['mark21']=np.where(EXCEL_data.收盘>EXCEL_data.twentyonema,1,0)
EXCEL_data['mark55']=np.where(EXCEL_data.收盘>EXCEL_data.fiftyfivema,1,0)


EXCEL_data.to_excel('ma.xls')