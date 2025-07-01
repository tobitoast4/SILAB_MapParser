import xml.etree.ElementTree as ET
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
        # self.node_ids = []
        # self.node_links = []

    def add_node(self, node_id, x, y, angle):
        """ <ots:Node Coordinate="(15.9460,-8.5808)" Direction="417.0623 deg(E)" Id="SB" />
        """
        point = (x, y)
        node = ET.SubElement(self.network, "ots:Link", {
            "Id": node_id,
            "Coordinate": str(point),
            "NodDirectioneStart": f"{angle} deg(E)"
        })
        return node

    def add_link(self, node_id0, node_id1, lane_layout: LaneLayout):
        """ <ots:Link Id="EEP" NodeEnd="EP" NodeStart="E" OffsetEnd="-5.25m" OffsetStart="-5.25m" Type="URBAN">
                <ots:Straight />
                <ots:DefinedLayout>1RIGHT</ots:DefinedLayout>
            </ots:Link>
        """
        link = ET.SubElement(self.network, "ots:Link", {
            "Id": "EEP",
            "NodeEnd": node_id0,
            "NodeStart": node_id1,
            "Type": "URBAN"
        })
        # Add child elements
        def_layout = ET.SubElement(link, "ots:DefinedLayout")
        def_layout.text = lane_layout
        return link

    def link_type_straight(parent):
        ET.SubElement(parent, "ots:Straight")

    def link_type_bezier(parent):
        ET.SubElement(parent, "ots:Bezier")

    def link_type_arc(parent):
        ET.SubElement(parent, "ots:Arc", {
            "Id": "EEP",
            "Direction": "L",
            "Radius": "19.0000 m"
        })

    def write(self, to_file=False):
        ET.indent(self.tree, space="  ")  # 2-space indentation
        if to_file:
            self.tree.write("output.xml", encoding="utf-8", xml_declaration=True)
        else:
            ET.dump(self.tree)


x = XmlWriter()
x.add_link()
x.write()
