import os
import json
import inspect
import pkgutil

import uuid
from xml.etree import ElementTree as ET
from xml.dom import minidom


# ==============================================================================
# Script
# ==============================================================================

if __name__ == "__main__":

    import brg

    root = ET.Element('graphml')

    key = ET.SubElement(root, 'key')
    graph = ET.SubElement(root, 'graph')

    for loader, name, is_pkg in pkgutil.walk_packages(brg.__path__):
        node = ET.SubElement(graph, 'node')

    ET.dump(root)
