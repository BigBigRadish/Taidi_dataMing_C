# -*- coding: utf-8 -*-
'''
Created on 2019年3月29日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
'''
第三题
(3) 综合考虑运输车辆的安全、效率和节能，并结合自然气象条件与道路状况等情况， 
为运输车辆管理部门建立行车安全的综合评价指标体系与综合评价模型。 
'''
import os
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from Utils import GpsConvert
import requests
import json
from datetime import datetime
from geopy.exc import GeocoderTimedOut
def datatime_2_date( dtime):
    date=dtime.split(' ')[0].split('-')
    year_=date[0]#年
    month_=date[1]#月
    day_=date[2]#日
    if(month_[0]=='0'):
        month=month_[1]
    else:
        month=month_
    if( day_[0]=='0'):
        day=day_[1]
    else:
        day=day_
    ans_time=day+'/'+month+'/'+year_
#     ans_time = datetime.strptime(date,"%Y/%m/%d")
    return ans_time
def do_geocode(geolocator,address):
    try:
        return geolocator.reverse(address)
    except GeocoderTimedOut:
        return do_geocode(geolocator,address)
#连接表与气象数据表
def merge_file(geolocator,gpsConvert):
    rw_train_path='../Result/result2/rw_train/'
    rusult3_data='../Result/result3/data/'
    rw_files=os.listdir(rw_train_path)
#     weather_file=pd.read_csv('../Result/result2/气象数据.csv',encoding='utf-8')
    for file in rw_files:     
        df2 = pd.read_csv(rw_train_path+file,encoding='utf-8')  #打开csv文件，注意编码问题，保存到df2中
        df2['date']=df2.location_time.apply(datatime_2_date)
        print(df2['date'])
        Province=[]#省
        City=[]#市
        District=[]#区县
        Street=[]#街道
        for _,i in df2[['lat','lng']].iterrows():
            huoxing=gpsConvert.wgs84togcj02(i['lng'], i['lat'])#转火星坐标 
            baidu_position=gpsConvert.gcj02tobd09(huoxing[0],huoxing[1])#转百度坐标
#             http://api.map.baidu.com/api?v=2.0&ak=tyasj0XIGmguGysATPGPXkffmVGp9Plu
            baiduUrl = "http://api.map.baidu.com/geocoder/v2/?ak=Oi2uijgpb8tILz7Ys9Q48KbmmfHDSpjK&callback=renderReverse&location=%s,%s&output=json&pois=0" % (
            baidu_position[1], baidu_position[0])
            proxies={'https':'116.209.56.118:9999'}
            req = requests.get(baiduUrl,proxies=proxies,timeout=10)
            content = req.text
            content = content.replace("renderReverse&&renderReverse(", "")
            content = content[:-1]
#             print(content)
            baiduAddr = json.loads(content)
            province = baiduAddr["result"]["addressComponent"]["province"]
            city = baiduAddr["result"]["addressComponent"]["city"]
            district = baiduAddr["result"]["addressComponent"]["district"]
            street=baiduAddr["result"]["addressComponent"]["street"]
            # 写入2.txt文件
            new_line =  province + "|" + city + "|" + district
            print(new_line)
            if '省' in province :
                province=province.replace('省','')
            if '市' in city:
                city=city.replace('市','')
            City.append(city)
            District.append(district)
            Street.append(street)
        df2['province']=Province
        df2['city']=City
        df2['district']=District
        df2['street']=Street
        df2.to_csv(rusult3_data+file,encoding='utf-8')
#             location=do_geocode(geolocator,str(i['lat'])+','+str(i['lng']))
#             print(location.address)
            
        
    
#         df1 = pd.concat([df1,df2],axis=0,ignore_index=True)  #将df2数据与df1合并
#     df1.to_csv(rusult3_data+ 'total.csv',encoding='utf-8') #将结果保存为新的csv文件
if __name__ == '__main__':
    weather_data=pd.read_csv('../Result/result3/weather_data.csv',encoding='utf-8')
    print(weather_data['province'].unique())
    geolocator = Nominatim()
    gpsConvert=GpsConvert.GpsConvert()
    merge_file(geolocator,gpsConvert)
    

        