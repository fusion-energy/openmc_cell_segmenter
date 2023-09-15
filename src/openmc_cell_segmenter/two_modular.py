import numpy as np
import openmc
import matplotlib.pyplot as plt


def segment_cell_with_surfaces(cell, number_of_segments, surface_types=['zcylinder']):

    print('segmenting with', surface_types[0])

    surfaces = get_surfaces_for_segmentation(
        cell,
        number_of_segments[0],
        surface_type=surface_types[0]
    )

    first_segment_of_cells = segment_cell_with_surface(
        cell,
        surfaces
    )
    return first_segment_of_cells

    # print('segmenting with', surface_types[1])

    # surfaces = get_surfaces_for_segmentation(
    #     cell,
    #     number_of_segments[1],
    #     surface_type=surface_types[1]
    # )

    # all_new_cells = []
    # for once_segmented_cell in first_segment_of_cells:
    #     new_cells = segment_cell_with_surface(
    #         once_segmented_cell, surfaces
    #     )
    #     all_new_cells = all_new_cells + new_cells


    # return all_new_cells

def get_surfaces_for_segmentation(cell, number_of_segments, surface_type):

    # if bounding_box==None:
    min_x = cell.bounding_box[0][0]
    max_x = cell.bounding_box[1][0]

    min_y = cell.bounding_box[0][1]
    max_y = cell.bounding_box[1][1]

    min_z = cell.bounding_box[0][2]
    max_z = cell.bounding_box[1][2]
    # elif bounding_box:
        # min_x = bounding_box[0][0]
        # max_x = bounding_box[1][0]

        # min_z = bounding_box[0][0]
        # max_z = bounding_box[1][0]

    # print(min_x, max_x)
    x_width_of_segment = abs(min_x-max_x)/number_of_segments
    y_width_of_segment = abs(min_y-max_y)/number_of_segments
    z_width_of_segment = abs(min_z-max_z)/number_of_segments
    print('z_width_of_segment',z_width_of_segment)

    if surface_type == 'zcylinder':
        
        start = min(min_x, min_y)
        end = max(max_x, max_y)

        print('abs(end-start)',abs(end-start)/2)
        width_of_segment = (abs(end-start)/2)/(number_of_segments-0.5)

        # inner surface is double of the width
        # 0-----50----------100----------200
        print('width_of_segment',width_of_segment)
        radiuses = np.linspace(width_of_segment/2, end, number_of_segments, endpoint=False)
        # print('segmentation', radiuses)
    elif surface_type == 'zplane':
        radiuses = np.linspace(min_z+z_width_of_segment, max_z, number_of_segments, endpoint=False)

    print('radiuses',radiuses)
    surfaces = []
    for radius in radiuses:
        if surface_type == 'zcylinder':
            surfaces.append(openmc.ZCylinder(r=radius))
        if surface_type == 'zplane':
            surfaces.append(openmc.ZPlane(z0=radius))
    
    return surfaces

# def check_surface_is_within_cell(cell, surface):
#     if isinstance(surface, openmc.ZCylinder):
#         if surface.r > cell.bounding_box[0][0] and surface.r < cell.bounding_box[1][0]:
#             print('surface' surface.r, )
#             return True
#         if surface.r > cell.bounding_box[0][1] and surface.r < cell.bounding_box[1][1]:
#             return True
#     if isinstance(surface, openmc.ZPlane):
#         if surface.z0 > cell.bounding_box[0][2] and surface.z0 < cell.bounding_box[1][2]:
#             return True
#     print('  surface not in cell')
#     return False


def segment_cell_with_surface(
        cell,
        surfaces
    ):

    new_regions = []
    for i, surface in enumerate(surfaces):
        # print('trying surface', i)
        # if check_surface_is_within_cell(cell, surface):

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
inner_sphere_surface2 = openmc.Sphere(r=150, z0=550, boundary_type='vacuum')
# outer_sphere_surface = openmc.Sphere(r=600)

# above (+) inner_sphere_surface and below (-) outer_sphere_surface
blanket_region = -inner_sphere_surface | -inner_sphere_surface2
# blanket_region = +inner_sphere_surface & -outer_sphere_surface  

# example cell
cell = openmc.Cell(region=blanket_region)

# cells = segment_cell_with_surfaces(cell, [10,10], ['zcylinder', 'zplane'])
cells = segment_cell_with_surfaces(cell, [10], ['zcylinder'])

geometry = openmc.Geometry(cells)  

plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('seg_xz.png')

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('seg_xy.png')

plot = geometry.plot(basis='yz',outline=True)
plot.figure.savefig('seg_yz.png')

