import numpy as np
import matplotlib.pyplot as plt

NUM_POINTS = 100
SHOW_LABELS = True

def aed_draw_straight(x0, y0, x1, y1, ax=None, custom_label=""):
    line, = ax.plot([x0, x1], [y0, y1], color='blue')
    
    if SHOW_LABELS:
        ax.text((x0+x1)//2, (y0+y1)//2, custom_label, color='blue', va='center', fontsize=7)
    return line

def aed_draw_circular_arc(x0, y0, angle0, angle1, r, ax=None, custom_label=""):
    # Normalize angles to ensure correct sweep direction
    if angle1 < angle0:
        angle1 += 2 * np.pi

    # Generate the points (we dont need them now for drwaing, but later)
    angles = np.linspace(angle0, angle1, NUM_POINTS)
    arc_x = x0 + r * np.cos(angles)
    arc_y = y0 + r * np.sin(angles)

    # Plot the arc
    line, = ax.plot(arc_x, arc_y, 'b-')
    if SHOW_LABELS:
        ax.text(arc_x[len(arc_x)//2], arc_y[len(arc_y)//2], custom_label, color='blue', va='center', fontsize=7)
    ax.plot(x0, y0, 'k+')  # center
    
    ## Optionally: Plot start and end of circular arc
    # ax.plot(arc_x[0], arc_y[0], 'go')
    # ax.plot(arc_x[-1], arc_y[-1], 'ro')
    return line

def aed_plot_hermite_spline(x0, y0, angle0, x1, y1, angle1, ax=None, custom_label=""):
    tangent_scale=1  # we assume this to be 1 (TODO: maybe clarify if this is correct)
    # Convert angles to radians if not already
    theta0 = angle0
    theta1 = angle1

    # Compute distance between points
    dx = x1 - x0
    dy = y1 - y0
    distance = np.hypot(dx, dy)
    tangent_length = tangent_scale * distance

    # Compute tangent vectors from angles and scaled magnitude
    T0 = tangent_length * np.array([np.cos(theta0), np.sin(theta0)])
    T1 = tangent_length * np.array([np.cos(theta1), np.sin(theta1)])

    # Hermite basis functions
    def hermite(t):
        h00 = 2*t**3 - 3*t**2 + 1
        h10 = t**3 - 2*t**2 + t
        h01 = -2*t**3 + 3*t**2
        h11 = t**3 - t**2
        return h00, h10, h01, h11

    # Generate the spline points
    t_values = np.linspace(0, 1, NUM_POINTS)
    curve = []
    for t in t_values:
        h00, h10, h01, h11 = hermite(t)
        point = (h00 * np.array([x0, y0]) +
                 h10 * T0 +
                 h01 * np.array([x1, y1]) +
                 h11 * T1)
        curve.append(point)

    curve = np.array(curve)

    # Plotting
    line, = ax.plot(curve[:, 0], curve[:, 1], color='purple')
    if SHOW_LABELS:
        ax.text(curve[len(curve)//2][0], curve[len(curve)//2][1], custom_label, color='purple', va='center', fontsize=7)
    # ax.plot([x0, x1], [y0, y1], 'ro--', label='Endpoints')
    # ax.quiver(x0, y0, T0[0], T0[1], angles='xy', scale_units='xy', scale=1, color='green')  # label='Start Tangent'
    # ax.quiver(x1, y1, T1[0], T1[1], angles='xy', scale_units='xy', scale=1, color='purple') # label='End Tangent'
    return line



# fig, ax = plt.subplots()

# x0 = -38.0111
# y0 = 51.1016
# x1 = -30.1935
# y1 = 39.8262
# aed_draw_straight(x0, y0, x1, y1, ax)

# x0 = 1.01226
# y0 = -5.37267
# angle0 = 2.82934
# angle1 = 1.59937
# r = 18.3512
# aed_draw_circular_arc(x0, y0, angle0, angle1, r, ax)

# x0 = 1.01226
# y0 = -5.37267
# Angle0 = -1.52143
# Angle1 = -2.67153
# r = 18.3512
# aed_draw_circular_arc(x0, y0, angle0, angle1, r, ax)

# x0 = 1.01226
# y0 = -5.37267
# Angle0 = -0.336225
# Angle1 = -1.52143
# r = 18.3512
# aed_draw_circular_arc(x0, y0, angle0, angle1, r, ax)

# # Example usage with your data:
# aed_plot_hermite_spline( x0=0, y0=0, angle0=0, x1=25, y1=25, angle1=3.1415/2, ax=ax)


# Final formatting
# ax.set_aspect('equal')
# ax.grid(True)
# ax.legend()
# plt.title("SILAB Map")
# plt.show()
