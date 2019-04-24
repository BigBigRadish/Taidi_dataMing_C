# -*- coding: utf-8 -*-
'''
Created on 2019年4月24日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
#解析osm数据
import os
import datetime
import pandas as pd
import time

#poi 查询
# import reverse_geocode
# coordinates = (0.0, 144.96)
# reverse_geocode.search(coordinates)
import json
from lxml import etree
import xmltodict

def iter_element(file_parsed, file_length, file_write):
    current_line = 0
    try:
        for event, element in file_parsed:
            current_line += 1
            print(current_line/float(file_length))
            elem_data = etree.tostring(element)
            elem_dict = xmltodict.parse(elem_data, attr_prefix="", cdata_key="")
            if (element.tag == "node"):
                elem_jsonStr = json.dumps(elem_dict["node"])
                file_write.write(elem_jsonStr + "\n")
            # 每次读取之后进行一次清空
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    except:
        pass

if __name__ == '__main__':
    osmfile = r'E:/china-latest.osm'

    file_length = -1
    for file_length, line in enumerate(open(osmfile, 'r',encoding='utf-8')):
        pass
    file_length += 1
    print ("length of the file:\t" + str(file_length))

    file_node = open(osmfile+"_node.json","a")
    file_parsed = etree.iterparse(osmfile, tag=["node"])
    iter_element(file_parsed, file_length, file_node)
    file_node.close()

