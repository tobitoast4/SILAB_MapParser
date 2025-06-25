import re, json
from collections import defaultdict
from matplotlib.widgets import CheckButtons

from draw_aed import *
from utils import *


def tokenize(text):
    """ Simple solution: Each line is a separate token."""
    # Simple tokenizer to split on delimiters
    # tokens = re.findall(r'[\w\.-]+|\(|\)|\{|\}|=|;|<->|,|"[^"]*"|\S', text)
    # return [t.strip() for t in tokens if t.strip()]
    tokens = text.split("\n")
    return [t.strip() for t in tokens if t.strip()]
    

def parse_to_nested_lists(tokens, current_t=0, parent=None, bracket=None, depth=0):
    new_obj = []
    amount_tokens = len(tokens)
    while current_t < amount_tokens:
        token = tokens[current_t]
        current_t += 1
        new_obj.append(token)
        if "{" in token:
            if "}" in token:  # if closing bracket is in same token
                continue
            current_t, child = parse_to_nested_lists(tokens, current_t, new_obj, bracket="{", depth=depth+1)
            new_obj.append(child)
        elif "}" in token and bracket=="{":
            return current_t, new_obj
        elif "(" in token:
            if ")" in token:  # if closing bracket is in same token
                continue
            current_t, child = parse_to_nested_lists(tokens, current_t, new_obj, bracket="(", depth=depth+1)
            new_obj.append(child)
        elif ")" in token and bracket=="(":
            return current_t, new_obj
        else:
            pass
    return new_obj


# def nested_lists_to_json(data, parent=None):
#     SKIP = ["{", "}", "(", ")", "};", ");"]
#     new_obj = {
#         "strings": [],
#         "values": {},
#         "children": []
#     }

#     if isinstance(data, dict):
#         raise SyntaxError("Only list should be passed")
#     elif isinstance(data, list):
#         for item in data:
#             child = nested_lists_to_json(item, new_obj)
#             if child:
#                 new_obj["children"].append(child)
#     else:
#         if data in SKIP:
#             pass
#         elif "=" in data and data[-1] == ";":
#             data_split = data[:-1].split("=")
#             assert len(data_split) == 2
#             key = data_split[0]
#             value = data_split[1]
#             parent["values"][key] = value     # here we add to parent
#         else:
#             parent["strings"].append(data)  # here we add to new_object !!!
#         return
#     return new_obj


elements = []

def get_lane_elements(data, parent=None):
    if isinstance(data, dict):
        raise SyntaxError("Only list should be passed")
    elif isinstance(data, list):
        for i in range(len(data)):
            element = data[i]
            if i < len(data)-2:
                expected_curly_brace = data[i+1]
                values = data[i+2]
                if (str(element).startswith("Straight") \
                or str(element).startswith("Bezier") \
                or str(element).startswith("CircularArc")) \
                and expected_curly_brace == "{" \
                and isinstance(values, list):
                    element_split = element.split(" ")
                    values_dict = {}
                    for value in values:
                        if value[-1] == ";":
                            value = value[:-1]
                        try:
                            value_split = value.split("=")
                            key = value_split[0].strip()
                            val = float(value_split[1].strip())
                            values_dict[key] = val
                        except: pass
                    elements.append({
                        "type": element_split[0],
                        "name": element_split[1],
                        "values": values_dict
                    })
            get_lane_elements(element)

with open('./parser/res/kvk_Area2.cfg', 'r') as f:
    raw_text = f.read()

tokens = tokenize(raw_text)
nested_lists = parse_to_nested_lists(tokens)
get_lane_elements(nested_lists)


fig, ax = plt.subplots()
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