# -*- coding: utf-8 -*-
'''
Created on 2019年4月16日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#画时间序列图
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
df = pd.read_csv(r'../data/dd_train_100/AA00001.csv') 
df.location_time = pd.to_datetime(df.location_time)
fig1 = plt.figure(figsize=(15,5))
ax = fig1.add_subplot(1,1,1)
xfmt = mdates.DateFormatter('%y-%m-%d %H:%M')
ax.xaxis.set_major_formatter(xfmt)
plt.plot(df['location_time'],df['gps_speed']) 
plt.ylabel(u'速度',fontproperties='SimHei') 
plt.xlabel(u'时间',fontproperties='SimHei') 
plt.grid(True) 
plt.show()
# plt.savefig('时间-速度.png')