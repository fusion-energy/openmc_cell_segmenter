import numpy as np
import openmc
import matplotlib.pyplot as plt
from typing import Sequence, List

def segment(
        cell: openmc.Cell,
        number_of_segments: Sequence[int],
        surface_types: Sequence[str]
    ) -> List[openmc.Cell]:

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

    return segment_of_cells


def get_surfaces_for_segmentation(cell, number_of_segments, surface_type):

    number_of_surfaces = number_of_segments-1
    # if bounding_box==None:
    min_x = cell.bounding_box[0][0]
    max_x = cell.bounding_box[1][0]

    min_y = cell.bounding_box[0][1]
    max_y = cell.bounding_box[1][1]

    min_z = cell.bounding_box[0][2]
    max_z = cell.bounding_box[1][2]

    x_width_of_segment = abs(min_x-max_x)/number_of_surfaces
    y_width_of_segment = abs(min_y-max_y)/number_of_surfaces
    z_width_of_segment = abs(min_z-max_z)/number_of_surfaces

    if surface_type == 'zcylinder':
        
        start = min(min_x, min_y)
        end = max(max_x, max_y)

        width_of_segment = (abs(end-start)/2)/(number_of_surfaces-0.5)

        # inner surface is double of the width
        # 0-----50----------100----------200
        radiuses = np.linspace(width_of_segment/2, end, number_of_surfaces, endpoint=False)

    elif surface_type == 'zplane':
        radiuses = np.linspace(min_z+z_width_of_segment, max_z, number_of_surfaces, endpoint=False)
    elif surface_type == 'xplane':
        radiuses = np.linspace(min_x+x_width_of_segment, max_x, number_of_surfaces, endpoint=False)
    elif surface_type == 'yplane':
        radiuses = np.linspace(min_y+y_width_of_segment, max_y, number_of_surfaces, endpoint=False)

    print('radiuses',radiuses)
    surfaces = []
    for radius in radiuses:
        if surface_type == 'zcylinder':
            surfaces.append(openmc.ZCylinder(r=radius))
        if surface_type == 'zplane':
            surfaces.append(openmc.ZPlane(z0=radius))
        if surface_type == 'xplane':
            surfaces.append(openmc.XPlane(x0=radius))
        if surface_type == 'yplane':
            surfaces.append(openmc.YPlane(y0=radius))
    
    return surfaces


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

            if i == 0:
                new_region = cell.region & -surface
            else:
                new_region = cell.region & +surfaces[i-1] & -surfaces[i]
            new_regions.append(new_region)

            if i == len(surfaces)-1:
                new_region = cell.region & +surface
                new_regions.append(new_region)

    cells = []
    for region in new_regions:

        cell = openmc.Cell(region=region)
        cells.append(cell)
    return cells
