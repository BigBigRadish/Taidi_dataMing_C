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
        acc_speed=[]#加速度
        for n in range(0,len_gps_speed):
            if n+1<len_gps_speed and (int(unix_time[n+1])>=int(unix_time[n])+3) :#计算加速度
                if gps_speed[n]!=0 :
                    acc_speed.append((float(gps_speed[n+1])-gps_speed[n])*1000/3600/(unix_time[n+1]-unix_time[n]))
                else:
                    acc_speed.append(0)
            elif n+2<len_gps_speed and (unix_time[n+2]>=unix_time[n]+3):
                if gps_speed[n]!=0 :
                    acc_speed.append((float(gps_speed[n+2])-gps_speed[n])*1000/3600/(unix_time[n+2]-unix_time[n]))
                else:
                    acc_speed.append(0)
            else:
                if n+3<len_gps_speed and gps_speed[n]!=0 :
                    acc_speed.append((float(gps_speed[n+3])-gps_speed[n])*1000/3600/(unix_time[n+3]-unix_time[n]))
                else:
                    acc_speed.append(0)
        raw_df['acc_speed']=acc_speed#加速度列
        def acce_v( v):
            if(v>2.22):
                return 1
            else:
                return 0
        def dece_v(v):
            if(v<-2.22):
                return 1
            else: 
                return 0
        raw_df['acce']=raw_df['acc_speed'].apply(acce_v)#急加速
        raw_df['dece']=raw_df['acc_speed'].apply(dece_v)#急减速   
#         raw_df.to_csv('../Result/result2/rw_train/'+i,index=False,encoding='utf-8')
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
        if(len_start_run<=len_stop_run):
            stop_run_area=stop_run_area[0:len_start_run-1]
        tierd_flag=[]#疲劳标签
        initial_flag=0
        init_time=unix_time[start_run_area[0]]
        tierd_flag+=[0]*start_run_area[0]
        k=start_run_area[0]
        while(k<len_gps_speed):
#             if unix_time[k]-init_time<=4*60*60
            
            if k in stop_run_area :
                if (unix_time[start_run_area[stop_run_area.index(k)+1]-1]-unix_time[k+1]>45*60):
                    init_time= unix_time[start_run_area[stop_run_area.index(k)+1]-1]
                    initial_flag=0
            if (unix_time[k]-init_time>4*60*60):
                initial_flag=1
#             print(initial_flag)
            tierd_flag.append(initial_flag)
            k+=1
        print(tierd_flag)
        raw_df['tierd_drive']=tierd_flag#疲劳驾驶
        daisu=[]#怠速标签
        max_time_diasu=[]#超长怠速
        daisu+=[0]*start_run_area[0]#启动之前都默认为正常
        max_time_diasu+=[0]*start_run_area[0]
        k=start_run_area[0]
        while(k<len_gps_speed):
#             if unix_time[k]-init_time<=4*60*60
            
            if k in stop_run_area :
                if (5*60>=unix_time[start_run_area[stop_run_area.index(k)+1]-1]-unix_time[k+1]>=3*60):
                    daisu.append(1)
                else:
                    daisu.append(0)
                if (45*60>unix_time[start_run_area[stop_run_area.index(k)+1]-1]-unix_time[k+1]>5*60):
                    max_time_diasu.append(1)
                else:
                    max_time_diasu.append(0)
            else:
                daisu.append(0)
                max_time_diasu.append(0)
#             print(initial_flag)
            k+=1
        raw_df['daisu_hire']=daisu#怠速预热
        raw_df['max_daisu']=max_time_diasu#超长怠速
        #熄火滑行
        ac_st_huaxing=[]#熄火滑行列表
        acc_gps_df=raw_df[['acc_state','gps_speed','acc_speed']]
        for index,j in acc_gps_df.iterrows():
            if(j['acc_state']==0 and j['gps_speed']!=0 and j['acc_speed']<0):
                ac_st_huaxing.append(1)
            else:
                ac_st_huaxing.append(0)
        raw_df['off_flip']=ac_st_huaxing
        def over_speed(speed):#100km/h
            if speed>100*1000/3600:
                return 1
            else :
                return 0
        raw_df['over_speed']=raw_df['gps_speed'].apply(over_speed)          
        #急变道
        change_angle=[0]#改变角度
        direction_angle=raw_df['direction_angle']
        len_direction_angle=len(direction_angle)
        for c in  range(1,len_direction_angle):
            change_angle.append(abs(direction_angle[c]-direction_angle[c-1]))
        raw_df['change_angle']=change_angle
        ra_chag_ang=[]
        Rapid_change_road=raw_df[['change_angle','gps_speed']]
        for index,m in Rapid_change_road.iterrows():
            if(m['change_angle']>=10 and m['gps_speed']>50*1000/3600):
                ra_chag_ang.append(1)
            else:
                ra_chag_ang.append(0)
        raw_df['rapid_change_road']=ra_chag_ang
        scores=[]#危险分数
        for index,p in raw_df[['acce','dece','tierd_drive','daisu_hire','max_daisu','off_flip','over_speed','rapid_change_road']]:
            sum=0
            if(p['tierd_drive']==1):
                sum+=6
            if(p['over_speed']==1):
                sum+=3
            if(p['rapid_change_road']==1):
                sum+=2
            if(p['acc']==1 or p['dece']==1 or p['off_flip']==1):
                sum+=1
            if(p['daisu_hire']==1 or p['max_daisu']==1):
                sum+=0.5
            scores.append(sum)
        raw_df['danger_score']=scores  
        raw_df.to_csv('../Result/result2/rw_train/'+i,index=False,encoding='utf-8')
        
#急加速，急减速       
def Rapid_acceleration_deceleration():
    dd_train='../data/dd_train_100/'#只使用去重之后的数据
    dd_train_files=os.listdir(dd_train)
    for i in dd_train_files:
        raw_df=pd.read_csv(dd_train+i)
        gps_speed=raw_df['gps_speed']
        unix_time=raw_df['unix_time']
        len_gps_speed=len(gps_speed)
        acc_speed=[]#加速度
        for n in range(0,len_gps_speed):
            if n+1<len_gps_speed and (int(unix_time[n+1])>=int(unix_time[n])+3) :#计算加速度
                if gps_speed[n]!=0 :
                    acc_speed.append((float(gps_speed[n+1])-gps_speed[n])*1000/3600/(unix_time[n+1]-unix_time[n]))
                else:
                    acc_speed.append(0)
            elif n+2<len_gps_speed and (unix_time[n+2]>=unix_time[n]+3):
                if gps_speed[n]!=0 :
                    acc_speed.append((float(gps_speed[n+2])-gps_speed[n])*1000/3600/(unix_time[n+2]-unix_time[n]))
                else:
                    acc_speed.append(0)
            else:
                if n+3<len_gps_speed and gps_speed[n]!=0 :
                    acc_speed.append((float(gps_speed[n+3])-gps_speed[n])*1000/3600/(unix_time[n+3]-unix_time[n]))
                else:
                    acc_speed.append(0)
        raw_df['acc_speed']=acc_speed#加速度列
        def acce_v( v):
            if(v>2.22):
                return 1
            else:
                return 0
        def dece_v(v):
            if(v<-2.22):
                return 1
            else: 
                return 0
        raw_df['acce']=raw_df['acc_speed'].apply(acce_v)#急加速
        raw_df['dece']=raw_df['acc_speed'].apply(dece_v)#急减速   
        
# def acc_state():
    

if __name__ == '__main__':
    tierd_drive()
            
                
                
            
            
            
    