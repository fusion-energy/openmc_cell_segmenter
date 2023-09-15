
# This example was just used for the readme image.
# It would need vacuum surfaces and voids for transport.

import openmc
from openmc_cell_segmenter import segment


surf_s_left = openmc.XPlane(x0=0)
surf_s_mid_left = openmc.XPlane(x0=2)
surf_s_mid_right = openmc.XPlane(x0=8)
surf_s_right = openmc.XPlane(x0=10)

surf_s_bottom = openmc.YPlane(y0=0)
surf_s_upper_bottom = openmc.YPlane(y0=4)
surf_s_lower_midy = openmc.YPlane(y0=8)
surf_s_upper_midy = openmc.YPlane(y0=12)
surf_s_lower_top = openmc.YPlane(y0=16)
surf_s_top = openmc.YPlane(y0=20)

surf_z_back = openmc.ZPlane(z0=-1)
surf_z_front = openmc.ZPlane(z0=1)

lower_region = +surf_s_left & -surf_s_right & +surf_s_bottom & -surf_s_upper_bottom & +surf_z_back & -surf_z_front
lower_upper_region = +surf_s_mid_right & -surf_s_right & +surf_s_upper_bottom & -surf_s_lower_midy & +surf_z_back & -surf_z_front
mid_region = +surf_s_left & -surf_s_right & +surf_s_lower_midy & -surf_s_upper_midy & +surf_z_back & -surf_z_front
upper_lower_region = -surf_s_mid_left & +surf_s_left & +surf_s_upper_midy & -surf_s_lower_top & +surf_z_back & -surf_z_front
upper_region = +surf_s_left & -surf_s_right & +surf_s_lower_top & -surf_s_top & +surf_z_back & -surf_z_front

all_regions = lower_region | mid_region
all_regions = all_regions | lower_upper_region
all_regions = all_regions | upper_lower_region
all_regions = all_regions | upper_region

cell = openmc.Cell(region=all_regions)

geometry = openmc.Geometry([cell])

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('letter_s_csg_xy.png',  bbox_inches="tight")

segmented_cells = segment(cell, [10,10, 10], ['zplane', 'xplane', 'yplane'])

geometry = openmc.Geometry(segmented_cells)

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('letter_s_csg_xyz_xy.png',  bbox_inches="tight")

segmented_cells = segment(cell, [10], ['yplane'])

geometry = openmc.Geometry(segmented_cells)

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('letter_s_csg_y_xy.png',  bbox_inches="tight")

segmented_cells = segment(cell, [10], ['xplane'])

geometry = openmc.Geometry(segmented_cells)

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('letter_s_csg_x_xy.png',  bbox_inches="tight")

segmented_cells = segment(cell, [10], ['zcylinder'])

geometry = openmc.Geometry(segmented_cells)

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('letter_s_csg_zcy_xy.png',  bbox_inches="tight")
