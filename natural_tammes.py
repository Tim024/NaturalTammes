import random
from math import pi, atan2, asin
from pyproj import Geod
from typing import List, Tuple
import numpy as np

_phi = pi * (3.0 - np.sqrt(5.0))  # golden angle in radians

def _fibonacci(n: int=1) -> List[Tuple[float, float]]:
    """ Returns n points on a sphere using the Fibonacci spiral method. """
    i = np.arange(0, n)
    y = 1 - (i / float(n - 1)) * 2  # y goes from 1 to -1
    radius = np.sqrt(1 - y * y)
    theta = _phi * i
    x, z = np.cos(theta) * radius, np.sin(theta) * radius
    lat = np.degrees(np.arcsin(z))
    lon = np.degrees(np.arctan2(y, x))
    return list(zip(lat, lon))


def _move_point_away(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    d: float,
    geoid: Geod,
    add_randomness=False,
):
    """
    Moves p1 away from p2 by distance d using the geoid for calculations.
    If add_randomness is True, adds a small random angle to the movement.
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
    _, back_azimuth, _ = geoid.inv(lon1, lat1, lon2, lat2)

    if add_randomness:
        back_azimuth += random.uniform(-0.01, 0.01)

    lng_new, lat_new, _ = geoid.fwd(lon1, lat1, back_azimuth, d * 1000)
    return lat_new, lng_new

def _haversine_vectorized(all_points):
    lat, lon = np.radians(np.array(all_points)).T
    deltas = lat[:, np.newaxis] - lat
    deltal = lon[:, np.newaxis] - lon
    a = np.sin(deltas / 2.0) ** 2 + np.cos(lat) * np.cos(lat[:, np.newaxis]) * np.sin(deltal / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c  # Distance matrix

def _min_distance(distances):
    return np.min(distances + np.diag([np.inf] * len(distances)))

def natural_tammes(n, init="fibonacci", step=1, add_randomness=False):
    geoid = Geod(ellps="WGS84")
    if init == "fibonacci":
        points = _fibonacci(n)
    elif init in ["random", "zeroes"]:
        points = [(random.uniform(-90, 90), random.uniform(-180, 180)) for _ in range(n)]
    else:
        raise ValueError('init must be one of "fibonacci", "random" or "zeroes"')

    fixed_point_index = random.choice(range(n))
    distances = _haversine_vectorized(points)
    radius = _min_distance(distances)

    end_loop = False
    while not end_loop:
        for i in range(n):
            for j in range(n):
                if j == fixed_point_index or i == j:
                    continue
                if distances[i, j] < radius:
                    move_distance = radius - distances[i, j]
                    points[j] = _move_point_away(points[j], points[i], move_distance, geoid, add_randomness)

                    if move_distance > 10 * step: # Exit loop if one point starts moving a lot (Chaos behavior)
                        end_loop = True
                        break
            if end_loop:
                break
        if end_loop:
            break

        new_distances = _haversine_vectorized(points)

        radius += step
        distances = new_distances

    return points
