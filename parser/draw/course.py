import numpy as np
import matplotlib.pyplot as plt
import math

try:
    from draw import utils
except:
    import utils

NUM_POINTS = 100
SHOW_LABELS = True
FONT_SIZE = 9



class Course:
    def __init__(self, id=""):
        self.id = id
        self.parts = []


class StraightCourse:
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
        self.angle0 += angle_deg
        self.angle1 += angle_deg
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
        
        self.x1 = self.x0 + self.length * np.cos(angle_rad)
        self.y1 = self.y0 + self.length * np.sin(angle_rad)
        
        if ax:
            line, = ax.plot([self.x0, self.x1], [self.y0, self.y1], color='green')
            # Optionally: Plot start and end
            # if self.id == "cp7":
            #     ax.plot(self.x0, self.y0, marker='o', color='black', markersize=5)
            #     ax.plot(self.x1, self.y1, marker='x', color='red', markersize=5)
            if SHOW_LABELS:
                ax.text((self.x0+self.x1)//2, (self.y0+self.y1)//2, self.id, color='blue', va='center', fontsize=FONT_SIZE)
            return line
        else:
            return self.x1, self.y1


class CurveCourse:
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

    def calculate(self, ax=None):
        """
        Draws a circular arc with a given length and radius.
        - direction: 'right' or 'left'
        - start_angle_deg: initial heading angle in degrees (0 = pointing right)
        Returns the end (x, y) and new heading angle.
        """
        # Arc angle in radians: arc_length = radius * angle
        r = abs(self.radius)
        arc_angle_rad = self.length / r
        if self.direction == 'right':
            arc_angle_rad = -arc_angle_rad

        # Generate theta values
        thetas = np.linspace(0, arc_angle_rad, NUM_POINTS)

        # Start angle in radians
        start_angle_rad = np.radians(self.angle0)

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

        # Return final position and angle
        self.angle1 = self.angle0 + np.degrees(arc_angle_rad)
        self.x1 = arc_x[-1]
        self.y1 = arc_y[-1]

        if ax:
            ax.plot(cx, cy, marker='o', color='red', markersize=1)
            line, = ax.plot(arc_x, arc_y, color='red')
            if SHOW_LABELS:
                ax.text(arc_x[len(arc_x)//2], arc_y[len(arc_y)//2], self.id, color='blue', va='center', fontsize=FONT_SIZE)
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
            x, y = StraightCourse(length, x0=x, y0=y, angle=angle).calculate(ax=ax)
            pass
        elif road_type == "Bend":
            length = road[2]
            radius = road[3]
            x, y, angle = CurveCourse(length=length, radius=radius, x0=x, y0=y, 
                                    angle0=angle).calculate(ax=ax)
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
