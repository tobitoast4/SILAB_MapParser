import numpy as np
import matplotlib.pyplot as plt

try:
    from draw import utils
except:
    import utils

NUM_POINTS = 100
SHOW_LABELS = True



class Area2:
    def __init__(self, id=""):
        self.id = id
        self.parts = []


class StraightAED:
    def __init__(self, x0, y0, x1, y1, id="", parent=None):
        self.id = id 
        self.parent = parent
        self.connectionStart = None
        self.connectionEnd = None
        self.x0 = x0 
        self.y0 = y0 
        self.x1 = x1 
        self.y1 = y1
        v1 = utils.vector_from_points((x0, y0), (x1, y1))
        angle = utils.angle_from_vector(v1)
        self.angle0 = angle
        self.angle1 = angle

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
        return self

    def calculate(self, ax=None):
        if ax:
            line, = ax.plot([self.x0, self.x1], [self.y0, self.y1], color='blue')
            
            if SHOW_LABELS:
                ax.text((self.x0+self.x1)//2, (self.y0+self.y1)//2, self.id, color='blue', va='center', fontsize=7)
        return line
    

class CircularArcAED:
    def __init__(self, x0, y0, angle0, angle1, r, id="", parent=None):
        self.id = id 
        self.parent = parent
        self.connectionStart = None
        self.connectionEnd = None
        self.x0 = x0
        self.y0 = y0
        self.x1 = None
        self.y1 = None
        self.angle0 = angle0
        self.angle1 = angle1
        self.r = r
        # Normalize angles to ensure correct sweep direction
        if self.angle1 < self.angle0:
            self.angle1 += 2 * np.pi

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
        angle_rad = utils.convert_angle(angle_deg, to="radians")
        self.angle0 += angle_rad
        self.angle1 += angle_rad
        return self

    def calculate(self, ax=None):
        # Generate the points (we dont need them now for drwaing, but later)
        angles = np.linspace(self.angle0, self.angle1, NUM_POINTS)
        arc_x = self.x0 + self.r * np.cos(angles)
        arc_y = self.y0 + self.r * np.sin(angles)

        # Plot the arc
        if ax:
            line, = ax.plot(arc_x, arc_y, 'b-')
            if SHOW_LABELS:
                ax.text(arc_x[len(arc_x)//2], arc_y[len(arc_y)//2], self.id, color='blue', va='center', fontsize=7)
            ax.plot(self.x0, self.y0, 'k+')  # center
        
        ## Optionally: Plot start and end of circular arc
        # ax.plot(arc_x[0], arc_y[0], 'go')
        # ax.plot(arc_x[-1], arc_y[-1], 'ro')
        self.x1 = arc_x[len(arc_x)-1]
        self.y1 = arc_y[len(arc_y)-1]
        return line


class HermiteSplineAED:
    def __init__(self, x0, y0, angle0, x1, y1, angle1, id="", parent=None):
        self.id = id 
        self.parent = parent
        self.connectionStart = None
        self.connectionEnd = None
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.angle0 = angle0
        self.angle1 = angle1

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
        angle_rad = utils.convert_angle(angle_deg, to="radians")
        self.angle0 += angle_rad
        self.angle1 += angle_rad
        return self

    def calculate(self, ax=None):
        tangent_scale=1  # we assume this to be 1 (TODO: maybe clarify if this is correct)
        # Convert angles to radians if not already
        theta0 = self.angle0
        theta1 = self.angle1

        # Compute distance between points
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
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
            point = (h00 * np.array([self.x0, self.y0]) +
                    h10 * T0 +
                    h01 * np.array([self.x1, self.y1]) +
                    h11 * T1)
            curve.append(point)

        curve = np.array(curve)

        # Plotting
        if ax:
            line, = ax.plot(curve[:, 0], curve[:, 1], color='purple')
            if SHOW_LABELS:
                ax.text(curve[len(curve)//2][0], curve[len(curve)//2][1], self.id, color='purple', va='center', fontsize=7)
        # ax.plot([x0, x1], [y0, y1], 'ro--', label='Endpoints')
        # ax.quiver(x0, y0, T0[0], T0[1], angles='xy', scale_units='xy', scale=1, color='green')  # label='Start Tangent'
        # ax.quiver(x1, y1, T1[0], T1[1], angles='xy', scale_units='xy', scale=1, color='purple') # label='End Tangent'
        return line



if __name__ == "__main__":
    fig, ax = plt.subplots()

    x0 = -38.0111
    y0 = 51.1016
    x1 = -30.1935
    y1 = 39.8262
    StraightAED(x0, y0, x1, y1).calculate(ax=ax)

    x0 = 1.01226
    y0 = -5.37267
    angle0 = 2.82934
    angle1 = 1.59937
    r = 18.3512
    CircularArcAED(x0, y0, angle0, angle1, r).calculate(ax=ax)

    HermiteSplineAED( x0=0, y0=0, angle0=0, x1=25, y1=25, angle1=3.1415/2).calculate(ax=ax)
    HermiteSplineAED( x0=50, y0=50, angle0=0, x1=75, y1=75, angle1=0).calculate(ax=ax)


    # Final formatting
    ax.set_aspect('equal')
    ax.grid(True)
    ax.legend()
    plt.title("SILAB Map")
    plt.show()
