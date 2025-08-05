import xml.etree.ElementTree as ET

nodes = """<ots:Node Id="cp1-lane1-0" Coordinate="(-5.0, -0.125)" Direction="0.0 deg(E)" />
<ots:Node Id="cp1-lane1-1" Coordinate="(300.0, -0.125)" Direction="0.0 deg(E)" />
<ots:Node Id="cp2-lane1-0" Coordinate="(810.3785, -0.1262)" Direction="0.0006 deg(E)" />
<ots:Node Id="cp2-lane1-1" Coordinate="(1110.3785, -0.1231)" Direction="0.0006 deg(E)" />
<ots:Node Id="l66-0" Coordinate="(779.6044, -0.1266)" Direction="0.0006 deg(E)" />
<ots:Node Id="l69-0" Coordinate="(810.3784, 10.3738)" Direction="180.0006 deg(E)" />
<ots:Node Id="l69-1" Coordinate="(779.6043, 10.3734)" Direction="180.0006 deg(E)" />
<ots:Node Id="l70-0" Coordinate="(810.3783, 14.1238)" Direction="180.0006 deg(E)" />
<ots:Node Id="l70-1" Coordinate="(779.6043, 14.1234)" Direction="180.0006 deg(E)" />
<ots:Node Id="l71-0" Coordinate="(810.3783, 17.2488)" Direction="180.0006 deg(E)" />
<ots:Node Id="l71-1" Coordinate="(779.6042, 17.2484)" Direction="180.0006 deg(E)" />
<ots:Node Id="l136-0" Coordinate="(620.3766, -0.1261)" Direction="-0.0001 deg(E)" />
<ots:Node Id="l136-1" Coordinate="(741.2561, -0.1264)" Direction="-0.0001 deg(E)" />
<ots:Node Id="l142-0" Coordinate="(741.2562, 17.2486)" Direction="179.9999 deg(E)" />
<ots:Node Id="l142-1" Coordinate="(620.3766, 17.2489)" Direction="179.9999 deg(E)" />
<ots:Node Id="l143-0" Coordinate="(741.2561, 14.1236)" Direction="179.9999 deg(E)" />
<ots:Node Id="l143-1" Coordinate="(620.3766, 14.1239)" Direction="179.9999 deg(E)" />
<ots:Node Id="l144-0" Coordinate="(741.2561, 10.3736)" Direction="179.9999 deg(E)" />
<ots:Node Id="l144-1" Coordinate="(620.3766, 10.3739)" Direction="179.9999 deg(E)" />
<ots:Node Id="l145-1" Coordinate="(496.755, 10.3744)" Direction="179.9998 deg(E)" />
<ots:Node Id="l146-1" Coordinate="(496.755, 14.1244)" Direction="179.9998 deg(E)" />
<ots:Node Id="l147-1" Coordinate="(496.7551, 17.2494)" Direction="179.9998 deg(E)" />
<ots:Node Id="l149-0" Coordinate="(496.755, -0.1256)" Direction="-0.0002 deg(E)" />
<ots:Node Id="l170-1" Coordinate="(567.7674, -63.0834)" Direction="-87.4217 deg(E)" />
<ots:Node Id="l171-0" Coordinate="(571.7633, -62.9034)" Direction="-267.4215 deg(E)" />
<ots:Node Id="l152-0" Coordinate="(373.5212, -0.1252)" Direction="-0.0002 deg(E)" />
<ots:Node Id="l161-1" Coordinate="(373.5213, 10.3748)" Direction="179.9998 deg(E)" />
<ots:Node Id="l162-1" Coordinate="(373.5213, 14.1248)" Direction="179.9998 deg(E)" />
<ots:Node Id="l163-1" Coordinate="(373.5213, 17.2498)" Direction="179.9998 deg(E)" />
<ots:Node Id="l160-1" Coordinate="(327.1537, 10.375)" Direction="179.9998 deg(E)" />
<ots:Node Id="l164-1" Coordinate="(327.1538, 17.25)" Direction="179.9998 deg(E)" />
<ots:Node Id="l165-1" Coordinate="(327.1538, 14.125)" Direction="179.9998 deg(E)" />
<ots:Node Id="l169-0" Coordinate="(327.1541, -0.1251)" Direction="-0.0004 deg(E)" />
<ots:Node Id="l166-1" Coordinate="(300.0, 10.375)" Direction="180.0 deg(E)" />
<ots:Node Id="l167-1" Coordinate="(300.0, 14.125)" Direction="180.0 deg(E)" />
<ots:Node Id="l168-1" Coordinate="(300.0, 17.25)" Direction="180.0 deg(E)" />
<ots:Node Id="l172-1" Coordinate="(571.7595, -151.7412)" Direction="-87.4218 deg(E)" />
<ots:Node Id="l173-0" Coordinate="(575.7555, -151.5613)" Direction="92.5782 deg(E)" />
<ots:Node Id="l181-0" Coordinate="(588.2378, -163.9238)" Direction="-178.5122 deg(E)" />
<ots:Node Id="l213-0" Coordinate="(575.9991, -162.5285)" Direction="-267.4215 deg(E)" />
<ots:Node Id="l212-1" Coordinate="(572.5026, -162.686)" Direction="-87.4217 deg(E)" />
<ots:Node Id="l195-1" Coordinate="(560.088, -164.655)" Direction="-178.5122 deg(E)" />
<ots:Node Id="l221-0" Coordinate="(566.7498, -164.4819)" Direction="181.4882 deg(E)" />
<ots:Node Id="l216-0" Coordinate="(566.8342, -167.7308)" Direction="1.4876 deg(E)" />
<ots:Node Id="l217-0" Coordinate="(560.2567, -171.1528)" Direction="1.4882 deg(E)" />
<ots:Node Id="l217-1" Coordinate="(566.9186, -170.9797)" Direction="1.4882 deg(E)" />
<ots:Node Id="l218-1" Coordinate="(579.8879, -170.6429)" Direction="1.4877 deg(E)" />
<ots:Node Id="l219-1" Coordinate="(588.4066, -170.4216)" Direction="1.4883 deg(E)" />
<ots:Node Id="l220-0" Coordinate="(560.1723, -167.9039)" Direction="1.4882 deg(E)" />
<ots:Node Id="l222-1" Coordinate="(579.7191, -164.1451)" Direction="181.4883 deg(E)" />
<ots:Node Id="l184-0" Coordinate="(652.1285, -178.631)" Direction="-219.2673 deg(E)" />
<ots:Node Id="l184-1" Coordinate="(623.5282, -166.0082)" Direction="-178.5122 deg(E)" />
<ots:Node Id="l185-0" Coordinate="(623.6191, -169.507)" Direction="1.4876 deg(E)" />
<ots:Node Id="l185-1" Coordinate="(649.9132, -181.3407)" Direction="-39.2674 deg(E)" />
<ots:Node Id="l186-1" Coordinate="(692.8603, -216.4513)" Direction="-39.267 deg(E)" />
<ots:Node Id="l187-0" Coordinate="(695.0756, -213.7416)" Direction="140.733 deg(E)" />
<ots:Node Id="l188-0" Coordinate="(507.0992, -181.1396)" Direction="49.1401 deg(E)" />
<ots:Node Id="l188-1" Coordinate="(521.341, -172.1636)" Direction="1.4876 deg(E)" />
<ots:Node Id="l189-0" Coordinate="(521.2502, -168.6648)" Direction="-178.5122 deg(E)" />
<ots:Node Id="l189-1" Coordinate="(504.4521, -178.8498)" Direction="-130.8599 deg(E)" />
<ots:Node Id="l190-1" Coordinate="(469.0806, -219.7412)" Direction="229.1399 deg(E)" />
<ots:Node Id="l191-0" Coordinate="(471.7277, -222.031)" Direction="49.1399 deg(E)" />
<ots:Node Id="l196-1" Coordinate="(551.1524, -164.8871)" Direction="181.4878 deg(E)" />
<ots:Node Id="l197-0" Coordinate="(551.2368, -168.136)" Direction="1.4878 deg(E)" />
<ots:Node Id="l200-0" Coordinate="(551.3212, -171.3849)" Direction="1.4878 deg(E)" />
<ots:Node Id="l202-1" Coordinate="(603.4273, -163.5293)" Direction="-178.5122 deg(E)" />
<ots:Node Id="l205-0" Coordinate="(603.5961, -170.027)" Direction="1.4877 deg(E)" />
<ots:Node Id="l206-1" Coordinate="(534.6882, -171.817)" Direction="1.4879 deg(E)" />
<ots:Node Id="l207-0" Coordinate="(534.5194, -165.3191)" Direction="-178.5122 deg(E)" />"""

nodes_split = nodes.split("\n")
new_nodes = []
for xml_line in nodes_split:
    # Use regex to extract the coordinate
    # Regex to find and extract coordinates
    # Parse the XML string
    xml_line = xml_line.replace("ots:", "")
    element = ET.fromstring(xml_line)

    # Extract, modify and update the Coordinate attribute
    coord_str = element.attrib['Coordinate']  # e.g., "(534.5194, -165.3191)"
    x_str, y_str = coord_str.strip('()').split(',')
    x_new = float(x_str) + 0
    y_new = float(y_str) - 7
    element.set('Coordinate', f'({x_new:.4f}, {y_new:.4f})')

    # Convert back to string
    new_xml_line = ET.tostring(element, encoding='unicode')
    new_xml_line = new_xml_line.replace("<Node", "<ots:Node")
    new_nodes.append(new_xml_line)
    
print("\n".join(new_nodes))