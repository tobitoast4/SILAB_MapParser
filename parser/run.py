import re, json
from collections import defaultdict
from matplotlib.widgets import CheckButtons

from draw.aed import *
from draw.course import *
from parse import *
from draw import utils


with open('parser/full.json', 'r') as f:
    file_content = f.read()
    map_content = json.loads(file_content)


objects = []

# initial settings for Course
angle = 90
x = 0
y = 0


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
                vector = utils.vector_from_points((x0, y0), (x1, y1))
                x0, y0 = utils.translate_perpendicular((x0, y0), vector, d0)
                x1, y1 = utils.translate_perpendicular((x1, y1), vector, d1)
                line = StraightAED(x0, y0, x1, y1, id=c_id, parent=area)
                line.calculate()
                objects.append(line)
                area.parts.append(line)
        
            elif c_type == "Bezier":
                x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
                angle0 = v["Angle0"]; angle1 = v["Angle1"]
                spline = HermiteSplineAED(x0, y0, angle0, x1, y1, angle1, id=c_id, parent=area)
                spline.calculate()
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

for connection in map_content["Connections"]:
    conn0_split = connection[0].split(".")
    conn1_split = connection[1].split(".")
    conn0_id = conn0_split[1]
    conn1_id = conn1_split[1]
    obj0 = [obj for obj in objects if obj.id == conn0_id][0]
    obj1 = [obj for obj in objects if obj.id == conn1_id][0]
    create_connection(obj0, conn0_split[2], obj1, conn1_split[2])
    create_connection(obj1, conn1_split[2], obj0, conn1_split[2])

    
## Transform elements  appling the CustomConnections
# Order of CustomConnections should match order of how objects appear !!!  TODO: Change that
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


## Visualize
fig, ax = plt.subplots()
names = []
lines = []
for obj in objects: 
    lines.append(obj.calculate(ax=ax))
    names.append(f"{obj.id} {type(obj).__name__[:5]}")
    




# fig, ax = plt.subplots()

# TRANSLATION_ROTATION = True
# if TRANSLATION_ROTATION:
#     ## Perform Translation and Rotation
#     # Target point & angle
#     angle_t = 90; x_t = 0; y_t = 0
#     x_t, y_t = StraightCourse(100, x0=x_t, y0=y_t, angle=angle_t).calculate(ax=ax)

#     # Current point & angle (of AED)
#     filtered = [e for e in elements if e['id'] == "l49"]
#     assert len(filtered) == 1
#     el = filtered[0]
#     x0 = el["values"]["x0"]; y0 = el["values"]["y0"]; x1 = el["values"]["x1"]; y1 = el["values"]["y1"]
#     angle_c = utils.angle_from_vector(utils.vector_from_points((x1, y1), (x0, y0)), degrees=True)
#     x_c = x1
#     y_c = y1

#     offset = (x_t - x_c, y_t - y_c)
#     angle_deg = angle_t - angle_c
#     angle_rad = utils.convert_angle(angle_deg, to='radians')


# names = []
# objects = []
# for i, element in enumerate(elements):
#     if element["type"] == "Course":
#         continue
#     v = element["values"]
#     name = element["id"]
#     names.append(element["type"] + " " + name)

#     if element["type"] == "Straight":
#         x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
#         d0 = v["DistToRef0"]; d1 = v["DistToRef1"]  # apparently for Straight, this is the correct offset
#         line = StraightAED(x0, y0, x1, y1, name).translate(offset).rotate((x_t, y_t), angle_deg).calculate(ax=ax)

#     elif element["type"] == "Bezier":
#         x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
#         angle0 = v["Angle0"]; angle1 = v["Angle1"]
#         # d0 = v["DistToMid0"]  # apparently for Bezier, this is the correct offset
#         # d1 = v["DistToMid1"]
#         line = HermiteSplineAED(x0, y0, angle0, x1, y1, angle1, name).translate(offset).rotate((x_t, y_t), angle_deg).calculate(ax=ax)

#     elif element["type"] == "CircularArc":
#         x0 = v["x0"]; y0 = v["y0"]; angle0 = v["Angle0"]; angle1 = v["Angle1"]; r = v["r"]
#         d0 = v["DistToRef0"]; d1 = v["DistToRef1"]  # apparently for CircularArc, this is the correct offset

#         if d0 != d1:
#             raise ValueError("This should not happen, I guess??")
#         line = CircularArcAED(x0, y0, angle0, angle1, r + d0).translate(offset).rotate((x_t, y_t), angle_deg).calculate(ax=ax)
#     objects.append(line)


# Make lines dynamically hidden / visible
def toggle_visibility(label):
    for i, name in enumerate(names):
        if name == label:
            break
    line = lines[i]
    line.set_visible(not line.get_visible())
    plt.draw()

# Make lines dynamically hidden / visible
check_ax = plt.axes([0.05, 0.1, 0.2, 0.65])
check = CheckButtons(check_ax, names, [True for _ in range(len(names))])
check.on_clicked(toggle_visibility)

ax.set_aspect('equal')
ax.grid(True)
ax.legend()
plt.title("SILAB Map")
plt.show()
