import numpy as np
import math
import draw.aed

class Point:
    def __init__(self, x, y, angle, obj, pos):
        self.id = f"{obj.id}-{pos}"
        self.x = x
        self.y = y
        self.angle = angle
        self.obj = obj
        self.pos = pos  # indicates where the note has been found (0 -> start of the line; 1 -> end of the line)

def get_points_in_range(objects, x, y, range=0.1):
    points_found = []
    for obj in objects:
        if isinstance(obj, draw.aed.CircularArcAED):
            continue  # these might be to complicated, esp. in roundabouts (TODO: Implement solution for this)
        else:
            pts = obj.get_points()
            for pt in pts:
                if abs(pt.x - x) <= range and  abs(pt.y - y) <= range:
                    points_found.append(pt)
    # if len(points_found) > 1:
    #     raise LookupError("More than 1 point found! Maybe decrese the range?")
    return points_found

def get_common_prefix(str1: str, str2: str):
    result = ""
    for c1, c2 in zip(str1, str2):
        if c1 == c2:
            result += c1
        else:
            break
    return result
