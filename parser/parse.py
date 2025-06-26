import re, json
from collections import defaultdict
from matplotlib.widgets import CheckButtons


class Parser:
    def __init__(self):
        self.elements = []

    @staticmethod
    def tokenize(text):
        """ Simple solution: Each line is a separate token."""
        # Simple tokenizer to split on delimiters
        # tokens = re.findall(r'[\w\.-]+|\(|\)|\{|\}|=|;|<->|,|"[^"]*"|\S', text)
        # return [t.strip() for t in tokens if t.strip()]
        tokens = text.split("\n")
        return [t.strip() for t in tokens if t.strip()]
    
    @staticmethod
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
                current_t, child = Parser.parse_to_nested_lists(tokens, current_t, new_obj, bracket="{", depth=depth+1)
                new_obj.append(child)
            elif "}" in token and bracket=="{":
                return current_t, new_obj
            elif "(" in token:
                if ")" in token:  # if closing bracket is in same token
                    continue
                current_t, child = Parser.parse_to_nested_lists(tokens, current_t, new_obj, bracket="(", depth=depth+1)
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

    def get_lane_elements(self, data, last_lane=None):
        if isinstance(data, dict):
            raise SyntaxError("Only list should be passed")
        elif isinstance(data, list):
            for i in range(len(data)):
                element = data[i]
                if str(element).startswith("LaneCell"):
                    last_lane = element
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
                        self.elements.append({
                            "type": element_split[0],
                            "id": element_split[1],
                            "parent": last_lane,
                            "values": values_dict
                        })
                self.get_lane_elements(element, last_lane)
        return self.elements


if __name__ == "__main__":
    with open('./parser/res/kvk_Area2.cfg', 'r') as f:
        raw_text = f.read()

    parser = Parser()
    tokens = parser.tokenize(raw_text)
    nested_lists = parser.parse_to_nested_lists(tokens)
    elements = parser.get_lane_elements(nested_lists)

    with open("./parser/elements.json", "w") as json_file:
        json.dump({"elements": elements}, json_file, indent=4)
