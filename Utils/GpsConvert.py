# -*- coding: utf-8 -*-
'''
Created on 2019年3月29日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
import math
x_PI = 3.14159265358979324 * 3000.0 / 180.0
PI = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323   
class GpsConvert(object):
 
#    * BD-09：百度坐标系(百度地图)
#    * GCJ-02：火星坐标系（谷歌中国地图、高德地图）
#    * WGS84：地球坐标系（国际通用坐标系，谷歌地图）

    def __init__(self):
        pass
       

#百度坐标系转火星坐标系
    def bd09togcj02(self,bd_lon, bd_lat):
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_PI)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_PI)
        gcj_lon = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        gcj = [ gcj_lon, gcj_lat ]#火星坐标系值#火星坐标系转wgs84
        wgs = self.gcj02towgs84(gcj[0], gcj[1])
        return wgs
    def transformlon(self,lon, lat):
        ret = 300.0 + lon + 2.0 * lat + 0.1 * lon * lon + 0.1 * lon * lat + 0.1 * math.sqrt(math.fabs(lon))
        ret += (20.0 * math.sin(6.0 * lon * PI) + 20.0 * math.sin(2.0 * lon * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lon * PI) + 40.0 * math.sin(lon / 3.0 * PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lon / 12.0 * PI) + 300.0 * math.sin(lon / 30.0 * PI)) * 2.0 / 3.0
        return ret

    def transformlat(self,lon, lat):
        ret = -100.0 + 2.0 * lon + 3.0 * lat + 0.2 * lat * lat + 0.1 * lon * lat + 0.2 * math.sqrt(math.fabs(lon))
        ret += (20.0 * math.sin(6.0 * lon * PI) + 20.0 * math.sin(2.0 * lon * PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * PI) + 320 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
        return ret
#火星坐标系转wgs84
    def gcj02towgs84(self,gcj_lon, gcj_lat):
        if (self.out_of_china(gcj_lon, gcj_lat)):
#          //不在国内，不进行纠偏
            back = [ gcj_lon, gcj_lat ]
            return back
        else:
            dlon = transformlon(gcj_lon - 105.0, gcj_lat - 35.0)
            dlat = transformlat(gcj_lon - 105.0, gcj_lat - 35.0)
            radlat = gcj_lat / 180.0 * PI
            magic = math.sin(radlat)
            magic = 1 - ee * magic * magic
            sqrtmagic = math.sqrt(magic)
            dlon = (dlon * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
            dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
            mglon = gcj_lon + dlon
            mglat = gcj_lat + dlat
            wgs_lon = gcj_lon * 2 - mglon
            wgs_lat = gcj_lat * 2 - mglat
            wgs = [ wgs_lon, wgs_lat ]#wgs84坐标系值
            return wgs

#   //火星坐标系转百度坐标系
    def gcj02tobd09(self,gcj_lon, gcj_lat):
        z = math.sqrt(gcj_lon * gcj_lon + gcj_lat * gcj_lat) + 0.00002 * math.sin(gcj_lat * x_PI)
        theta = math.atan2(gcj_lat, gcj_lon) + 0.000003 * math.cos(gcj_lon * x_PI)
        bd_lon = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        bd = [ bd_lon, bd_lat ]
        return bd


#    //wgs84转火星坐标系
    def wgs84togcj02(self,wgs_lon, wgs_lat):
        if (self.out_of_china(wgs_lon, wgs_lat)):
            #//不在国内
            back = [ wgs_lon, wgs_lat ]
            return back
        else:
            dwgs_lon = self.transformlon(wgs_lon - 105.0, wgs_lat - 35.0)
            dwgs_lat = self.transformlat(wgs_lon - 105.0, wgs_lat - 35.0)
            radwgs_lat = wgs_lat / 180.0 * PI
            magic = math.sin(radwgs_lat)
            magic = 1 - ee * magic * magic
            sqrtmagic = math.sqrt(magic)
            dwgs_lon = (dwgs_lon * 180.0) / (a / sqrtmagic * math.cos(radwgs_lat) * PI)
            dwgs_lat = (dwgs_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
            gcj_lon = wgs_lon + dwgs_lon
            gcj_lat = wgs_lat + dwgs_lat
            gcj = [ gcj_lon, gcj_lat ]
            return gcj

#    //判断是否在国内，不在国内则不做偏移
    def out_of_china(self,lon, lat):
        return (lon < 72.004 or lon > 137.8347) or ((lat < 0.8293 or lat > 55.8271) or False)

