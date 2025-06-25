import numpy as np
import math
import matplotlib.pyplot as plt

roads = [
    ["Straight", 100],
    ["Bend", 157, 100],
    ["Bend", 157, -100],
    ["Straight", 300],
    ["Bend",  1500, -500],
    ["Bend",  340, -200],
    ["Straight", 3000],
]

def draw_straight(length, start_x=0, start_y=0, angle_deg=0, ax=None):
    """
    Draws a straight line of the given length and direction.
    
    Parameters:
        length: Length of the straight segment
        start_x, start_y: Starting coordinates
        angle_deg: Direction in degrees (0 = right, 90 = up)
        ax: Matplotlib axis (optional)
    
    Returns:
        (end_x, end_y): End coordinates
    """
    if ax is None:
        ax = plt.gca()
    
    angle_rad = np.radians(angle_deg)
    
    end_x = start_x + length * np.cos(angle_rad)
    end_y = start_y + length * np.sin(angle_rad)
    
    ax.plot([start_x, end_x], [start_y, end_y], color='green')
    
    return end_x, end_y



def draw_curve(length, radius, direction='right', start_x=0, start_y=0, start_angle_deg=0, ax=None):
    """
    Draws a circular arc with a given length and radius.
    - direction: 'right' or 'left'
    - start_angle_deg: initial heading angle in degrees (0 = pointing right)
    Returns the end (x, y) and new heading angle.
    """
    # Arc angle in radians: arc_length = radius * angle
    radius = abs(radius)
    arc_angle_rad = length / radius
    if direction == 'right':
        arc_angle_rad = -arc_angle_rad

    # Generate theta values
    num_points = 10
    thetas = np.linspace(0, arc_angle_rad, num_points)

    # Start angle in radians
    start_angle_rad = np.radians(start_angle_deg)

    if direction == "right":
        cx = start_x - math.cos(np.pi/2 + start_angle_rad) * radius
        cy = start_y - math.sin(np.pi/2 + start_angle_rad) * radius
        arc_x = cx + abs(radius) * np.cos(thetas + start_angle_rad + np.pi/2)
        arc_y = cy + abs(radius) * np.sin(thetas + start_angle_rad + np.pi/2)
    else:
        cx = start_x + math.cos(np.pi/2 + start_angle_rad) * radius
        cy = start_y + math.sin(np.pi/2 + start_angle_rad) * radius
        arc_x = cx + abs(radius) * np.cos(thetas - (np.pi/2 - start_angle_rad))
        arc_y = cy + abs(radius) * np.sin(thetas - (np.pi/2 - start_angle_rad))
    ax.plot(cx, cy, color='red', marker='o', markersize=1)

    ax.plot(arc_x, arc_y)

    # Return final position and angle
    end_angle_deg = start_angle_deg + np.degrees(arc_angle_rad)
    return arc_x[-1], arc_y[-1], end_angle_deg



fig, ax = plt.subplots()

angle = 90
x = 0
y = 0

for road in roads:
    road_type = road[0]
    if road_type == "Straight":
        length = road[1]
        x, y = draw_straight(length, start_x=x, start_y=y, angle_deg=angle, ax=ax)
        pass
    elif road_type == "Bend":
        length = road[1]
        radius = road[2]
        if radius < 0:
            direction = "left"
        else: 
            direction = "right"
        x, y, angle = draw_curve(length=length, radius=radius, direction=direction, 
                                 start_x=x, start_y=y, start_angle_deg=angle, ax=ax)
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
