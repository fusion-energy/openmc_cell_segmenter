
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

def test_correct_number_of_segments():
    cells = segment(cell, [3], ['yplane'])
    assert len(cells) == 3

    cells = segment(cell, [3], ['xplane'])
    assert len(cells) == 3

    cells = segment(cell, [3], ['zplane'])
    assert len(cells) == 3

    cells = segment(cell, [3], ['zcylinder'])
    assert len(cells) == 3

    cells = segment(cell, [3,7], ['zplane', 'xplane'])
    assert len(cells) == 3*7

    cells = segment(cell, [3,7, 9], ['zplane', 'xplane', 'yplane'])
    assert len(cells) == 3*7*9

    cells = segment(cell, [3,7, 9], ['zcylinder', 'xplane', 'yplane'])
    assert len(cells) == 3*7*9

def test_in_transport():

    material = openmc.Material()
    material.add_nuclide("Fe56", 1)
    material.set_density("g/cm3", 0.1)
    my_materials = openmc.Materials([material])

    cells = segment(cell, [3,4], ['zcylinder', 'zplane'])
    my_geometry = openmc.Geometry(cells)

    my_source = openmc.IndependentSource()

    my_source.space = openmc.stats.Point(cell.bounding_box.center)

    # sets the direction to isotropic
    my_source.angle = openmc.stats.Isotropic()

    my_settings = openmc.Settings()
    # my_settings.inactive = 0
    my_settings.run_mode = "fixed source"
    my_settings.batches = 10
    my_settings.particles = 100000
    my_settings.source = my_source

    model = openmc.model.Model(my_geometry, my_materials, my_settings)
    model.run()