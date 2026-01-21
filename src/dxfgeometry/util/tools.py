# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""
import math
from typing import Optional
from shapely.geometry import Polygon as ShapelyPolygon
import numpy as np
from src.dxfgeometry.config import default_point_precision, default_angle_precision, default_min_angle_difference
from src.dxfgeometry.json_geometry.json_base_class import Jsonable


def calculate_distance(point1: Optional[list], point2: list):
    if point1 is None:
        return float('inf')
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    return round(distance, default_point_precision)


def simplify_polygon_vertices(points):
    poly = ShapelyPolygon(points)
    boundary = poly.exterior
    coords = list(boundary.coords)
    coords = coords[:-1]

    vertices = []
    for i in range(len(coords)):
        prev = coords[i - 1]
        curr = coords[i]
        next_point = coords[(i + 1) % len(coords)]
        vector1 = np.array([curr[0] - prev[0], curr[1] - prev[1]])
        vector2 = np.array([next_point[0] - curr[0], next_point[1] - curr[1]])
        if not is_collinear(vector1, vector2):
            vertices.append(list(curr))
    return vertices


def is_collinear(vector1, vector2):
    cross_product = np.cross(vector1, vector2)
    return abs(cross_product) < 1e-10


def get_angle(x1, y1, x2, y2) -> float:
    x1, y1 = round(x1, default_point_precision), round(y1, default_point_precision)
    x2, y2 = round(x2, default_point_precision), round(y2, default_point_precision)
    if x1 == x2 and y1 == y2:
        raise ValueError("Line初始化错误，两个点坐标相同", x1, x2)

    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    if x1 == x2:
        return 0.0
    else:
        k = (y2 - y1) / (x2 - x1)
        angle = 90.0 - math.atan(k) * 180.0 / math.pi
        if abs(angle - 180) < default_min_angle_difference:
            angle = 0.0
        return round(angle, default_angle_precision)


def get_rect_mid_point(point_list: list[list[float]]):
    return [calculate_mid_point(point_list[-1 + i], point_list[i]) for i in range(len(point_list))]


def calculate_mid_point(point1: list[float], point2: list[float]):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    return [(x1 + x2) / 2, (y1 + y2) / 2]


def save_json_file(json_object: Jsonable, json_file_dir: str):
    with open(json_file_dir, 'w') as f:
        json_object.save_to_file(f)
    print(f">>>>>> Saved in '{json_file_dir}' <<<<<<")
