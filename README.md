[![CI with install](https://github.com/fusion-energy/openmc_cell_segmenter/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/openmc_cell_segmenter/actions/workflows/ci_with_install.yml)

# Segments OpenMC cells into smaller cells.

Specify the type of segmentation pane desired (XPlane, YPlane, ZPlane or ZCylinder) and the number of segments and obtain segmented cells.

# Example scripts

Example Python scripts can be found in the [examples folder](https://github.com/fusion-energy/openmc_cell_segmenter/tree/main/example).

# Example outputs

In this animation we see an S shaped cell that has been segmented first with XPlanes, YPlanes, ZPlanes and ZCylinders colored by cell.


![openmc cell segmented zplane](https://user-images.githubusercontent.com/8583900/268407842-6e8783b4-1bc6-443e-ab01-ec390ae3dfe2.gif)


# Motivation

Cell segmentation has a variety of use cases.
However, this package was originally made for redefining CSG geometry for cell based shutdown dose rate simulations where separate cells are needed to capture the variation in neutron activation across large cells.
