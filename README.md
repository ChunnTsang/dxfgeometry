# dxfgeometry

[![PyPI - Version](https://img.shields.io/badge/Pypi-v0.1.2-blue)](https://pypi.org/project/dxfgeometry/)
[![PyPI - Python Version](https://img.shields.io/badge/Python-3.10-blue)](https://pypi.org/project/dxfgeometry/)

**dxfgeometry** is a Python library for converting graphic data from `.dxf` CAD files into standard geometric data structures (such as polygons, lines, circles, etc.).

It traverses all layers in a CAD file and returns the results organized by "File → Layers → Data".

## Features

-  Parse DXF files and extract geometric primitives
-  Layer-based organization of geometric data
-  Convert CAD entities to Shapely geometries
-  Export all geometric elements to JSON format
-  Support for various primitive types (polygons, lines, circles, arcs, etc.)
-  Reload previously saved JSON files for further processing
-  Designed for architectural and BIM applications

## Installation
```bash
pip install dxfgeometry
```

## Quick Start
```python
from dxfgeometry.parser import read_dxf_to_geometry

# Read DXF file
result = read_dxf_to_geometry('your_file.dxf')

# Access data by layer
for layer_name, layer_data in result.get_layers():
    print(f"Layer: {layer_name}")
    print(f"Geometric set: {layer_data}")
```

## Requirements

- Python >= 3.10
- ezdxf >= 1.2.0
- shapely >= 2.0.4

## Examples

See the [examples/](examples/) directory for more usage examples.

## License

MIT License - see [LICENSE](LICENSE) file for details.
