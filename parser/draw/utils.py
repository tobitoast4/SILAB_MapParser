import numpy as np
import math


def convert_angle(value, to='degrees'):
    """
    Convert an angle between radians and degrees.

    Parameters:
        value (float): The angle value to convert.
        to (str): Either 'degrees' or 'radians'.

    Returns:
        float: Converted angle.
    """
    if to == 'degrees':
        return math.degrees(value)
    elif to == 'radians':
        return math.radians(value)
    else:
        raise ValueError("Parameter 'to' must be either 'degrees' or 'radians'.")


def vector_from_points(p1, p2):
    """
    Returns the vector from point p1 to point p2.

    Args:
        p1 (tuple or list or np.array): Starting point (x1, y1).
        p2 (tuple or list or np.array): Ending point (x2, y2).

    Returns:
        np.array: Vector from p1 to p2.
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    return p2 - p1


def vector_from_angle(angle_rad, distance=1.0):
    """
    Returns a 2D vector in the direction of the given angle.

    Args:
        angle_rad (float): The angle in radians (0 is along +x).
        distance (float): Length of the vector (default 1.0 for unit vector).

    Returns:
        np.array: Vector [dx, dy] of the given direction and magnitude.
    """
    dx = np.cos(angle_rad) * distance
    dy = np.sin(angle_rad) * distance
    return np.array([dx, dy])


def angle_from_vector(vector, degrees=True):
    """
    Calculate the angle (in degrees) of a 2D vector from the positive x-axis.

    Parameters:
        vector: tuple or array-like (vx, vy)

    Returns:
        float: angle in degrees, in range (-180, 180]
    """
    vx, vy = vector
    angle_rad = np.arctan2(vy, vx)  # returns angle in radians
    if degrees:
        angle_deg = np.degrees(angle_rad)
        return angle_deg
    else:
        return angle_rad


def translate_perpendicular(point, direction_vector, distance):
    """
    Translates a 2D point by a given distance perpendicular to a direction vector.

    Args:
        point (tuple or list or np.array): The original point (x, y).
        direction_vector (tuple or list or np.array): The direction vector.
        distance (float): Distance to translate the point perpendicular to the direction.

    Returns:
        np.array: The new translated point.
    """
    # Convert to numpy arrays
    point = np.array(point)
    v = np.array(direction_vector)

    # Normalize the direction vector
    v_norm = v / np.linalg.norm(v)

    # Get perpendicular vector (rotate 90 degrees counterclockwise)
    perp = np.array([-v_norm[1], v_norm[0]])
    # perp = np.array([v_norm[1], -v_norm[0]])  # 90° clockwise

    # Translate the point
    new_point = point + distance * perp
    return new_point


def translate(point, offset):
    """
    Translate a 2D point by a given offset.

    Parameters:
        point: tuple (x, y)
        offset: tuple (dx, dy)

    Returns:
        tuple: translated point
    """
    return (point[0] + offset[0], point[1] + offset[1])


def rotate_around(point, center, angle_degrees):
    """
    Rotate a 2D point around another point.

    Parameters:
        point: tuple (x, y)
        center: tuple (cx, cy)
        angle_degrees: float, rotation angle in degrees (counter-clockwise)

    Returns:
        tuple: rotated point
    """
    angle_rad = np.radians(angle_degrees)
    x, y = point
    cx, cy = center

    # Translate point back to origin:
    x -= cx
    y -= cy

    # Rotate point
    x_new = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_new = x * np.sin(angle_rad) + y * np.cos(angle_rad)

    # Translate point back
    return (x_new + cx, y_new + cy)


def blink_line(fig, line, blinks=9, interval=30):
    """Make a line blink by toggling its visibility."""
    visible = True
    count = 0

    def toggle_visibility():
        nonlocal visible, count
        if count >= blinks:
            timer.stop()
            line.set_visible(True)
            fig.canvas.draw()
            return
        visible = not visible
        line.set_visible(visible)
        fig.canvas.draw()
        count += 1

    timer = fig.canvas.new_timer(interval=interval)
    timer.add_callback(toggle_visibility)
    timer.start()