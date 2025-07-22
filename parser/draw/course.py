import numpy as np
import matplotlib.pyplot as plt
import math
import export.utils

try:
    from draw import utils
except:
    import utils

NUM_POINTS = 100
SHOW_LABELS = True
FONT_SIZE = 7

# Lane#0 will be at 0, LANE_POSITIONS[0], Lane#1 will be LANE_POSITIONS[1] meters from Lane#0, 
# Lane#2 will be LANE_POSITIONS[2] meters from Lane#0, ...
LANE_POSITIONS = [0, 3.75] 
LANE_IDS_TO_EXPORT = [0, 1]  # Only export Lane#0 and Lane#1, not Lane#2, Lane#3, etc.



class Course:
    def __init__(self, id=""):
        self.id = id
        self.parts = []


class StraightCourse:
    class Lane:
        def __init__(self, lane_id, id, x0, y0, x1, y1, angle0, angle1, parent):
            self.lane_id = lane_id
            self.id = id
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
            self.angle0 = angle0
            self.angle1 = angle1
            self.parent = parent

    def __init__(self, length, x0, y0, angle, id="", parent=None):
        self.id = id
        self.parent = parent
        self.connection0 = None
        self.connection1 = None
        self.length = length
        self.x0 = x0
        self.y0 = y0
        self.x1 = None
        self.y1 = None
        self.angle0 = angle  # in degrees
        self.angle1 = angle  # in degrees
        self.lanes = []

    def get_points(self):
        pts = []
        for lane in self.lanes:
            if lane.lane_id in LANE_IDS_TO_EXPORT:
                pts.append(export.utils.Point(lane.x0, lane.y0, lane.angle0, lane, 0))
                pts.append(export.utils.Point(lane.x1, lane.y1, lane.angle1, lane, 1))
        return pts

    def add_or_update_lane(self, new_lane: Lane):
        self.lanes = [lane for lane in self.lanes if lane.id != new_lane.id]  # remove old lane
        self.lanes.append(new_lane)

    def translate(self, offset):
        """Translate all points of the Straight by a given offset.

        Parameters:
            offset: tuple (dx, dy)
        """
        self.x0, self.y0 = utils.translate((self.x0, self.y0), offset)
        self.x1, self.y1 = utils.translate((self.x1, self.y1), offset)
        return self

    def rotate(self, center, angle_deg):
        """Rotate all points of the Straight around a given center by given angle.

        Parameters:
            center: tuple (x, y)
            angle_deg: angle in degrees
        """
        self.x0, self.y0 = utils.rotate_around((self.x0, self.y0), center, angle_deg)
        self.x1, self.y1 = utils.rotate_around((self.x1, self.y1), center, angle_deg)
        self.angle0 += angle_deg
        self.angle1 += angle_deg
        return self
    
    def mirror(self):
        self.y0 = -self.y0
        self.y1 = -self.y1
        self.angle0 = -self.angle0
        self.angle1 = -self.angle1
        return self

    def calculate(self, ax=None):
        """
        Draws a straight line of the given length and direction.
        
        Parameters:
            length: Length of the straight segment
            start_x, start_y: Starting coordinates
            angle: Direction in degrees (0 = right, 90 = up)
            ax: Matplotlib axis (optional)
        
        Returns:
            (end_x, end_y): End coordinates
        """
        angle_rad = np.radians(self.angle0)
        
        if not self.x1 and not  self.y1:
            self.x1 = self.x0 + self.length * np.cos(angle_rad)
            self.y1 = self.y0 + self.length * np.sin(angle_rad)
        
        if ax:
            for l in range(len(LANE_POSITIONS)):
                vector = utils.vector_from_points((self.x0, self.y0), (self.x1, self.y1))
                x0, y0 = utils.translate_perpendicular((self.x0, self.y0), vector, -LANE_POSITIONS[l])
                x1, y1 = utils.translate_perpendicular((self.x1, self.y1), vector, -LANE_POSITIONS[l])
                lane = StraightCourse.Lane(l, f"{self.id}-lane{l}", 
                            x0, y0, x1, y1, self.angle0, self.angle1, self)
                self.add_or_update_lane(lane)
                line, = ax.plot([x0, x1], [y0, y1], color='green', picker=2)
                line.parent = lane
                utils.plot_oriented_triangle((x1, y1), self.angle0, "green", ax=ax)
                # Optionally: Plot start and end
                # if self.id == "cp7":
                #     ax.plot(self.x0, self.y0, marker='o', color='black', markersize=5)
                #     ax.plot(self.x1, self.y1, marker='x', color='red', markersize=5)
                if SHOW_LABELS:
                    ax.text((self.x0+self.x1)//2, (self.y0+self.y1)//2, lane.id, color='blue', va='center', fontsize=FONT_SIZE)
            return line
        else:
            return self.x1, self.y1


class CurveCourse:
    class Lane:
        def __init__(self, lane_id, id, x0, y0, x1, y1, angle0, angle1, radius, parent):
            self.lane_id = lane_id
            self.id = id
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
            self.angle0 = angle0
            self.angle1 = angle1
            self.radius = radius
            self.parent = parent

    def __init__(self, length, radius, x0=0, y0=0, angle0=0, id="", parent=None):
        self.id = id
        self.parent = parent
        self.connection0 = None
        self.connection1 = None
        self.length = length
        self.radius = radius
        if radius < 0:
            self.direction = "left"
        else: 
            self.direction = "right"
        self.x0 = x0
        self.y0 = y0
        self.x1 = None
        self.y1 = None
        self.angle0 = angle0      # in degrees
        self.angle1 = None        # in degrees
        self.lanes = []

    def get_points(self):
        pts = []
        for lane in self.lanes:
            if lane.lane_id in LANE_IDS_TO_EXPORT:
                pts.append(export.utils.Point(lane.x0, lane.y0, lane.angle0, lane, 0))
                pts.append(export.utils.Point(lane.x1, lane.y1, lane.angle1, lane, 1))
        return pts

    def add_or_update_lane(self, new_lane: Lane):
        self.lanes = [lane for lane in self.lanes if lane.id != new_lane.id]  # remove old lane
        self.lanes.append(new_lane)

    def translate(self, offset):
        """Translate all points of the Straight by a given offset.

        Parameters:
            offset: tuple (dx, dy)
        """
        
        self.x0, self.y0 = utils.translate((self.x0, self.y0), offset)
        return self

    def rotate(self, center, angle_deg):
        """Rotate all points of the Straight around a given center by given angle.

        Parameters:
            center: tuple (x, y)
            angle_deg: angle in degrees
        """
        self.x0, self.y0 = utils.rotate_around((self.x0, self.y0), center, angle_deg)
        self.angle0 += angle_deg
        self.angle1 += angle_deg
        return self
    
    def mirror(self):
        self.y0 = -self.y0
        self.y1 = -self.y1
        self.angle0 = -self.angle0
        self.angle1 = -self.angle1
        if self.direction == "right":
            self.direction = "left"
        else: 
            self.direction = "right"
        return self

    def calculate(self, ax=None):
        """
        Draws a circular arc with a given length and radius.
        - direction: 'right' or 'left'
        - start_angle_deg: initial heading angle in degrees (0 = pointing right)
        Returns the end (x, y) and new heading angle.
        """
        for l in range(len(LANE_POSITIONS)):
            # Arc angle in radians: arc_length = radius * angle
            r = abs(self.radius)
            arc_angle_rad = self.length / r
            if self.direction == 'right':
                arc_angle_rad = -arc_angle_rad

            # Generate theta values
            thetas = np.linspace(0, arc_angle_rad, NUM_POINTS)

            # Start angle in radians
            start_angle_rad = np.radians(self.angle0)
            if l == 0:  # We want to store the values of the first lane
                self.angle1 = self.angle0 + np.degrees(arc_angle_rad)

            if self.direction == "right":
                cx = self.x0 - math.cos(np.pi/2 + start_angle_rad) * r
                cy = self.y0 - math.sin(np.pi/2 + start_angle_rad) * r
                arc_x = cx + abs(r) * np.cos(thetas + start_angle_rad + np.pi/2)
                arc_y = cy + abs(r) * np.sin(thetas + start_angle_rad + np.pi/2)
            else:
                cx = self.x0 + math.cos(np.pi/2 + start_angle_rad) * r
                cy = self.y0 + math.sin(np.pi/2 + start_angle_rad) * r
                arc_x = cx + abs(r) * np.cos(thetas - (np.pi/2 - start_angle_rad))
                arc_y = cy + abs(r) * np.sin(thetas - (np.pi/2 - start_angle_rad))
            
            for p in range(len(arc_x)):
                x = arc_x[p]
                y = arc_y[p]
                try: 
                    x_n = arc_x[p+1]
                    y_n = arc_y[p+1]
                    vector = utils.vector_from_points((x, y), (x_n, y_n))
                except:
                    vector = utils.vector_from_angle(utils.convert_angle(self.angle1, to='radians'))
                arc_x[p], arc_y[p] = utils.translate_perpendicular((x, y), vector, -LANE_POSITIONS[l])

            # Return final position and angle
            if l == 0:  # We want to store the values of the first lane
                self.x1 = arc_x[-1]
                self.y1 = arc_y[-1]

            if ax:
                current_radius = utils.euclidean_distance((cx, cy), (arc_x[0], arc_y[0]))
                lane = CurveCourse.Lane(l, f"{self.id}-lane{l}", arc_x[0], arc_y[0], arc_x[-1], 
                                        arc_y[-1], self.angle0, self.angle1, current_radius, self)
                self.add_or_update_lane(lane)
                ax.plot(cx, cy, marker='o', color='red', markersize=1)
                line, = ax.plot(arc_x, arc_y, color='red', picker=2)
                utils.plot_oriented_triangle((arc_x[-1], arc_y[-1]), self.angle1, "red", ax=ax)
                line.parent = lane
                if SHOW_LABELS:
                    ax.text(arc_x[len(arc_x)//2], arc_y[len(arc_y)//2], lane.id, color='blue', va='center', fontsize=FONT_SIZE)
        if ax:
            return line
        else:
            return self.x1, self.y1, self.angle1


if __name__ == "__main__":
    roads = [
        # id   # type  # parameters from silab
        ["cp1", "Straight", 100],
        ["cp2", "Bend", 157, 100],
        ["cp3", "Bend", 157, -100],
        ["cp4", "Straight", 300],
        ["cp5", "Bend",  1500, -500],
        ["cp6", "Bend",  340, -200],
        ["cp7", "Straight", 3000] 
    ]

    fig, ax = plt.subplots()

    angle = 90
    x = 0
    y = 0

    for road in roads:
        road_type = road[1]
        if road_type == "Straight":
            length = road[2]
            straight = StraightCourse(length, x0=x, y0=y, angle=angle)
            x, y = straight.calculate()
            straight.calculate(ax=ax)
        elif road_type == "Bend":
            length = road[2]
            radius = road[3]
            curve = CurveCourse(length=length, radius=radius, x0=x, y0=y, 
                                angle0=angle)
            x, y, angle = curve.calculate()
            curve.calculate(ax=ax)
            pass
        else:
            raise ValueError("Road type not valid")


    ## TEST for seeing one Straight and a laft and right curve
    # angle = 90; x = 0; y = 0
    # x, y = draw_straight(100, start_x=x, start_y=y, angle_deg=angle, ax=ax)
    # draw_curve(length=97, radius=-100, direction="right", start_x=x, start_y=y, start_angle_deg=angle, ax=ax)
    # draw_curve(length=47, radius=-100, direction="left", start_x=x, start_y=y, start_angle_deg=angle, ax=ax)

    # Final formatting
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()
    plt.title("SILAB Map")
    plt.show()
