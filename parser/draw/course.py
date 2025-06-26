import numpy as np
import math
import matplotlib.pyplot as plt


class Course:
    def __init__(self, id=""):
        self.id = id
        self.parts = []


class StraightCourse:
    def __init__(self, length, x0, y0, angle, id=""):
        self.id = id
        self.connectionStart = None
        self.connectionEnd = None
        self.length = length
        self.x0 = x0
        self.y0 = y0
        self.x1 = None
        self.y1 = None
        self.angle0 = angle
        self.angle1 = angle

    def draw(self, ax=None):
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
        if ax is None:
            ax = plt.gca()
        
        angle_rad = np.radians(self.angle0)
        
        self.x1 = self.x0 + self.length * np.cos(angle_rad)
        self.y1 = self.y0 + self.length * np.sin(angle_rad)
        
        ax.plot([self.x0, self.x1], [self.y0, self.y1], color='green')
        
        return self.x1, self.y1


class CurveCourse:
    def __init__(self, length, radius, x0=0, y0=0, angle0=0, id=""):
        self.id = id
        self.connectionStart = None
        self.connectionEnd = None
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

    def draw(self, ax=None):
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
        num_points = 10
        thetas = np.linspace(0, arc_angle_rad, num_points)

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
        ax.plot(cx, cy, marker='o', color='red', markersize=1)
        ax.plot(arc_x, arc_y, color='red')

        # Return final position and angle
        self.angle1 = self.angle0 + np.degrees(arc_angle_rad)
        self.x1 = arc_x[-1]
        self.y1 = arc_y[-1]
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
            x, y = StraightCourse(length, x0=x, y0=y, angle=angle).draw(ax=ax)
            pass
        elif road_type == "Bend":
            length = road[2]
            radius = road[3]
            x, y, angle = CurveCourse(length=length, radius=radius, x0=x, y0=y, 
                                    angle0=angle).draw(ax=ax)
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
