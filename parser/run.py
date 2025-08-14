import re, json
from collections import defaultdict
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import Button

from draw.aed import *
from draw.course import *
from parse import *
import draw.utils
import export.utils
import export.xml
import misc

SHOW_LEGEND = False
FILE_NAME = "Scenario01"

# Enter the inverted values of a Node to ensure this one is (0, 0, 0 deg(E)) 
GLOBAL_TRANSLATION = (-289.9635-8.9997+0.1891+0.0163, 26.7667-0.0666+2.21-0.0013-0.0001)
GLOBAL_ROTATION = 0.4234

# the following lanes (and its points!!!) will be excluded from XML export
EXCLUDE_FILE = "parser/res/json/exclude.json"
LINES_TO_EXCLUDE = misc.read_json(EXCLUDE_FILE)

with open(f'parser/res/json/{FILE_NAME}.json', 'r') as f:
    file_content = f.read()
    map_content = json.loads(file_content)


objects = []  # contains all instances of StraightCourse, CurveCourse, StraightAED, HermiteSplineAED, CircularArcAED
              # note that StraightCourse and CurveCourse themselves again can contain multiple lanes 

# initial settings for Course
angle = 0
x = 0
y = -3.625


## Create objects
for element in map_content["elements"]:
    e_type = element["type"]
    e_id = element["id"]

    if e_type == "Course":
        course = Course(e_id)
        for road in element["elements"]:
            c_type = road[1]
            c_id = road[0]

            if c_type == "Straight":
                length = road[2]
                straight = StraightCourse(length, x0=x, y0=y, angle=angle, 
                                      id=c_id, parent=course)
                x, y = straight.calculate()
                objects.append(straight)
                course.parts.append(straight)

            elif c_type == "Bend":
                length = road[2]
                radius = road[3]
                curve = CurveCourse(length=length, radius=radius, x0=x, y0=y, angle0=angle, 
                                          id=c_id, parent=course)
                x, y, angle = curve.calculate()
                objects.append(curve)
                course.parts.append(curve)

            else:
                raise ValueError("Road type not valid")
    elif e_type == "Area2":
        area = Area2(e_id)
        for road in element["elements"]:
            c_type = road["type"]
            c_id = road["id"]
            v = road["values"]

            if c_type == "Straight":
                x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
                d0 = v["DistToRef0"]; d1 = v["DistToRef1"]  # apparently for Straight, this is the correct offset
                vector = draw.utils.vector_from_points((x0, y0), (x1, y1))
                x0, y0 = draw.utils.translate_perpendicular((x0, y0), vector, d0)
                x1, y1 = draw.utils.translate_perpendicular((x1, y1), vector, d1)
                line = StraightAED(x0, y0, x1, y1, id=c_id, parent=area)
                line.calculate()
                objects.append(line)
                area.parts.append(line)
        
            elif c_type == "Bezier":
                x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
                angle0 = v["Angle0"]; angle1 = v["Angle1"]
                d0 = v["DistToRef0"]; d1 = v["DistToRef1"]
                spline = HermiteSplineAED(x0, y0, angle0, x1, y1, angle1, id=c_id, parent=area)
                spline.calculate()
                spline.x0, spline.y0 = utils.translate_perpendicular(
                    (spline.x0, spline.y0), utils.vector_from_angle(angle0), d0)
                spline.x1, spline.y1 = utils.translate_perpendicular(
                    (spline.x1, spline.y1), utils.vector_from_angle(angle1), d1)
                objects.append(spline)
                area.parts.append(spline)

            elif c_type == "CircularArc":
                x0 = v["x0"]; y0 = v["y0"]; angle0 = v["Angle0"]; angle1 = v["Angle1"]; r = v["r"]
                d0 = v["DistToRef0"]; d1 = v["DistToRef1"]  # apparently for CircularArc, this is the correct offset

                if d0 != d1:
                    raise ValueError("This should not happen, I guess??")
                arc = CircularArcAED(x0, y0, angle0, angle1, r + d0, id=c_id, parent=area)
                arc.calculate()
                objects.append(arc)
                area.parts.append(arc)
                
            else:
                raise ValueError("Road type not valid")
    else: 
        raise ValueError("Type not valid")

for obj in objects:
    obj.mirror()

## Create connections
def create_connection(objX, anchorX, objY, anchorY):
    if anchorX ==  "Begin":
        attribute_name = "connection0"
    else:  # "End"
        attribute_name = "connection1"
    if anchorY == "Begin":
        value = 0
    else:  # "End"
        value = 1
    # if getattr(objX, attribute_name) != None:
    #     print("TODO: This might be worth noting")
    setattr(objX, attribute_name, (objY, value))

