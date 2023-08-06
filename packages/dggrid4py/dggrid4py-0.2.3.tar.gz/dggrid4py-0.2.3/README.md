# dggrid4py - a Python library to run highlevel functions of DGGRIDv7

[https://pypi.org/project/dggrid4py](https://pypi.org/project/dggrid4py)

GNU AFFERO GENERAL PUBLIC LICENSE

[DGGRID](https://www.discreteglobalgrids.org/software/) is a free software program for creating and manipulating Discrete Global Grids created and maintained by Kevin Sahr. DGGRID version 7.0 was released in September, 2019.

- [DGGRID Version 7.0 on GitHub](https://github.com/sahrk/DGGRID)
- [DGGRID User Manual](https://webpages.sou.edu/~sahrk/docs/dggridManualV70.pdf)


You need the ddgrid tool compiled available on the system.

Besides some lowlevel access influence the dggrid operations' metafile creation, a few highlevel functions are integrated to work with the more comfortable geopython libraries, like shapely and geopandas

- grid_cell_polygons_for_extent(): fill extent/subset with cells at resolution (clip or world)
- grid_cell_polygons_from_cellids(): geometry_from_cellid for dggs at resolution (from id list)
- grid_cellids_for_extent(): get_all_indexes/cell_ids for dggs at resolution (clip or world)
- cells_for_geo_points(): poly_outline for point/centre at resolution


```python
import geopandas
import shapely

from dggrid4py import DGGRIDv7

# create an inital instance that knows where the dggrid tool lives, configure temp workspace and log/stdout output
dggrid_instance = DGGRIDv7(executable='../src/apps/dggrid/dggrid', working_dir='/tmp/grids', capture_logs=False, silent=False)

# global ISEA4T grid at resolution 5 into GeoDataFrame to Shapefile
gdf1 = dggrid_instance.grid_cell_polygons_for_extent('ISEA4T', 5)
print(gdf1.head())
gdf1.to_file('isea4t_5.shp')

# clip extent
clip_bound = shapely.geometry.box(20.2,57.00, 28.4,60.0 )

# ISEA7H grid at resolution 9, for extent of provided WGS84 rectangle into GeoDataFrame to Shapefile
gdf3 = dggrid_instance.grid_cell_polygons_for_extent('ISEA7H', 9, clip_geom=est_bound)
print(gdf3.head())
gdf3.to_file('/tmp/grids/est_shape_isea7h_9.shp')

# generate cell and areal statistics for a ISEA7H grids from resolution 0 to 8 (return a pandas DataFrame)
df1 = dggrid_instance.grid_stats_table('ISEA7H', 8)
print(df1.head(8))
df1.to_csv('isea7h_8_stats.csv', index=False)

# generate the DGGS grid cells that would cover a GeoDataFrame of points, return Polygons with cell IDs as GeoDataFrame
gdf4 = dggrid_instance.cells_for_geo_points(geodf_points_wgs84, False, 'ISEA7H', 5)
print(gdf4.head())
gdf4.to_file('polycells_from_points_isea7h_5.shp')

# generate the DGGS grid cells that would cover a GeoDataFrame of points, return cell IDs added as column to the points GDF
gdf5 = dggrid_instance.cells_for_geo_points(geodf_points_wgs84=geodf_points_wgs84, cell_ids_only=True, dggs_type='ISEA4H', resolution=8)
print(gdf5.head())
gdf5.to_file('geopoint_cellids_from_points_isea4h_8.shp')

# generate DGGS grid cell polygons based on 'cell_id_list' (a list or np.array of provided cell_ids)
gdf6 = dggrid_instance.grid_cell_polygons_from_cellids(cell_id_list=[1, 4, 8], 'ISEA7H', 5)
print(gdf6.head())
gdf6.to_file('from_seqnums_isea7h_5.shp')

```

## TODO:

- get parent_for_cell_id at coarser resolution
- get children_for_cell_id at finer resolution

- sample raster values into dggs cells
- sample vector values into dggs cells

## Related work:

Originally insprired by [dggridR](https://github.com/r-barnes/dggridR), Richard Barnes’ R interface to DGGRID. However, dggridR is directly linked via Rcpp to DGGRID and calls native C/C++ functions.

After some unsuccessful trials with ctypes, cython, CFFI, pybind11 or cppyy (rather due to lack of experience) I found [am2222/pydggrid](https://github.com/am2222/pydggrid) ([on PyPI](https://pypi.org/project/pydggrid/)) which made apparently some initial scaffolding for the transform operation with [pybind11](https://pybind11.readthedocs.io/en/master/) including some sophisticated conda packaging for Windows. This might be worth following up. Interestingly, its todos include "Adding GDAL export Geometry Support" and "Support GridGeneration using DGGRID" which this dggrid4py module supports with integration of GeoPandas.

