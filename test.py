if __name__ == '__main__':
    import time
    import numpy as np
    from natural_tammes import natural_tammes, haversine
    from fibonacci import fibonacci


    def calculate_distances(points):
        all_distances = []
        for p1 in points:
            min_dist = 1000000
            for p2 in points:
                d = haversine(p1, p2)
                if d < min_dist and d != 0: min_dist = d
            all_distances.append(min_dist)
        return all_distances


    N = 50
    print(f"N={N}")
    t1 = time.time()
    p1s = natural_tammes(N)
    d1 = calculate_distances(p1s)
    m, s = np.mean(d1), np.std(d1)
    print(f"NAT:      (mean,std)={m, s}\ttime={time.time() - t1}")
    t1 = time.time()
    p3s = fibonacci(N)
    d3 = calculate_distances(p3s)
    m, s = np.mean(d3), np.std(d3)
    print(f"Fibo:     (mean,std)={m, s}\ttime={time.time() - t1}")
