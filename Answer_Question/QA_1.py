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
from sklearn.cluster import DBSCAN
from sklearn import metrics
import pandas as pd
import numpy as np
df_min=pd.read_csv('../data/train_100/AA00001.csv')
# represent GPS points as (lat, lon)
coords = df_min.as_matrix(columns=['lat', 'lng'])

# earth's radius in km
kms_per_radian = 6371.0088
# define epsilon as 0.5 kilometers, converted to radians for use by haversine
epsilon = 0.5 / kms_per_radian

# eps is the max distance that points can be from each other to be considered in a cluster
# min_samples is the minimum cluster size (everything else is classified as noise)
db = DBSCAN(eps=epsilon, min_samples=100, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
cluster_labels = db.labels_
# get the number of clusters (ignore noisy samples which are given the label -1)
num_clusters = len(set(cluster_labels) - set([-1]))

print ('Clustered ' + str(len(df_min)) + ' points to ' + str(num_clusters) + ' clusters')

# turn the clusters in to a pandas series
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
print(clusters)

import matplotlib.pyplot as plt
from shapely.geometry import MultiPoint
from geopy.distance import great_circle
def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)

# get the centroid point for each cluster
centermost_points = clusters.map(get_centermost_point)
lats, lons = zip(*centermost_points)
rep_points = pd.DataFrame({'lon':lons, 'lat':lats})

fig, ax = plt.subplots(figsize=[10, 6])
rs_scatter = ax.scatter(rep_points['lon'][0], rep_points['lat'][0], c='#99cc99', edgecolor='None', alpha=0.7, s=450)
ax.scatter(rep_points['lon'][1], rep_points['lat'][1], c='#99cc99', edgecolor='None', alpha=0.7, s=250)
ax.scatter(rep_points['lon'][2], rep_points['lat'][2], c='#99cc99', edgecolor='None', alpha=0.7, s=250)
ax.scatter(rep_points['lon'][3], rep_points['lat'][3], c='#99cc99', edgecolor='None', alpha=0.7, s=150)
df_scatter = ax.scatter(df_min['lng'], df_min['lat'], c='k', alpha=0.9, s=3)
ax.set_title('Full GPS trace vs. DBSCAN clusters')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend([df_scatter, rs_scatter], ['GPS points', 'Cluster centers'], loc='upper right')

labels = ['cluster{0}'.format(i) for i in range(1, num_clusters+1)]
for label, x, y in zip(labels, rep_points['lon'], rep_points['lat']):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (-25, -30),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

plt.show()

