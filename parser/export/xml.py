import xml.etree.ElementTree as ET
import export.utils
from enum import Enum


class LaneLayout(Enum):
    TWOLANE = "2LANE"
    LEFT = "1LEFT"
    RIGHT = "1RIGHT"


class XmlWriter:
    def __init__(self):
        self.network= ET.Element("ots:Network")
        # Define namespaces if needed
        ET.register_namespace('ots', "http://example.com/ots")  # optional
        self.tree = ET.ElementTree(self.network)
        self.points = []

    def add_point(self, point: export.utils.Point):
        """ <ots:Node Coordinate="(15.9460,-8.5808)" Direction="417.0623 deg(E)" Id="SB" />
        """
        coords = (round(float(point.x), 4), round(float(point.y), 4))
        node = ET.SubElement(self.network, "ots:Link", {
            "Id": point.id,
            "Coordinate": str(coords),
            "NodDirectioneStart": f"{point.angle} deg(E)"
        })
        self.points.append(point)
        return node

    def add_link(self, link_id, point0: export.utils.Point, point1: export.utils.Point, lane_layout: LaneLayout = LaneLayout.RIGHT):
        """ <ots:Link Id="EEP" NodeEnd="EP" NodeStart="E" OffsetEnd="-5.25m" OffsetStart="-5.25m" Type="URBAN">
                <ots:DefinedLayout>1RIGHT</ots:DefinedLayout>
            </ots:Link>
        """
        link = ET.SubElement(self.network, "ots:Link", {
            "Id": link_id,
            "NodeEnd": point0.id,
            "NodeStart": point1.id,
            "Type": "URBAN"
        })
        # Add child elements
        def_layout = ET.SubElement(link, "ots:DefinedLayout")
        def_layout.text = lane_layout.value
        return link

    def link_type_straight(self, parent):
        ET.SubElement(parent, "ots:Straight")

    def link_type_bezier(self, parent):
        ET.SubElement(parent, "ots:Bezier")

    def link_type_arc(self, parent, radius, direction):
        if direction == "right":
            direction = "R"
        if direction == "left":
            direction = "L"
        ET.SubElement(parent, "ots:Arc", {
            "Direction": direction,  # expects either "L" or "R" (I guess)
            "Radius": f"{round(float(radius), 4)} m"
        })

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
            self.tree.write("output.xml", encoding="utf-8", xml_declaration=True)
        else:
            ET.dump(self.tree)
