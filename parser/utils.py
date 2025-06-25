import numpy as np

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
