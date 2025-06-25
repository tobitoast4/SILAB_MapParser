import numpy as np

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

    # Translate the point
    new_point = point + distance * perp
    return new_point


# Example usage
p = (1, 2)
v = (3, 4)
d = 5
translated = translate_perpendicular(p, v, d)
print("Translated point:", translated)
