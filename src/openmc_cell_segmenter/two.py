import numpy as np
import openmc
import matplotlib.pyplot as plt


def segment_cell_with_surfaces(cell, number_of_segments, surface_types=['zcylinder']):

    for surface_type in surface_types:
        print('segmenting with', surface_type)
    first_segment_of_cells = segment_cell_with_surface(
        cell,
        number_of_segments,
        surface_type=surface_types[0]
    )

    all_new_cells = []
    for once_segmented_cell in first_segment_of_cells:
        new_cells = segment_cell_with_surface(
            once_segmented_cell,
            number_of_segments,
            surface_type=surface_types[1],
            bounding_box=cell.bounding_box
        )
        all_new_cells = all_new_cells + new_cells


    return all_new_cells


def segment_cell_with_surface(
        cell,
        number_of_segments,
        surface_type='zcylinder',
        bounding_box=None
    ):

    if bounding_box==None:
        min_x = cell.bounding_box[0][0]
        max_x = cell.bounding_box[1][0]

        min_z = cell.bounding_box[0][0]
        max_z = cell.bounding_box[1][0]
    elif bounding_box:
        min_x = bounding_box[0][0]
        max_x = bounding_box[1][0]

        min_z = bounding_box[0][0]
        max_z = bounding_box[1][0]

    # print(min_x, max_x)
    x_width_of_segment = abs(min_x-max_x)/number_of_segments
    z_width_of_segment = abs(min_z-max_z)/number_of_segments
    print('z_width_of_segment',z_width_of_segment)

    if surface_type == 'zcylinder':
        x_width_of_segment = max_x/number_of_segments
        z_width_of_segment = max_z/number_of_segments
        # todo check if max_y is larger than max_x
        radiuses = np.linspace(x_width_of_segment/2, max_x, number_of_segments, endpoint=False)
        # print('segmentation', radiuses)
    if surface_type == 'zplane':
        radiuses = np.linspace(min_z+z_width_of_segment, max_z, number_of_segments, endpoint=False)

    print('radiuses',radiuses)
    surfaces = []
    for radius in radiuses:
        if surface_type == 'zcylinder':
            surfaces.append(openmc.ZCylinder(r=radius))
        if surface_type == 'zplane':
            surfaces.append(openmc.ZPlane(z0=radius))

    new_regions = []
    for i, surface in enumerate(surfaces):
        if i == 0:
            # print('first segmenting surface')
            new_region = cell.region & -surface
        else:
            new_region = cell.region & +surfaces[i-1] & -surfaces[i]
        new_regions.append(new_region)
        # print(i, new_region)

        if i == len(surfaces)-1:
            # print('last segmenting surface')
            new_region = cell.region & +surface
            new_regions.append(new_region)
            # print(i, new_region)


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

cells = segment_cell_with_surfaces(cell, 5, ['zcylinder', 'zplane'])

geometry = openmc.Geometry(cells)  

plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('seg_xz.png')

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('seg_xy.png')

plot = geometry.plot(basis='yz',outline=True)
plot.figure.savefig('seg_yz.png')