# -*- coding: utf-8 -*-
'''
Created on 2019年4月15日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import os
# from pandarallel import pandarallel#numpy 版本问题，弃用
import pandas as pd
import pyproj
#数据去重
def drop_dup():
    raw_path='../data/train_100'
    drop_dup_path='../data/dd_train_100'
    list = os.listdir(raw_path)
    print(list)
    for i in list:
        raw_df=pd.read_csv(raw_path+'/'+i)
        print(raw_df.size)
        new_df=raw_df.drop_duplicates(subset=['lng','lat','mileage'])
        new_df.to_csv(drop_dup_path+'/'+i,encoding='utf-8',index=False)
# drop_dup()
# 投影变换
def proj_trans(ln_la_dir,file):
    # 读取经纬度
    
    data = pd.read_csv('../data/dd_train_100'+'/'+file)
    lng = data.lng.values
    lat = data.lat.values
    print(lng, lat)
    p1 = pyproj.Proj(init="epsg:4326")# 定义数据地理坐标系
    p2 = pyproj.Proj(init="epsg:3857")# 定义转换投影坐标系
    x1, y1 = p1(lng, lat)
    x2, y2 = pyproj.transform(p1, p2, x1, y1, radians=True)
    print(x2,y2)
    data['lng_x']=x2
    data['lat_y']=y2
    data.to_csv(ln_la_dir+'/'+file,encoding='utf-8',index=False)
if __name__ == '__main__':
    dd_train_100='../data/dd_train_100'
    la_ln_dd_train_100='../data/la_ln_dd_train_100'#转换为平面坐标的文件夹
    dd_files=os.listdir(dd_train_100)
    for i in dd_files:
        proj_trans(la_ln_dd_train_100,i)
        
    
    


        
    

