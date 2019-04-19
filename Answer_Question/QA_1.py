# -*- coding: utf-8 -*-
'''
Created on 2019年3月29日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
'''
第一题
(1) 利用附件 1 所给数据，提取并分析车辆的运输路线以及其在运输过程中的速度、加 速度等行车状态。
提交附表中 10 辆车每辆车每条线路在经纬度坐标系下的运输线路图及对 应的行车里程、平均行车速度、急加速急减速情况。 
'''
#dbscan gps聚类
import pandas as pd
import numpy as np
import os
import matplotlib
# df_min=pd.read_csv('../data/train_100/AA00052.csv')
# # represent GPS points as (lat, lon)
# coords = df_min.as_matrix(columns=['lat', 'lng'])
# 
# # # earth's radius in km
# kms_per_radian = 6371.0088
# # define epsilon as 0.5 kilometers, converted to radians for use by haversine
# epsilon = 0.5 / kms_per_radian
# 
# # eps is the max distance that points can be from each other to be considered in a cluster
# # min_samples is the minimum cluster size (everything else is classified as noise)
# db = DBSCAN(eps=epsilon, min_samples=100, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
def plot_route_map():
    # cluster_labels = db.labels_
    import geopy.distance
    from dipy.segment.metric import Metric
    from dipy.segment.metric import ResampleFeature
    import gmplot
    #declare the center of the map, and how much we want the map zoomed in
    cluster_plot_file='../Result/result1/tr_train_100'#分组之后的路线数据
    route_map='../Result/result1/route_map/'#每辆车的路线图
    list1 = os.listdir(cluster_plot_file)
    print(list1)
    colors=[]
    for name, hex in matplotlib.colors.cnames.items():
        colors.append(name)#颜色列表
    print(colors)
    '''
    ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 
    'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblu
    e', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson',
     'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'dark
    grey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid',
     'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'dar
    kslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray'
    , 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia',
     'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow',
     'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavend
    er', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'l
    ightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'ligh
    tpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'light
    slategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'mage
    nta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple'
    , 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', '
    mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajow
    hite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid',
     'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', '
    peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 're
    d', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen',
     'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey
    ', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turq
    uoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
    '''
    n=0
    for i in list1[172:174]:
        n+=1
        partition_df=pd.read_csv(cluster_plot_file+'/'+i)
        partition_df=partition_df[partition_df['labels']!=-1].reset_index()
        print(partition_df)
        gmap = gmplot.GoogleMapPlotter(partition_df.lat[0], partition_df.lng[0],11,apikey='AIzaSyBPAXdx0-ZoxDaa8pGK5YIP6TcuEDwwYWA')
        for j in partition_df['labels'].unique():
            label_partition_df=partition_df[partition_df['labels']==j]
    #         gmap = gmplot.GoogleMapPlotter(label_partition_df.lat[label_partition_df.keys()[0]], label_partition_df.lng[label_partition_df.keys()[0]],11,apikey='AIzaSyBPAXdx0-ZoxDaa8pGK5YIP6TcuEDwwYWA')    
    # print(df_min)
            gmap.plot(label_partition_df.lat, label_partition_df.lng,color=colors[j],edge_width=5)
        gmap.draw(route_map+i.replace('csv','html'))
#求总里程以及平均速度
def sum_mile_average():
    tr_train='../Result/result1/tr_train_100/'
    route_details='../Result/result1/routes_details/'
    tr_train_files=os.listdir(tr_train)
    routes=[]#路线名
    sum_miles=[]#总里程
    avr_v=[]#平均速度
    acc_times=[]#急加速急减速次数
    cars=[]#车辆号
    for i in tr_train_files:
        partition_df=pd.read_csv(tr_train+i)
        gps_speed=partition_df['gps_speed']
        unix_time=partition_df['unix_time']
        len_gps_speed=len(gps_speed)
        acc_speed=[]
        for n in range(0,len_gps_speed):
            if n+1<len_gps_speed and (int(unix_time[n+1])>=int(unix_time[n])+3) :
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
                
        partition_df['acc_speed']=acc_speed#加速度列
        partition_df=partition_df[partition_df['labels']!=-1].reset_index()
        print(partition_df)
        labels=partition_df['labels'].unique()
        
        for j in labels:
            cars.append(i)
            routes.append('route'+str(j))#路线名
            label_partition_df=partition_df[partition_df['labels']==j]
            miles=label_partition_df['mileage']
            mile=miles.values[-1]-miles.values[0]
            sum_miles.append(mile)#分段总里程
            partition_gps_speeds=label_partition_df[label_partition_df['gps_speed']!=0]['gps_speed']
            if len(partition_gps_speeds)!=0:
                avr_v.append(float(sum(partition_gps_speeds))/len(partition_gps_speeds) )#平均速度
            else:
                avr_v.append(0)
            acc_vs=label_partition_df[label_partition_df['acc_speed']>=2.22]
            acc_times.append(len(acc_vs))#急加速次数
    data = {
            'cars':cars,\
            'routes':routes,\
            'sum_miles':sum_miles,\
            'avr_v':avr_v,\
            'acc_times':acc_times
            }
    car_route_cond=pd.DataFrame(data)
    car_route_cond.to_csv(route_details+i)
        
            
            
def add_acc_v():#求加速度
    tr_train='../Result/result1/tr_train_100/'
    tr_train_files=os.listdir(tr_train)
    for i in tr_train_files[0:1]:
        partition_df=pd.read_csv(tr_train+i)
        print(partition_df)
        gps_speed=partition_df['gps_speed']
        len_gps_speed=len(gps_speed)
        acc_speed=[]
        for i in range(0,len_gps_speed):
            if i+1<len_gps_speed and gps_speed[i]!=0 :
                acc_speed.append(float(gps_speed[i+1])/gps_speed[i])
            else:
                acc_speed.append(0) 
        print(len(acc_speed))
if __name__ == '__main__':
#     add_acc_v()
    sum_mile_average()
    
                
            
            
        
    
