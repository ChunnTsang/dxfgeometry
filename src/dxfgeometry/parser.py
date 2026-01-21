# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/19
# Author: ChunTsang <zjun5566@163.com>
"""

import ezdxf
import math
import logging
from shapely.geometry import LineString as ShapelyLineString
from util.color import get_layer_color
from geometry.arc import Arc
from geometry.ellipse import Ellipse
from geometry.circle import Circle
from geometry.text import Text
from geometry.hatch import Hatch
from geometry.ortho_hatch import OrthoHatch
from geometry.line import Line
from geometry.point import Point
from geometry.cad_layer import CADLayer
from geometry.polyline import Polyline
from geometry.polygon import Polygon
from geometry.ortho_polygon import OrthoPolygon
from geometry.cad_result import CADReadResult
from exception.reader_exception import ReadElementException, handle_exception
from exception.polygon_exception import PolygonAngleException, PolygonTinyAreaException
from json_geometry.json_cad_layer import JsonCADLayer


def read_dxf_to_geometry(dxf_file_path: str) -> CADReadResult:
    doc = ezdxf.readfile(dxf_file_path)
    layers_color = get_layer_color(doc)
    msp = doc.modelspace()

    group: dict = msp.groupby(dxfattrib='layer')
    layers_to_read = []
    existing_angle_list = []
    layer_dict: dict[str, CADLayer] = {}
    element_with_exception: dict[str, list[ReadElementException]] = {}

    for layer_name in list(group.keys()):
        if layer_name in group:
            layers_to_read.append((layer_name, group[layer_name]))

    while len(layers_to_read) > 0:
        next_layer_name, next_layer = layers_to_read[0]
        color = layers_color[next_layer_name]
        new_layer_list = parse_layer(next_layer, next_layer_name, layer_dict, existing_angle_list,
                                     element_with_exception, color)
        layers_to_read.pop(0)
        layers_to_read += new_layer_list

    return CADReadResult(dxf_file_path, layer_dict, existing_angle_list)


def parse_layer(layer, layer_name: str, layer_dict: dict[str, CADLayer], existing_angle_list: list[float],
                element_with_exception: dict[str, list[ReadElementException]], color: str):
    layer_dict.setdefault(layer_name, CADLayer(layer_name, color))
    element_with_exception.setdefault(layer_name, [])

    new_layer_list: list[tuple[str, CADLayer]] = []
    for new_element in layer:
        if new_element.dxftype() == 'LWPOLYLINE' or new_element.dxftype() == 'POLYLINE':
            authentic_is_closed = new_element.is_closed
            point_list = list(new_element.vertices_in_wcs())
            if (point_list[0][0] - point_list[-1][0]) ** 2 + (point_list[0][1] - point_list[-1][1]) ** 2 < 10:
                authentic_is_closed = True
            parse_polyline(point_list, layer_dict, layer_name, existing_angle_list, element_with_exception,
                           authentic_is_closed)

        elif new_element.dxftype() == 'LINE':
            try:
                layer_dict.get(layer_name).add_line(Line(new_element.dxf.start[0], new_element.dxf.start[1],
                                                    new_element.dxf.end[0], new_element.dxf.end[1],
                                                    layer_name, existing_angle_list))
            except ValueError as e:
                handle_exception(e, [[new_element.dxf.start[0], new_element.dxf.start[1]],
                                     [new_element.dxf.end[0], new_element.dxf.end[1]]],
                                 element_with_exception[layer_name])
                continue

        elif new_element.dxftype() == 'POINT':
            layer_dict.get(layer_name).add_point(Point(new_element.dxf.location[0], new_element.dxf.location[1],
                                                       layer_name))

        elif new_element.dxftype() == 'HATCH':
            for path in new_element.paths.paths:
                point_list: list[list[float]] = []
                if isinstance(path, ezdxf.entities.PolylinePath):
                    for vertices in path.vertices:
                        point_list.append([vertices[0], vertices[1]])
                elif isinstance(path, ezdxf.entities.EdgePath):
                    edge_list = path.edges
                    for edge in edge_list:
                        if isinstance(edge, ezdxf.entities.LineEdge):
                            x, y = edge.start
                            point_list.append([x, y])
                        else:
                            logging.warning("暂不支持: %s", type(edge))
                            continue
                if len(point_list) == 0:
                    continue
                try:
                    layer_dict.get(layer_name).add_ortho_hatch(
                        OrthoHatch(point_list, layer_name, new_element.dxf.pattern_name, existing_angle_list))
                except PolygonAngleException:
                    try:
                        hatch = Hatch(point_list, layer_name, new_element.dxf.pattern_name, existing_angle_list)
                        layer_dict.get(layer_name).add_hatch(hatch)
                    except Exception as e:
                        handle_exception(e, point_list, element_with_exception[layer_name])
                        continue
                except Exception as e:
                    handle_exception(e, point_list, element_with_exception[layer_name])
                    continue

        elif new_element.dxftype() == 'TEXT' or new_element.dxftype() == 'MTEXT':
            anchor_point_list: list[list[float]] = [[new_element.dxf.insert[0], new_element.dxf.insert[1]]]
            if new_element.dxftype() == 'TEXT':
                content_text: str = new_element.dxf.text
                if new_element.dxf.align_point is not None:
                    anchor_point_list.append([new_element.dxf.align_point[0], new_element.dxf.align_point[1]])
                angle: float = - round(new_element.dxf.rotation + 90, 10)
                while angle >= 180:
                    angle = angle - 180
                while angle < 0:
                    angle = angle + 180
                width = max(new_element.dxf.width, 0.1)
                text = Text(anchor_point_list, layer_name, content_text, angle, width,
                            new_element.dxf.height, existing_angle_list)
                layer_dict.get(layer_name).add_text(text)

            elif new_element.dxftype() == 'MTEXT':
                content_text: str = new_element.plain_text()
                text_x = new_element.dxf.text_direction[0]
                text_y = new_element.dxf.text_direction[1]
                cos_theta = text_x / ((text_x ** 2 + text_y ** 2) ** 0.5)
                if abs(abs(cos_theta) - 1) < 0.01:
                    text = Text(anchor_point_list, layer_name, content_text, 90, new_element.dxf.width,
                                new_element.dxf.char_height, existing_angle_list)
                else:
                    angle = round(
                        math.atan(new_element.dxf.text_direction[0] / new_element.dxf.text_direction[1]) * 57.2958, 10)
                    while angle >= 180:
                        angle = angle - 180
                    while angle < 0:
                        angle = angle + 180
                    width = max(new_element.dxf.width, 0.1)
                    text = Text(anchor_point_list, layer_name, content_text, angle, width,
                                new_element.dxf.char_height, existing_angle_list)
                layer_dict.get(layer_name).add_text(text)

        elif new_element.dxftype() == 'INSERT':
            try:
                new_msp = new_element.explode().groupby('layer')
            except Exception as _:
                continue
            for new_layer_name in new_msp.keys():
                new_layer_list.append((new_layer_name, new_msp[new_layer_name]))

        elif new_element.dxftype() == "DIMENSION":
            try:
                new_msp = new_element.explode().groupby('layer')
            except Exception as e:
                continue
            for new_layer_name in new_msp.keys():
                new_layer_list.append((layer_name, new_msp[new_layer_name]))

        elif new_element.dxftype() == "CIRCLE":
            coord_x: int = new_element.dxf.center[0]
            coord_y: int = new_element.dxf.center[1]
            radius: int = new_element.dxf.radius
            layer_dict.get(layer_name).add_circle(Circle(coord_x, coord_y, radius, layer_name))

        elif new_element.dxftype() == "ARC":
            center_x: float = new_element.dxf.center[0]
            center_y: float = new_element.dxf.center[1]
            radius: float = new_element.dxf.radius
            start_angle: float = new_element.dxf.start_angle
            end_angle: float = new_element.dxf.end_angle
            layer_dict.get(layer_name).add_arc(Arc(center_x, center_y, start_angle, end_angle, radius, layer_name))

        elif new_element.dxftype() == "ELLIPSE":
            center_x: float = new_element.dxf.center[0]
            center_y: float = new_element.dxf.center[1]
            major_axis = new_element.dxf.major_axis
            major_angle = get_line_angle(ShapelyLineString([(0, 0), (major_axis[0], major_axis[1])]))
            ratio: float = new_element.dxf.ratio

            start_param: float = new_element.dxf.start_param
            end_param: float = new_element.dxf.end_param

            layer_dict.get(layer_name).add_ellipse(Ellipse(center_x, center_y, start_param, end_param,
                                                           major_axis, ratio, layer_name))
            equal_radius = math.sqrt(ratio * major_axis.magnitude * major_axis.magnitude)
            if new_element.dxf.extrusion[2] >= 0:
                start_angle: float = start_param / math.pi * 180 + major_angle
                end_angle: float = end_param / math.pi * 180 + major_angle
            else:
                start_angle: float = major_angle - end_param / math.pi * 180
                end_angle: float = major_angle - start_param / math.pi * 180
            if start_angle <= 0:
                start_angle += 360
            if end_angle <= 0:
                end_angle += 360

            layer_dict.get(layer_name).add_arc(Arc(center_x, center_y, start_angle, end_angle, equal_radius,
                                                   layer_name))

        else:
            logging.warning(f"parse_layer(): 暂不支持该格式: {new_element.dxftype()} {layer_name}")

    return new_layer_list


def parse_polyline(point_list: list[list[float]], layer_dict: dict[str, CADLayer], layer_name: str,
                   existing_angle_list: list[float], element_with_exception: dict[str, list[ReadElementException]],
                   is_enclosed: bool):
    if is_enclosed:
        try:
            layer_dict.get(layer_name).add_ortho_polygon(OrthoPolygon(point_list, layer_name, existing_angle_list))
        except PolygonTinyAreaException as e:
            handle_exception(e, point_list, element_with_exception[layer_name])
            return
        except PolygonAngleException as e:
            layer_dict.get(layer_name).add_polygon(Polygon(point_list, layer_name, existing_angle_list))
        except Exception as e:
            handle_exception(e, point_list, element_with_exception[layer_name])
            return
    else:
        if len(point_list) == 2:
            try:
                layer_dict.get(layer_name).add_line(Line(point_list[0][0], point_list[0][1],
                                                         point_list[1][0], point_list[1][1],
                                                         layer_name, existing_angle_list))
            except Exception as e:
                handle_exception(e, point_list, element_with_exception[layer_name])
                return
        else:
            polyline_point_list: list[list[float]] = []
            for point in point_list:
                polyline_point_list.append([point[0], point[1]])
            try:
                layer_dict.get(layer_name).add_polyline(Polyline(polyline_point_list, layer_name, existing_angle_list))
            except Exception as e:
                handle_exception(e, polyline_point_list, element_with_exception[layer_name])
                return


def get_line_angle(line: ShapelyLineString):
    x1, y1 = line.coords[0]
    x2, y2 = line.coords[-1]
    dx = x2 - x1
    dy = y2 - y1
    angle = math.atan2(dy, dx)
    return math.degrees(angle)

