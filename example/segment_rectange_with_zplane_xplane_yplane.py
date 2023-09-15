
import openmc
from openmc_cell_segmenter import segment

# example surfaces
surface_1 = openmc.model.RectangularParallelepiped(
    xmin=20,
    xmax=200,
    ymin=40,
    ymax=400,
    zmin=60,
    zmax=600,
    boundary_type='vacuum'
)

# above (+) inner_sphere_surface and below (-) outer_sphere_surface
region_1 = -surface_1
# region_1 = +inner_sphere_surface & -outer_sphere_surface  

# example cell
cell = openmc.Cell(region=region_1)

cells = segment(cell, [10,10, 10], ['zplane', 'xplane', 'yplane'])
# cells = segment_cell_with_surfaces(cell, [10], ['zcylinder'])

geometry = openmc.Geometry(cells)

plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('seg_rectangle_with_zplane_xplane_yplane_xz.png')

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('seg_rectangle_with_zplane_xplane_yplane_xy.png')

plot = geometry.plot(basis='yz',outline=True)
plot.figure.savefig('seg_rectangle_with_zplane_xplane_yplane_yz.png')
