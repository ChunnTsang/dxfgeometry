# -*-coding:utf-8 -*-
"""
# Time  : 2026/1/20
# Author: ChunTsang <zjun5566@163.com>
"""

from dxfgeometry.parser import read_dxf_to_geometry
from dxfgeometry.json_geometry.json_cad_result import JsonCADReadResult, json_cad_read_result_to_object
from dxfgeometry.util.tools import save_json_file


if __name__ == '__main__':
    # Read DXF File
    dxf_file_path = 'demo_file.dxf'
    cad_read_result = read_dxf_to_geometry(dxf_file_path)

    # Export to JSON File
    json_result = JsonCADReadResult(cad_read_result)
    save_json_file(json_result, 'result.json')

    # Reload saved JSON File
    with open('result.json', 'r', encoding='utf-8') as f:
        cad_read_result = json_cad_read_result_to_object(f.read())

