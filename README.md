# A nature-inspired solution to the Tammes Problem

The [Tammes problem](https://en.wikipedia.org/wiki/Tammes_problem) consists in finding a *n* points distribution arrangement on a sphere such that the minimum distance between the points is maximized.

This python code a simple yet efficient solution to the problem:
1. *n* points are scattered around the sphere. We initialize using the fibonacci distribution.
2. Each points starts with a radius *r=0*
3. We incrementally increase the radius of all points by a small amount (*r+=step*)
4. The radius pushes other points away
5. The algorithm stops when increasing the radius generates to much movements (edge of chaos)

The key challenges are:
1. __Stopping at the right time.__ Indeed, when initializing the points randomly, we sometimes observe chaotic behavior followed by stabilization. It could be that monitoring the nodes movement is not the correct approach. 
2. __Computation times.__ This code is not optimized and parallel computations could improve the computation times. However, even with computational power its current complexity does not scale well with *n*.

# Results

The algorithm presents significant lower variance compared to the fibonacci distribution, at a cost of computation time.
Pre-computed results are available in the data folder.

Results with N=100:
![results-100](visualisations/output100.gif)

Results with N=1000:
![results-100](visualisations/output1000.gif)