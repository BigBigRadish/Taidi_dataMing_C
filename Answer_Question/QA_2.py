# -*- coding: utf-8 -*-
'''
Created on 2019年3月29日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
'''
第二题
(2) 利用附件 1 所给数据，挖掘每辆运输车辆的不良驾驶行为，建立行车安全的评价模 型，并给出评价结果。 
'''
import os
import pandas as pd
import time,datetime
def datatime_2_unixtime( dtime):
    ans_time = time.mktime(datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S").timetuple())
    return ans_time
#大于等于45分钟为疲劳驾驶
def tierd_drive():
    dd_train='../data/dd_train_100/'#只使用去重之后的数据
    dd_train_files=os.listdir(dd_train)
    for i in dd_train_files:
        raw_df=pd.read_csv(dd_train+i)
        raw_df['unix_time']=raw_df['location_time'].apply(datatime_2_unixtime)#转换成unix时间
        gps_speed=raw_df['gps_speed']
        unix_time=raw_df['unix_time']
        len_gps_speed=len(gps_speed)
        acc_speed=[]
        for n in range(0,len_gps_speed):
            if n+1<len_gps_speed and (int(unix_time[n+1])>=int(unix_time[n])+3) :#计算加速度
                if gps_speed[n]!=0 :
                    acc_speed.append(abs((float(gps_speed[n+1])-gps_speed[n])*1000/3600/(unix_time[n+1]-unix_time[n])))
                else:
                    acc_speed.append(0)
            elif n+2<len_gps_speed and (unix_time[n+2]>=unix_time[n]+3):
                if gps_speed[n]!=0 :
                    acc_speed.append(abs((float(gps_speed[n+2])-gps_speed[n])*1000/3600/(unix_time[n+2]-unix_time[n])))
                else:
                    acc_speed.append(0)
            else:
                if n+3<len_gps_speed and gps_speed[n]!=0 :
                    acc_speed.append(abs((float(gps_speed[n+3])-gps_speed[n])*1000/3600/(unix_time[n+3]-unix_time[n])))
                else:
                    acc_speed.append(0)
        raw_df['acc_speed']=acc_speed#加速度列
        raw_df.to_csv('../Result/result2/rw_train/'+i,index=False,encoding='utf-8')
        start_run_area=[]#运行索引
        stop_run_area=[]#停止运行索引
        n=0
        for index in range(0,len_gps_speed-1):
            if gps_speed[index+1]!=0 and gps_speed[index]==0:
                    start_run_area.append(index+1)
            elif gps_speed[index+1]==0 and gps_speed[index]!=0:
                    stop_run_area.append(index)     
            else:
                continue
        print(start_run_area,stop_run_area)
        len_start_run,len_stop_run=len(start_run_area),len(stop_run_area)
        tierd_flag=[]#疲劳标签
        initial_flag=0
        init_time=unix_time[start_run_area[0]]
        tierd_flag+=[0]*start_run_area[0]
        k=start_run_area[0]
        while(k<len_gps_speed):
#             if unix_time[k]-init_time<=4*60*60
            
            if k in stop_run_area:
                if (unix_time[start_run_area[stop_run_area.index(k)+1]-1]-unix_time[k]+1>45*60):
                    init_time= unix_time[start_run_area[stop_run_area.index(k)+1]-1]
                    initial_flag=0
            if (unix_time[k]-init_time>4*60*60):
                initial_flag=1
            print(initial_flag)
            tierd_flag.append(initial_flag)
            k+=1
        print(tierd_flag)
        raw_df['tierd_drive']=tierd_flag        
     
if __name__ == '__main__':
    tierd_drive()
            
                
                
            
            
            
    