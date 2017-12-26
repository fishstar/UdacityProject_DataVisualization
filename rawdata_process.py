#!/usr/bin/python
# python 3

import pandas as pd

years = range(1987,2009)
colnames = ['Year', 'Month', 'DayofMonth', 'DayOfWeek', 'ArrDelay']
pieces = []

for year in years:
	# 数据文件路径
    filename = './Flights_Dataset/%d.csv.bz2' % year
    # 分段读取数据，并对每年的数据做分组求和
    for chunk in pd.read_csv(filename, usecols=colnames, chunksize=10**6, compression='bz2' ):
        piece = chunk.groupby(['Year', 'Month', 'DayofMonth'], as_index=False) \
            [['DayOfWeek', 'ArrDelay']].agg({'ArrDelay':['sum', 'count'], 'DayOfWeek':'first'})
        pieces.append(piece)
    print(year,  'finished')
        
df = pd.concat(pieces)  

df.columns = ['Year', 'Month', 'DayofMonth', 'TotalArrDelay', 'Num', 'DayOfWeek']

df = df.groupby(['Year', 'Month', 'DayofMonth'], as_index=False) \
    [['DayOfWeek', 'TotalArrDelay', 'Num']].agg({'TotalArrDelay':'sum', 'Num':'sum', 'DayOfWeek':'first'})

#年均数据
avg_y = df.groupby('year').apply(avgdelay).reset_index()
avg_y.columns = ['year', 'avgdelay']
avg_y['category'] = 'Avg'

# 按月份筛选数据
avg_ym = df.groupby(['year', 'month']).apply(avgdelay).reset_index()
avg_ym.columns = ['year', 'category', 'avgdelay']
month_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
avg_ym.category = avg_ym.category.map(month_map)

#按星期筛选数据
avg_yw = df.groupby(['year', 'week']).apply(avgdelay).reset_index()
avg_yw.columns = ['year', 'category', 'avgdelay']
week_map = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
avg_yw.category = avg_yw.category.map(week_map)

# 合并数据并存储
avg_ymw = pd.concat([avg_y, avg_ym, avg_yw], ignore_index=True)
avg_ymw.to_csv('flights_avgdelay.csv', index=None)