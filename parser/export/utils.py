import numpy as np
import math


def get_point_in_range(objects, x, y, range=0.1):
    points_found = []
    for obj in objects:
        if abs(obj.x0 - x) <= range and  abs(obj.y0 - y) <= range:
            points_found.append([obj.x0, obj.y0, obj])
        if abs(obj.x1 - x) <= range and  abs(obj.y1 - y) <= range:
            points_found.append([obj.x1, obj.y1, obj])

        
    return points_found
