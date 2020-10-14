import math
import numpy as np


def fibonacci(n=1):
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians
    for i in range(n):
        y = 1 - (i / float(n - 1)) * 2  # y goes from 1 to -1
        x = math.cos(phi * i) * math.sqrt(1 - y * y)
        z = math.sin(phi * i) * math.sqrt(1 - y * y)
        lat = np.degrees(np.arcsin(z / 1))
        lon = np.degrees(np.arctan2(y, x))
        points.append((lat, lon))
    return points
