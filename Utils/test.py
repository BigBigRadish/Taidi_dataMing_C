# -*- coding: utf-8 -*-
'''
Created on 2019年3月29日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#比较通过百度地图的纠偏接口数据 和 GpsConvert转换类数据接口 纠偏后的经纬度差异

import requests
import math,base64, json
from GpsConvert import GpsConvert #引入GPSConvert 地址转换类



#百度地图纠偏接口如下：
#http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=113.540124&y=23.517846
#from=0 代表传入真实经纬度
#to=4 代表转换成百度纠偏后的经纬度
#输出json格式：
#{"error":0,"x":"MTEzLjU1MTgwNzMy","y":"MjMuNTIxMjMzOTEwNjQ2"}
#x、y分别是纠偏后的经纬度值，base64编码格式，大家可根据base64编码转换成明码
r=requests.get("http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=113.540124&y=23.517846")
doc = json.loads(r.text)
print(base64.b64decode(doc.get('x')))
print(base64.b64decode(doc.get('y')))
#print(doc)


#以下输出GPS经纬度（即GPS设备上传的原始数据）转换为百度地图纠偏后的经纬度
w=GpsConvert()
y=w.wgs84togcj02(113.540124,23.517846) #GPS转火星
x=w.gcj02tobd09(y[0],y[1]) #火星转百度
print(x[0]) #转换后经度
print(x[1])  #转换后纬度


#经测试 在百度地图商标点 15倍缩放比例情况下 两个点重合