# -*- coding: utf-8 -*-
'''
Created on 2019年4月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#osmnx使用教程
import osmnx as ox
city=ox.gdf_from_place("南山区,深圳市,中国")
print(city)