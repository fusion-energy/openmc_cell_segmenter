import numpy as np
import openmc
import matplotlib.pyplot as plt


def segment(cell, number_of_segments, surface_types=['zcylinder']):

    print('segmenting with', surface_types[0])

    groups_of_surfaces = []
    for i, (num_segs, surface_type) in enumerate(zip(number_of_segments, surface_types)):

        surfaces = get_surfaces_for_segmentation(
            cell,
            num_segs,
            surface_type=surface_type
        )
        groups_of_surfaces.append(surfaces)

    for i, surfaces in enumerate(groups_of_surfaces):
        if i == 0:
            segment_of_cells = segment_cell_with_surfaces(
                cell,
                surfaces
            )
        else:
            segment_of_cells = segment_cells_with_surfaces(
                segment_of_cells,
                surfaces
            )




    # for once_segmented_cell in first_segment_of_cells:
    #     new_cells = segment_cell_with_surface(
    #         once_segmented_cell, surfaces
    #     )
        # all_new_cells = all_new_cells + new_cells


    return segment_of_cells

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

def segment_cells_with_surfaces(
        cells,
        surfaces
    ):

    all_segmented_cells = []
    for cell in cells:

        segmented_cells = segment_cell_with_surfaces(
            cell,
            surfaces
        )
        all_segmented_cells= all_segmented_cells+segmented_cells
    return all_segmented_cells


def segment_cell_with_surfaces(
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
