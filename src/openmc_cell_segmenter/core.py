import numpy as np
import openmc
import matplotlib.pyplot as plt

def segment_with_z_cylinder_surface(cell, number_of_segments):

    min_x = cell.bounding_box[0][0]
    max_x = cell.bounding_box[1][0]

    print(min_x, max_x)

    length_of_segment = max_x/number_of_segments
    radiuses = np.linspace(length_of_segment/2, max_x, number_of_segments, endpoint=False)
    print('segmentation', radiuses)

    surfaces = []
    for radius in radiuses:
        surfaces.append(openmc.ZCylinder(r=radius))

    new_regions = []
    for i, surface in enumerate(surfaces):
        if i == 0:
            print('first segmenting surface')
            new_region = cell.region & -surface
        else:
            new_region = cell.region & +surfaces[i-1] & -surfaces[i]
        new_regions.append(new_region)
        print(i, new_region)

        if i == len(surfaces)-1:
            print('last segmenting surface')
            new_region = cell.region & +surface
            new_regions.append(new_region)
            print(i, new_region)


    cells = []
    for region in new_regions:

        cell = openmc.Cell(region=region)
        cells.append(cell)
    return cells



# example surfaces
inner_sphere_surface = openmc.Sphere(r=500, boundary_type='vacuum')
# outer_sphere_surface = openmc.Sphere(r=600)

# above (+) inner_sphere_surface and below (-) outer_sphere_surface
blanket_region = -inner_sphere_surface  
# blanket_region = +inner_sphere_surface & -outer_sphere_surface  

# example cell
cell = openmc.Cell(region=blanket_region)

cells = segment_with_z_cylinder_surface(cell, 15)

geometry = openmc.Geometry(cells)  

plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('seg.png')
plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('seg_xy.png')