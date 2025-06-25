import re, json
from collections import defaultdict
from matplotlib.widgets import CheckButtons

from draw.aed import *
from draw.basic import *
from parse import *
from utils import *


with open('./parser/res/kvk_Area2.cfg', 'r') as f:
    raw_text = f.read()

parser = Parser()
tokens = parser.tokenize(raw_text)
nested_lists = parser.parse_to_nested_lists(tokens)
elements = parser.get_lane_elements(nested_lists)


fig, ax = plt.subplots()

TRANSLATION_ROTATION = True
if TRANSLATION_ROTATION:
    ## Perform Translation and Rotation
    # Target point & angle
    angle_t = 90; x_t = 0; y_t = 0
    x_t, y_t = StraightBasic(100, start_x=x_t, start_y=y_t, angle_deg=angle_t).draw(ax=ax)

    # Current point & angle (of AED)
    filtered = [e for e in elements if e['name'] == "l49"]
    assert len(filtered) == 1
    el = filtered[0]
    x0 = el["values"]["x0"]; y0 = el["values"]["y0"]; x1 = el["values"]["x1"]; y1 = el["values"]["y1"]
    angle_c = angle_from_vector(vector_from_points((x1, y1), (x0, y0)), degrees=True)
    x_c = x1
    y_c = y1

    offset = (x_t - x_c, y_t - y_c)
    angle_deg = angle_t - angle_c
    angle_rad = convert_angle(angle_deg, to='radians')


names = []
lines = []
for i, element in enumerate(elements):
    v = element["values"]
    name = element["name"]
    names.append(element["type"] + " " + name)

    if element["type"] == "Straight":
        x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
        d0 = v["DistToRef0"]; d1 = v["DistToRef1"]  # apparently for Straight, this is the correct offset
        vec = vector_from_points([x0, y0], [x1, y1])
        x0, y0 = translate_perpendicular([x0, y0], vec, d0)
        x1, y1 = translate_perpendicular([x1, y1], vec, d1)

        if TRANSLATION_ROTATION:
            x0, y0 = rotate_around(translate((x0, y0), offset), (x_t, y_t), angle_deg)
            x1, y1 = rotate_around(translate((x1, y1), offset), (x_t, y_t), angle_deg)
        line = StraightAED(x0, y0, x1, y1, name).draw(ax=ax)

    elif element["type"] == "Bezier":
        x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
        angle0 = v["Angle0"]; angle1 = v["Angle1"]
        # d0 = v["DistToMid0"]  # apparently for Bezier, this is the correct offset
        # d1 = v["DistToMid1"]
        # vec0 = vector_from_angle(angle0)
        # vec1 = vector_from_angle(angle1)
        # x0, y0 = translate_perpendicular([x0, y0], vec0, d0)
        # x1, y1 = translate_perpendicular([x1, y1], vec1, d1)
        if TRANSLATION_ROTATION:
            x0, y0 = rotate_around(translate((x0, y0), offset), (x_t, y_t), angle_deg)
            x1, y1 = rotate_around(translate((x1, y1), offset), (x_t, y_t), angle_deg)
            angle0 += angle_rad
            angle1 += angle_rad
        line = HermiteSplineAED(x0, y0, angle0, x1, y1, angle1, name).draw(ax=ax)

    elif element["type"] == "CircularArc":
        x0 = v["x0"]; y0 = v["y0"]; angle0 = v["Angle0"]; angle1 = v["Angle1"]; r = v["r"]
        d0 = v["DistToRef0"]; d1 = v["DistToRef1"]  # apparently for CircularArc, this is the correct offset

        if d0 != d1:
            raise ValueError("This should not happen, I guess??")

        if TRANSLATION_ROTATION:
            x0, y0 = rotate_around(translate((x0, y0), offset), (x_t, y_t), angle_deg)
            angle0 += angle_rad
            angle1 += angle_rad
        line = CircularArcAED(x0, y0, angle0, angle1, r + d0).draw(ax=ax)
    lines.append(line)


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