# for connection in map_content["Connections"]:
#     conn0_split = connection[0].split(".")
#     conn1_split = connection[1].split(".")
#     conn0_id = conn0_split[1]
#     conn1_id = conn1_split[1]
#     obj0 = [obj for obj in objects if obj.id == conn0_id][0]
#     obj1 = [obj for obj in objects if obj.id == conn1_id][0]
#     create_connection(obj0, conn0_split[2], obj1, conn1_split[2])
#     create_connection(obj1, conn1_split[2], obj0, conn1_split[2])

    
## Transform elements  appling the CustomConnections
# Order of CustomConnections should match order of how objects appear !!!  TODO: Change that
if "CustomConnections" in map_content:
    for connection in map_content["CustomConnections"]:
        conn0_split = connection[0].split(".")
        conn1_split = connection[1].split(".")
        conn0_id = conn0_split[0]
        conn1_id = conn1_split[0]
        obj0 = [obj for obj in objects if obj.id == conn0_id][0]
        obj1 = [obj for obj in objects if obj.id == conn1_id][0]
        create_connection(obj0, conn0_split[1], obj1, conn1_split[1])
        create_connection(obj1, conn1_split[1], obj0, conn0_split[1])

        # Target point & angle (of obj0)
        if conn0_split[1] == "Begin":
            angle_t = obj0.angle0; x_t = obj0.x0; y_t = obj0.y0
        else:  # "End"
            angle_t = obj0.angle1; x_t = obj0.x1; y_t = obj0.y1
        # Current point & angle (of obj1)
        if conn1_split[1] == "Begin":
            angle_c = obj1.angle0; x_c = obj1.x0; y_c = obj1.y0
        else:  # "End"
            angle_c = obj1.angle1; x_c = obj1.x1; y_c = obj1.y1
        #Calculate difference
        offset = (x_t - x_c, y_t - y_c)
        angle_difference = angle_t - angle_c
        for other_obj in obj1.parent.parts:
            other_obj.translate(offset).rotate((x_t, y_t), angle_difference)
            other_obj.calculate()  # re-calculate attributes

if GLOBAL_TRANSLATION and GLOBAL_ROTATION:
    for obj in objects:
        obj.translate(GLOBAL_TRANSLATION)
        obj.rotate((0, 0), GLOBAL_ROTATION)

## Visualize
fig, ax = plt.subplots()
names = []
lines = []
for obj in objects: 
    lines.append(obj.calculate(ax=ax))
    names.append(f"{obj.id} {type(obj).__name__[:5]}")
    


## Create button for export
def export_map(event):
    xml_writer = export.xml.XmlWriter(inverse=False)

    ## Add all points. If there are two points, only add one of them 
    for obj in objects:
        if isinstance(obj, CircularArcAED):
            continue  # these might be to complicated, esp. in roundabouts (TODO: Implement solution for this)
        for pt in obj.get_points():
            added_point = xml_writer.find_point(pt.x, pt.y)
            if pt.id[:-2] in LINES_TO_EXCLUDE:
                continue
            if added_point == None:
                xml_writer.add_point(pt)
        
    ## Add all links
    for obj in objects:
        if isinstance(obj, CircularArcAED):
            continue  # these might be to complicated, esp. in roundabouts (TODO: Implement solution for this)
        if isinstance(obj, StraightCourse) or isinstance(obj, CurveCourse):
            for lane in obj.lanes:
                if lane.id in LINES_TO_EXCLUDE:
                    continue
                p0 = xml_writer.find_point(lane.x0, lane.y0)
                p1 = xml_writer.find_point(lane.x1, lane.y1)
                link = xml_writer.add_link(lane.id, p0, p1)
                if isinstance(obj, StraightCourse):
                    xml_writer.link_type_straight(link)
                if isinstance(obj, CurveCourse):
                    xml_writer.link_type_arc(link, lane.radius, obj.direction)
        else:
            if obj.id in LINES_TO_EXCLUDE:
                continue
            p0 = xml_writer.find_point(obj.x0, obj.y0)
            p1 = xml_writer.find_point(obj.x1, obj.y1)
            link = xml_writer.add_link(obj.id, p0, p1)

        if isinstance(obj, StraightCourse):
            xml_writer.link_type_straight(link)
        if isinstance(obj, CurveCourse):
            xml_writer.link_type_arc(link, obj.radius, obj.direction)
        if isinstance(obj, StraightAED):
            xml_writer.link_type_straight(link)
        if isinstance(obj, HermiteSplineAED):
            xml_writer.link_type_bezier(link)
    xml_writer.write(to_file_path=f"./parser/res/xml/{FILE_NAME}.xml")

button_ax = plt.axes([0.85, 0.9, 0.1, 0.05])
button = Button(button_ax, 'Export Map')
button.on_clicked(export_map)


## Create legend for hiding / showing lines
# Make lines dynamically hidden / visible
def toggle_visibility(label):
    for i, name in enumerate(names):
        if name == label:
            break
    line = lines[i]
    line.set_visible(not line.get_visible())
    plt.draw()

# Make lines dynamically hidden / visible
if SHOW_LEGEND:
    check_ax = plt.axes([0.05, 0.2, 0.2, 0.65])
    check = CheckButtons(check_ax, names, [True for _ in range(len(names))])
    check.on_clicked(toggle_visibility)


# Make lines clickable
def on_click_line(event):
    line = event.artist
    if line.get_visible():
        draw.utils.blink_line(fig, line, blinks=4)
        # YOu may use the following lines for debugging
        print(f'Line clicked at: {event.mouseevent.xdata:.2f}, {event.mouseevent.ydata:.2f}')
        print(f"    {type(line.parent).__name__}: {line.parent.id}")
        print(f"    x0={round(float(line.parent.x0), 4)}; y0={round(float(line.parent.y0), 4)}")
        print(f"    x1={round(float(line.parent.x1), 4)}; y1={round(float(line.parent.y1), 4)}")
        print(f"    angle0={round(float(line.parent.angle0), 4)}")
        print(f"    angle1={round(float(line.parent.angle1), 4)}")
        print()
        # excludes = misc.read_json(EXCLUDE_FILE)
        # excludes = list(set(excludes))  # remove duplicates
        # excludes.append(line.parent.id)
        # misc.write_json(EXCLUDE_FILE, excludes)
        

fig.canvas.mpl_connect('pick_event', on_click_line)


ax.set_aspect('equal')
ax.grid(True)
ax.legend()
plt.title("SILAB Map")
plt.show()
