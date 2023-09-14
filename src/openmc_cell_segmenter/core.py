import openmc
import matplotlib.pyplot as plt

# example surfaces
inner_sphere_surface = openmc.Sphere(r=500, boundary_type='vacuum')
# outer_sphere_surface = openmc.Sphere(r=600)

# above (+) inner_sphere_surface and below (-) outer_sphere_surface
blanket_region = -inner_sphere_surface  
# blanket_region = +inner_sphere_surface & -outer_sphere_surface  

# example cell
cell = openmc.Cell(region=blanket_region)

# makes a universe to cotain all the cells
geometry = openmc.Geometry([cell])  


plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('xz-cell.png')

min_x = cell.bounding_box[0][0]
max_x = cell.bounding_box[1][0]

print(min_x, max_x)

import numpy as np
num_of_segs=5
length_of_segment = max_x/num_of_segs
radiuses = np.linspace(length_of_segment/2, max_x, num_of_segs, endpoint=False)
print(radiuses)

max_x/num_of_segs



surfaces = []
for radius in radiuses:
    surfaces.append(openmc.ZCylinder(r=radius))

new_regions = []
for i, surface in enumerate(surfaces):
    print(surface.id)
    if i == 0:
        print('first surface')
        new_region = cell.region & -surface
        # new_regions.append(new_region)
    else:
        new_region = cell.region & +surfaces[i-1] & -surfaces[i]
    new_regions.append(new_region)
    print(i, cell.region, new_region)

    if i == len(surfaces)-1:
        print('last surface')
        new_region = cell.region & +surface
        new_regions.append(new_region)
        print(i, cell.region, new_region)


cells = []
for region in new_regions:

    cell = openmc.Cell(region=region)
    cells.append(cell)

geometry = openmc.Geometry(cells)  

plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('seg.png')