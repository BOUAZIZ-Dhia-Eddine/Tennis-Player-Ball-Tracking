# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 00:31:22 2024

@author: PC_DHIA
"""

def convert_from_pixel_to_metre(dimension_pixel,donner_en_pixel=210,donner_en_metre=10.97):
    return((dimension_pixel*donner_en_metre)/donner_en_pixel)

def convert_from_metre_to_pixel(dimension_metre,donner_en_pixel=210,donner_en_metre=10.97):
    return((dimension_metre*donner_en_pixel)/donner_en_metre)
def convert_pixel_distance_to_meters(pixel_distance, refrence_height_in_meters, refrence_height_in_pixels):
    return (pixel_distance * refrence_height_in_meters) / refrence_height_in_pixels

def convert_meters_to_pixel_distance(meters, refrence_height_in_meters, refrence_height_in_pixels):
    return (meters * refrence_height_in_pixels) / refrence_height_in_meters