
# Segments OpenMC cells into smaller cells.

Specify the type of segmentation pane desired (XPlane, YPlane, ZPlane or ZCylinder) and the number of segments and obtain segmented cells.

# Example scripts

Example Python scripts can be found in the [examples folder](https://github.com/fusion-energy/openmc_cell_segmenter/tree/main/example).

# Example outputs

In this animation we see an S shaped cell that has been segmented first with XPlanes, YPlanes, ZPlanes and ZCylinders colored by cell.


![openmc cell segmented zplane](https://private-user-images.githubusercontent.com/8583900/268287466-98b2f5ca-7653-4ba4-9d35-4fcd911603f4.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE2OTQ3ODMyNzksIm5iZiI6MTY5NDc4Mjk3OSwicGF0aCI6Ii84NTgzOTAwLzI2ODI4NzQ2Ni05OGIyZjVjYS03NjUzLTRiYTQtOWQzNS00ZmNkOTExNjAzZjQuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQUlXTkpZQVg0Q1NWRUg1M0ElMkYyMDIzMDkxNSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyMzA5MTVUMTMwMjU5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NjY5MGYyZjljZjQ4OTRhODFlNDI2Njk5M2E2YTk5NGZlZGM3YWQ4MTNlMTNiODJhNzhiMDlmNzMyMWZmYTlhYyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.AAVa317fay6zaUrfvTkKNXs24lNA7u6NBzR4-gm5CUU)


# Motivation

Cell segmentation has a variety of use cases.
However, this package was originally made for redefining CSG geometry for cell based shutdown dose rate simulations where separate cells are needed to capture the variation in neutron activation across large cells.
