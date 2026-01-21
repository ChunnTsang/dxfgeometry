# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from src.dxfgeometry.json_geometry.json_cad_element import JsonCADElement
from src.dxfgeometry.geometry.ellipse import Ellipse
from ezdxf.math import Vec3


class JsonEllipse(JsonCADElement):
    x: float
    y: float
    start_param: float
    end_param: float
    major_axis: any
    ratio: float
    radius: float
    xfact: float
    yfact: float

    def __init__(self, ellipse: Ellipse):
        super(JsonEllipse, self).__init__(ellipse.get_layer_name(), 'Ellipse')
        self.x = ellipse.get_x()
        self.y = ellipse.get_y()
        self.start_param = ellipse.get_start_param()
        self.end_param = ellipse.get_end_param()
        self.major_axis = [ellipse.get_major_axis().x, ellipse.get_major_axis().y, ellipse.get_major_axis().z]
        self.ratio = ellipse.get_ratio()
        self.radius = ellipse.get_radius()
        self.xfact = ellipse.get_xfact()
        self.yfact = ellipse.get_yfact()
        self.electric_info = {}

    def __setitem__(self, key, value):
        self.electric_info[key] = value


def json_ellipse_to_ellipse(json_ellipse: dict) -> Ellipse:
    v = Vec3(json_ellipse['major_axis'][0], json_ellipse['major_axis'][1], json_ellipse['major_axis'][2])
    return Ellipse(json_ellipse['x'], json_ellipse['y'], json_ellipse['start_param'], json_ellipse['end_param'],
                   v, json_ellipse['ratio'], json_ellipse['layer_name'])
