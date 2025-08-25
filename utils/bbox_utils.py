# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 13:24:23 2024

@author: PC_DHIA
"""
import numpy as np
def find_center(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return (x2+x1)/2,(y2+y1)/2

def find_distance (p1,p2):
    return np.sqrt(((p2[0]-p1[0])**2)+((p2[1]-p1[1])**2))

def calcul_foot(bbox):
    return (((bbox[0]+bbox[2])/2),bbox[3])

def calcul_position(p1,p2):
    return abs(p1[0]-p2[0]), abs(p1[1]-p2[1])
def get_height_of_bbox(bbox):
    return bbox[3]-bbox[1]

