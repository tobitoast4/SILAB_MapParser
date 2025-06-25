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


angle = 90; x = 0; y = 0
x, y = draw_straight(100, start_x=x, start_y=y, angle_deg=angle, ax=ax)


names = []
lines = []
for i, element in enumerate(elements):
    v = element["values"]
    name = element["name"]
    names.append(element["type"] + " " + name)
    if element["type"] == "Bezier":
        # d0 = v["DistToMid0"]  # apparently for Bezier, this is the correct offset
        # d1 = v["DistToMid1"]
        x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
        angle0 = v["Angle0"]
        angle1 = v["Angle1"]
        # vec0 = vector_from_angle(angle0)
        # vec1 = vector_from_angle(angle1)
        # x0, y0 = translate_perpendicular([x0, y0], vec0, d0)
        # x1, y1 = translate_perpendicular([x1, y1], vec1, d1)
        line = aed_plot_hermite_spline(x0, y0, angle0, x1, y1, angle1, ax, name)
    elif element["type"] == "Straight":
        d0 = v["DistToRef0"]  # apparently for Straight, this is the correct offset
        d1 = v["DistToRef1"]
        x0 = v["x0"]; y0 = v["y0"]; x1 = v["x1"]; y1 = v["y1"]
        vec = vector_from_points([x0, y0], [x1, y1])
        x0, y0 = translate_perpendicular([x0, y0], vec, d0)
        x1, y1 = translate_perpendicular([x1, y1], vec, d1)
        line = aed_draw_straight(x0, y0, x1, y1, ax, name)
    elif element["type"] == "CircularArc":
        d0 = v["DistToRef0"]  # apparently for CircularArc, this is the correct offset
        d1 = v["DistToRef1"]
        x0 = v["x0"]; y0 = v["y0"]; angle0 = v["Angle0"]; angle1 = v["Angle1"]; r = v["r"]
        if d0 != d1:
            raise ValueError("This should not happen, I guess??")
        line = aed_draw_circular_arc(x0, y0, angle0, angle1, r + d0, ax, name)
    lines.append(line)


# Make lines dynamically hidden / visible
def toggle_visibility(label):
    for i, name in enumerate(names):
        if name == label:
            break
    line = lines[i]
    line.set_visible(not line.get_visible())
    plt.draw()

check_ax = plt.axes([0.05, 0.1, 0.2, 0.65])
check = CheckButtons(check_ax, names, [True for _ in range(len(names))])
check.on_clicked(toggle_visibility)

ax.set_aspect('equal')
ax.grid(True)
ax.legend()
plt.title("SILAB Map")
plt.show()