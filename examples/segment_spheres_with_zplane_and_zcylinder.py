
import openmc
from openmc_cell_segmenter import segment

# example surfaces
inner_sphere_surface = openmc.Sphere(r=500, boundary_type='vacuum')
inner_sphere_surface2 = openmc.Sphere(r=150, z0=550, boundary_type='vacuum')
# outer_sphere_surface = openmc.Sphere(r=600)

# above (+) inner_sphere_surface and below (-) outer_sphere_surface
blanket_region = -inner_sphere_surface | -inner_sphere_surface2
# blanket_region = +inner_sphere_surface & -outer_sphere_surface  

# example cell
cell = openmc.Cell(region=blanket_region)

cells = segment(cell, [10,10], ['zplane', 'zcylinder'])
# cells = segment_cell_with_surfaces(cell, [10], ['zcylinder'])

geometry = openmc.Geometry(cells)

plot = geometry.plot(basis='xz',outline=True)
plot.figure.savefig('seg_spheres_with_zplane_and_zcylinder_xz.png')

plot = geometry.plot(basis='xy',outline=True)
plot.figure.savefig('seg_spheres_with_zplane_and_zcylinder_xy.png')

plot = geometry.plot(basis='yz',outline=True)
plot.figure.savefig('seg_spheres_with_zplane_and_zcylinder_yz.png')
