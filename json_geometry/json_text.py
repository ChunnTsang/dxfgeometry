# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from json_geometry.json_cad_element import JsonCADElement
from geometry.text import Text


class JsonText(JsonCADElement):
    angle: float
    content: str
    anchor_point_list: list[list[float]]
    points: list[float]
    height: float
    width: float

    def __init__(self, text: Text):
        super(JsonText, self).__init__(text.get_layer_name(), "Text")
        self.angle = text.get_angle().get_angle()
        self.content = text.get_content()
        self.anchor_point_list = text.get_anchor_point_list()
        self.width = text.get_width()
        self.height = text.get_height()
        self.points = []
        for point in text.get_anchor_point_list():
            self.points.append(point[0])
            self.points.append(point[1])


def json_text_to_text(json_text, existing_angle_list: list[float]) -> Text:
    width = json_text["width"] if "width" in json_text and json_text["width"] is not None else 0
    height = json_text["height"] if "height" in json_text and json_text["height"] is not None else 0
    return Text(json_text["anchor_point_list"], json_text["layer_name"], json_text["content"], json_text["angle"],
                width, height, existing_angle_list)

