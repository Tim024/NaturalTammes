import random
from math import radians, cos, sin, asin, sqrt
from pyproj import Geod
from fibonacci import *


# Maybe induce randomness in point movement?
def move_point_away(p1, p2, d, geoid):  # d in km
    # Moves p1 away from p2 by d, return new p1 coordinates
    lat1, lon1 = p1
    lat2, lon2 = p2
    fwd_azimuth, back_azimuth, distance = geoid.inv(lon1, lat1, lon2, lat2)
    # back_azimuth = back_azimuth + np.random.randn()/100
    lng_new, lat_new, return_az = geoid.fwd(lon1, lat1, back_azimuth, d * 1000)
    return lat_new, lng_new


def haversine(p1, p2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return c * r


def natural_tammes(n, init='fibonacci', step=1):
    geoid = Geod(ellps='WGS84')
    # Display n points randomly on map
    points = []
    # Init with fibo by default
    if init == 'fibonacci':
        points = fibonacci(n)
    elif init == 'random':
        for i in range(n):
            lat = random.random() * 180 - 90
            lon = random.random() * 360 - 180
            points.append((lat, lon))
    elif init == 'zeroes':
        for i in range(n):
            lat = random.random()
            lon = random.random()
            points.append((lat, lon))

    def push_around(point_index, radius):
        p1 = points[point_index]
        random_list = list(range(n))
        random_list.remove(point_index)
        if point_index != 0: random_list.remove(0)  # Point 0 is fixed
        random.shuffle(random_list)
        for i in random_list:
            p2 = points[i]
            d = haversine(p1, p2)
            if n * step > radius - d > 0.001:  # If p2 is inside p1 radius
                # Push p2 to edge
                points[i] = move_point_away(p2, p1, radius - d, geoid)
            if radius - d > 20 * step:  # Stop when moving too much ?
                return 0
        return 1

    r = 0
    ok = 1
    while ok == 1:
        r += step
        # Increase radius
        for i in range(n):
            ok *= push_around(i, r)
    return points


if __name__ == '__main__':
    points = natural_tammes(5)
