import xml.etree.ElementTree as ET
import export.utils
from enum import Enum


class XmlWriter:
    def __init__(self, inverse=False):
        self.inverse = inverse
        self.network= ET.Element("ots:Network")
        # Define namespaces if needed
        # ET.register_namespace('ots', "http://example.com/ots")  # optional
        self.tree = ET.ElementTree(self.network)
        self.points = []

    def add_point(self, point: export.utils.Point):
        """ <ots:Node Coordinate="(15.9460,-8.5808)" Direction="417.0623 deg(E)" Id="SB" />
        """
        if self.inverse:
            point.angle += 180
        coords = (round(float(point.x), 4), round(float(point.y), 4))
        node = ET.SubElement(self.network, "ots:Node", {
            "Id": point.id,
            "Coordinate": str(coords),
            "Direction": f"{round(float(point.angle), 4)} deg(E)"
        })
        self.points.append(point)
        return node

    def add_link(self, link_id, point0: export.utils.Point, point1: export.utils.Point, lane_layout="RIGHT"):
        """ <ots:Link Id="EEP" NodeEnd="EP" NodeStart="E" OffsetEnd="-5.25m" OffsetStart="-5.25m" Type="URBAN">
                <ots:DefinedLayout>1RIGHT</ots:DefinedLayout>
            </ots:Link>
        """
        link = ET.SubElement(self.network, "ots:Link", {
            "Id": link_id,
            "NodeStart": point1.id if self.inverse else point0.id,
            "NodeEnd": point0.id if self.inverse else point1.id,
            "Type": "URBAN"
        })
        # Add child elements
        def_layout = ET.SubElement(link, "ots:DefinedLayout")
        def_layout.text = lane_layout
        return link

    def link_type_straight(self, parent):
        parent.insert(0, ET.Element("ots:Straight"))  # insert at the top

    def link_type_bezier(self, parent):
        parent.insert(0, ET.Element("ots:Bezier"))  # insert at the top

    def link_type_arc(self, parent, radius, direction):
        if direction == "right":
            if self.inverse:
                direction = "L"
            else:
                direction = "R"
        if direction == "left":
            if self.inverse:
                direction = "R"
            else:
                direction = "L"
        element = ET.Element("ots:Arc", {
            "Direction": direction,  # expects either "L" or "R" (I guess)
            "Radius": f"{round(float(abs(radius)), 4)} m"
        })
        parent.insert(0, element)  # insert at the top

    def find_point(self, x, y, range=0.1):
        points_found = []
        for point in self.points:
            if abs(point.x - x) <= range and  abs(point.y - y) <= range:
                points_found.append(point)
        if len(points_found) > 1:
            raise LookupError("More than 1 point found! Maybe decrese the range?")
        return points_found[0]

    def write(self, to_file=False):
        ET.indent(self.tree, space="  ")  # 2-space indentation
        if to_file:
            self.tree.write("output.xml", encoding="utf-8", xml_declaration=False)
        else:
            ET.dump(self.tree)
