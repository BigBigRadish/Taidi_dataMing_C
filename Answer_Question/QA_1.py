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
# cluster_labels = db.labels_
import geopy.distance
from dipy.segment.metric import Metric
from dipy.segment.metric import ResampleFeature
import gmplot
#declare the center of the map, and how much we want the map zoomed in
cluster_plot_file='../Result/result1/tr_train_100'
route_map='../Result/result1/route_map/'
list1 = os.listdir(cluster_plot_file)
print(list1)
for i in list1:
    partition_df=pd.read_csv(cluster_plot_file+'/'+i)
    partition_df=partition_df[partition_df['labels']!=-1].reset_index()
    print(partition_df)
    gmap = gmplot.GoogleMapPlotter(partition_df.lat[0], partition_df.lng[0],11,apikey='AIzaSyBPAXdx0-ZoxDaa8pGK5YIP6TcuEDwwYWA')
    for j in partition_df['labels'].unique():
        label_partition_df=partition_df[partition_df['labels']==j]
#         gmap = gmplot.GoogleMapPlotter(label_partition_df.lat[label_partition_df.keys()[0]], label_partition_df.lng[label_partition_df.keys()[0]],11,apikey='AIzaSyBPAXdx0-ZoxDaa8pGK5YIP6TcuEDwwYWA')    
# print(df_min)
        gmap.plot(label_partition_df.lat, label_partition_df.lng,color='red')
    gmap.draw(route_map+i.replace('csv','html'))

