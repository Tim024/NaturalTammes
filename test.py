import time
import numpy as np
from natural_tammes import natural_tammes

import numpy as np

def calculate_distances(points):
    # Convert points to a NumPy array for efficient computation
    points = np.array(points)
    
    # Calculate all pairwise haversine distances using vectorized operations
    all_distances = np.array([_haversine_vectorized(p1, points) for p1 in points])
    
    # Sort distances for each point and get the 3 closest points (excluding the point itself)
    closest_distances = np.sort(all_distances, axis=1)[:, 1:4]  # Skip the first column as it's the distance to itself

    return closest_distances.flatten()

def _haversine_vectorized(point, all_points):
    """
    Vectorized version of the Haversine formula to calculate distances.
    point: A single (lat, lon) tuple.
    all_points: Array of (lat, lon) tuples.
    """
    # Haversine formula components
    lat1, lon1 = np.radians(point)
    lat2, lon2 = np.radians(all_points).T
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))

    # Radius of Earth in kilometers (can be adjusted for other units)
    r = 6371
    return r * c



if __name__ == "__main__":
    N = 3000

    print(f"N={N}")
    t1 = time.time()
    p1s = natural_tammes(N, init='fibonacci', step=1.0, add_randomness=False)
    d1 = calculate_distances(p1s)
    mean = np.mean(d1)
    std = np.std(d1)
    minimum = np.min(d1)
    print(f"NAT:      (mean,std,min)={mean, std, minimum}\ttime={time.time() - t1}")

    import os
    filename = os.path.join(os.path.dirname(__file__), "data", f"point_f{N}.npy")
    with open(filename, "wb") as f:
        np.save(f, p1s)
