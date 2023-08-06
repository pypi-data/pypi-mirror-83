# -*- coding: utf-8 -*-

from pathlib import Path
import uuid
import shutil
import os
import sys
import subprocess
import traceback
import tempfile
import numpy as np
import pandas as pd

import fiona
from fiona.crs import from_epsg

import geopandas as gpd

import shapely
from shapely.geometry import Polygon, box, shape


# specify a ISEA3H
dggs_types = ( 
    'CUSTOM',  # parameters will be specified manually
    'SUPERFUND', # Superfund_500m grid
    'PLANETRISK',
    'ISEA3H', # ISEA projection with hexagon cells and an aperture of 3
    'ISEA4H', # ISEA projection with hexagon cells and an aperture of 4
    'ISEA4T',  # ISEA projection with triangle cells and an aperture of 4
    'ISEA4D', # ISEA projection with diamond cells and an aperture of 4
    'ISEA43H', # ISEA projection with hexagon cells and a mixed sequence of aperture 4 resolutions followed by aperture 3 resolutions
    'ISEA7H', # ISEA projection with hexagon cells and an aperture of 7
    'FULLER3H', # FULLER projection with hexagon cells and an aperture of 3
    'FULLER4H', # FULLER projection with hexagon cells and an aperture of 4
    'FULLER4T', # FULLER projection with triangle cells and an aperture of 4
    'FULLER4D', # FULLER projection with diamond cells and an aperture of 4
    'FULLER43H', # FULLER projection with hexagon cells and a mixed sequence of aperture 4 resolutions followed by aperture 3 resolutions
    'FULLER7H', # FULLER projection with hexagon cells and an aperture of 7
)

# control grid generation
clip_subset_types = ( 
    'SHAPEFILE',
    'WHOLE_EARTH',
    'GDAL',
    'AIGEN',
    'SEQNUMS'
)

# specify the output
cell_output_types = ( 
    'AIGEN',
    'GDAL',
    'GEOJSON',
    'SHAPEFILE',
    'NONE',
    'TEXT'
)

output_address_types = (
    'GEO', # geodetic coordinates -123.36 43.22 20300 Roseburg
    'Q2DI', # quad number and (i, j) coordinates on that quad
    'SEQNUM', # DGGS index - linear address (1 to size-of-DGG), not supported for parameter input_address_type if dggs_aperture_type is SEQUENCE
    'INTERLEAVE', # digit-interleaved form of Q2DI, only supported for parameter output_address_type; only available for hexagonal aperture 3 and 4 grids
    'PLANE', # (x, y) coordinates on unfolded ISEA plane,  only supported for parameter output_address_type;
    'Q2DD', # quad number and (x, y) coordinates on that quad
    'PROJTRI', # PROJTRI - triangle number and (x, y) coordinates within that triangle on the ISEA plane
    'VERTEX2DD', # vertex number, triangle number, and (x, y) coordinates on ISEA plane
    'AIGEN'  # Arc/Info Generate file format
)

input_address_types = (
    'GEO', # geodetic coordinates -123.36 43.22 20300 Roseburg
    'Q2DI', # quad number and (i, j) coordinates on that quad
    'SEQNUM', # DGGS index - linear address (1 to size-of-DGG), not supported for parameter input_address_type if dggs_aperture_type is SEQUENCE
    'Q2DD', # quad number and (x, y) coordinates on that quad
    'PROJTRI', # PROJTRI - triangle number and (x, y) coordinates within that triangle on the ISEA plane
    'VERTEX2DD', # vertex number, triangle number, and (x, y) coordinates on ISEA plane
    'AIGEN'  # Arc/Info Generate file format
)

### CUSTOM args
dggs_projections = ( "ISEA", "FULLER")

dggs_topologies = ( 'HEXAGON', 'TRIANGLE', 'DIAMOND')
dggs_aperture_types = ( 'PURE', 'MIXED43', 'SEQUENCE')

dggs_res_specify_types = ( "SPECIFIED", "CELL_AREA", "INTERCELL_DISTANCE" )
dggs_orient_specify_types = ( 'SPECIFIED', 'RANDOM', 'REGION_CENTER' )

# specify the operation
dggrid_operations = ( 
    'GENERATE_GRID',
    'TRANSFORM_POINTS',
    'BIN_POINT_VALS',
    'BIN_POINT_PRESENCE',
    'OUTPUT_STATS'
)


"""
helper function to create a DGGS config quickly
"""
def dgselect(dggs_type, **kwargs):

    dggs = None

    topo_dict = {
        'H' : 'HEXAGON',
        'T' : 'TRIANGLE',
        'D' : 'DIAMOND'
    }

    if dggs_type in dggs_types:
        if dggs_type in ['SUPERFUND', 'PLANETRISK']:
            # keep it simple, only that spec
            dggs = Dggs(dggs_type=dggs_type,
                        metric = True,
                        show_info = True)
            
            for res_opt in [ 'res', # dggs_res_spec
                             'precision', # default 7
                             'area', # dggs_res_specify_area
                             'spacing' , 
                             'cls_val' # dggs_res_specify_intercell_distance
                        ]:
                if res_opt in kwargs.keys():
                    dggs.set_par(res_opt, kwargs[res_opt])
        
        elif not dggs_type == 'CUSTOM':

            # if dggs_type == 'ISEA3H'
            #     projection, aperture, topology = 'ISEA', 3, 'HEXAGON'
            
            projection, aperture, topology = 'ISEA', 3, 'HEXAGON'

            if dggs_type.find('ISEA') > -1:
                projection == 'ISEA'
                sub1 = dggs_type.replace('ISEA','')
                topology = topo_dict[sub1[-1]]
                aperture = int(sub1.replace(sub1[-1], ''))
            
            elif dggs_type.find('FULLER') > -1:
                projection == 'FULLER'
                sub1 = dggs_type.replace('FULLER','')
                topology = topo_dict[sub1[-1]]
                aperture = int(sub1.replace(sub1[-1], ''))

            else:
                raise ValueError('projection not ISEA nor FULLER???')

            dggs = Dggs(dggs_type=dggs_type,
                        projection=projection,  # dggs_projection
                        aperture=aperture,  # dggs_aperture_type / dggs_aperture
                        topology=topology, # dggs_topology
                        metric = True,
                        show_info = True)
            
            for res_opt in [ 'res', # dggs_res_spec
                             'precision', # default 7
                             'area', # dggs_res_specify_area
                             'spacing' , 
                             'cls_val' # dggs_res_specify_intercell_distance
                        ]:
                if res_opt in kwargs.keys():
                    dggs.set_par(res_opt, kwargs[res_opt])
            
            if aperture == 43:
                if 'mixed_aperture_level' in kwargs.keys():
                    dggs.set_par('mixed_aperture_level', kwargs['mixed_aperture_level'])
                
        
        elif dggs_type == 'CUSTOM':
            # load and insert grid definition from dggs obj
            
            # dggs_projections = ( "ISEA", "FULLER")
            # dggs_res_specify_types = ( "SPECIFIED", "CELL_AREA", "INTERCELL_DISTANCE" )

            # specify_resolution(proj_spec, dggs_res_spec_type)
            """
            proj_spec,
                        dggs_res_spec_type,
                        dggs_res_spec=9,
                        dggs_res_specify_area=120000,
                        dggs_res_specify_intercell_distance=4000,
                        dggs_res_specify_rnd_down=True
            """

            # dggs_topologies = ( 'HEXAGON', 'TRIANGLE', 'DIAMOND')
            # dggs_aperture_types = ( 'PURE', 'MIXED43', 'SEQUENCE')

            # specify_topo_aperture(topology_type, aperture_type, aperture_res)
            """
            specify_topo_aperture(topology_type, aperture_type, aperture_res, dggs_num_aperture_4_res=0, dggs_aperture_sequence="333333333333")
            """

            # dggs_orient_specify_types = ( 'SPECIFIED', 'RANDOM', 'REGION_CENTER' )

            if 'orient_type' in kwargs.keys() and kwargs['orient_type'] in dggs_orient_specify_types:

                orient_type = kwargs['orient_type']
                # specify_orient_type_args(orient_type)
                """
                                            dggs_vert0_lon=11.25,
                                            dggs_vert0_lat=58.28252559,
                                            dggs_vert0_azimuth=0.0,
                                            dggs_orient_rand_seed=42
                """
            
            raise ValueError('custom not yet implemented')
    
    # dggs.dgverify()
    
    return dggs


"""
helper function to generate the metafile from a DGGS config
"""
def dg_grid_meta(dggs):

    dggrid_par_lookup = {
        'res' : 'dggs_res_spec',
        'precision': 'precision',
        'area' : 'dggs_res_specify_area',
        'cls_val' : 'dggs_res_specify_intercell_distance',
        'mixed_aperture_level' : 'dggs_num_aperture_4_res'
    }
    metafile = []
    
    if dggs.dggs_type in ['SUPERFUND', 'PLANETRISK']:
        metafile.append(f"dggs_type {dggs.dggs_type}")

    elif not dggs.dggs_type == 'CUSTOM':
        metafile.append(f"dggs_type {dggs.dggs_type}")

    elif dggs_type == 'CUSTOM':
        raise ValueError('custom not yet implemented')

    for res_opt in [ 'res', # dggs_res_spec
                    'precision', # default 7
                    'area', # dggs_res_specify_area
                    'cls_val', # dggs_res_specify_intercell_distance
                    'mixed_aperture_level'  # dggs_num_aperture_4_res 5
                    ]:
        if not dggs.get_par(res_opt, None) is None:
            opt_val = dggs.get_par(res_opt, None)
            if not opt_val is None:
                metafile.append(f"{dggrid_par_lookup[res_opt]} {opt_val}")
            
    return metafile


"""
class representing a DGGS grid system configuration, projection aperture etc
"""
class Dggs(object):

    """
        dggs_type: str     # = 'CUSTOM'
        projection: str     # = 'ISEA'
        aperture: int      #  = 3
        topology: str      #  = 'HEXAGON'
        res: int           #  = None
        precision: int     #  = 7
        area: float         #   = None
        spacing: float       #  = None
        cls_val: float        #     = None
        resround: str      #  = 'nearest'
        metric: bool        #  = True
        show_info: bool     #  = True
        azimuth_deg: float   #  = 0
        pole_lat_deg: float  #  = 58.28252559
        pole_lon_deg: float  # = 11.25

        mixed_aperture_level:  # e.g. 5 -> dggs_num_aperture_4_res 5  for ISEA_43_H etc
        metafile = []
    """

    def __init__(self, dggs_type, **kwargs):
        self.dggs_type = dggs_type

        for key, value in kwargs.items():
            self.set_par(key, value)


    # def dgverify(self):
    #     #See page 21 of documentation for further bounds
    #     if not self.projection in ['ISEA','FULLER']:
    #         raise ValueError('Unrecognised dggs projection')
    # 
    #     if not self.topology in ['HEXAGON','DIAMOND','TRIANGLE']:
    #         raise ValueError('Unrecognised dggs topology')
    #     if not self.aperture in [ 3, 4 ]:
    #         raise ValueError('Unrecognised dggs aperture')
    #     if self.res < 0:
    #         raise ValueError('dggs resolution must be >=0')
    #     if self.res > 30:
    #         raise ValueError('dggs resolution must be <=30')
    #     if self.azimuth_deg < 0 or self.azimuth_deg > 360:
    #         raise ValueError('dggs azimuth_deg must be in the range [0,360]')
    #     if self.pole_lat_deg < -90  or self.pole_lat_deg > 90:
    #         raise ValueError('dggs pole_lat_deg must be in the range [-90,90]')
    #     if self.pole_lon_deg < -180 or self.pole_lon_deg > 180:
    #         raise ValueError('dggs pole_lon_deg must be in the range [-180,180]')

    
    def set_par(self, par_key, par_value):
        if par_key == 'dggs_type':
            self.dggs_type = par_value
        if par_key == 'projection':
            self.projection = par_value
        if par_key == 'aperture':
            self.aperture = par_value
        if par_key == 'topology':
            self.topology = par_value
        if par_key == 'res':
            self.res = par_value
        if par_key == 'precision':
            self.precision = par_value
        if par_key == 'area':
            self.area = par_value
        if par_key == 'spacing':
            self.spacing = par_value 
        if par_key == 'cls_val':
            self.cls_val = par_value
        if par_key == 'resround':
            self.resround = par_value
        if par_key == 'metric':
            self.metric = par_value
        if par_key == 'show_info':
            self.show_info = par_value 
        if par_key == 'azimuth_deg':
            self.azimuth_deg = par_value 
        if par_key == 'pole_lat_deg':
            self.pole_lat_deg = par_value
        if par_key == 'pole_lon_deg':
            self.pole_lon_deg = par_value
        if par_key == 'mixed_aperture_level':
            self.mixed_aperture_level = par_value
        
        return self
    

    def get_par(self, par_key, alternative=None):
        if par_key == 'dggs_type':
            try:
                return self.dggs_type
            except AttributeError:
                return alternative
        if par_key == 'projection':
            try:
                return self.projection
            except AttributeError:
                return alternative
        if par_key == 'aperture':
            try:
                return self.aperture
            except AttributeError:
                return alternative
        if par_key == 'topology':
            try:
                return self.topology
            except AttributeError:
                return alternative
        if par_key == 'res':
            try:
                return self.res
            except AttributeError:
                return alternative
        if par_key == 'precision':
            try:
                return self.precision
            except AttributeError:
                return alternative
        if par_key == 'area':
            try:
                return self.area
            except AttributeError:
                return alternative
        if par_key == 'spacing':
            try:
                return self.spacing
            except AttributeError:
                return alternative
        if par_key == 'cls_val':
            try:
                return self.cls_val
            except AttributeError:
                return alternative
        if par_key == 'resround':
            try:
                return self.resround
            except AttributeError:
                return alternative
        if par_key == 'metric':
            try:
                return self.metric
            except AttributeError:
                return alternative
        if par_key == 'show_info':
            try:
                return self.show_info
            except AttributeError:
                return alternative
        if par_key == 'azimuth_deg':
            try:
                return self.azimuth_deg
            except AttributeError:
                return alternative
        if par_key == 'pole_lat_deg':
            try:
                return self.pole_lat_deg
            except AttributeError:
                return alternative
        if par_key == 'pole_lon_deg':
            try:
                return self.pole_lon_deg
            except AttributeError:
                return alternative
        if par_key == 'mixed_aperture_level':
            try:
                return self.mixed_aperture_level
            except AttributeError:
                return alternative
        else:
            return alternative
    

    def dg_closest_res_to_area (self, area, resround,metric,show_info=True):
        raise ValueError('not yet implemented')
    
    def dg_closest_res_to_spacing(self, spacing,resround,metric,show_info=True):
        raise ValueError('not yet implemented')

    def dg_closest_res_to_cls (self, cls_val, resround,metric,show_info=True):
        raise ValueError('not yet implemented')


"""
necessary instance object that needs to be instantiated once to tell where to use and execute the dggrid cmd tool
"""
class DGGRIDv7(object):

    def __init__(self, executable = 'dggrid', working_dir = None, capture_logs=True, silent=False):
        self.executable = Path(executable).resolve()
        self.capture_logs=capture_logs
        self.silent=silent
        self.last_run_succesful = False
        self.last_run_logs = ''

        if working_dir is None:
            self.working_dir = tempfile.mkdtemp(prefix='dggrid_')
        else:
            self.working_dir = working_dir

    
    def is_runnable(self):
        is_runnable = 0

        takes = []
        take_1 = shutil.which(self.executable)
        if not take_1 is None:
            takes.append(take_1)

        take_2 = shutil.which(os.path.join(self.working_dir, self.executable))
        if not take_2 is None:
            takes.append(take_2)

        if len(takes) < 1:
            print(f"{self.executable} not in executable paths")
        else:
            for elem in takes:
                swx = Path(elem)
                if swx.exists() and swx.is_file():
                    if os.access(elem, os.X_OK):
                        # print(f"{elem} is executable")
                        self.executable = str(elem)
                        is_runnable = 1
        
        return is_runnable


    def run(self, dggs_meta_ops):

        curdir = os.getcwd()
        tmp_id = uuid.uuid4()

        # subprocess.call / Popen swat_exec, check if return val is 0 or not
        # yield logs?
        try:
            os.chdir(self.working_dir)

            with open('metafile_' + str(tmp_id), 'w', encoding='utf-8') as metafile:
                for line in dggs_meta_ops:
                    metafile.write(line + '\n')
            
            logs = []
            o = subprocess.Popen([os.path.join(self.working_dir, self.executable), 'metafile_' + str(tmp_id)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            while o.poll() is None:
                for b_line in o.stdout:
                    line = b_line.decode().strip()
                    # sys.stdout.write(line)
                    if not self.silent:
                        print(line)
                    if self.capture_logs:
                        logs.append(line.strip())
            
            if o.returncode == 0:
                self.last_run_succesful = True
                try:
                    os.remove( 'metafile_' + str(tmp_id) )
                except Exception:
                    pass
            else:
                self.last_run_succesful = False

            if self.capture_logs:
                self.last_run_logs = '\n'.join(logs)
            else:
                self.last_run_logs = ''

        except Exception as e:
            self.last_run_succesful = False
            print(repr(e))
            traceback.print_exc(file=sys.stdout)
            self.last_run_logs(repr(e))
        finally:
            os.chdir(curdir)

        return o.returncode
    

    """
    ##############################################################################################
    # lower level API
    ##############################################################################################
    """
    def dgapi_grid_gen(self, dggs, subset_conf, output_conf):
        """
        Grid Generation. Generate the cells of a DGG, either covering the complete surface of the earth or covering only a 
        specific set of regions on the earth’s surface.
        """
        dggrid_operation = 'GENERATE_GRID'
        metafile = []
        metafile.append("dggrid_operation " + dggrid_operation)

        dggs_config_meta = dg_grid_meta(dggs)

        for cmd in dggs_config_meta:
            metafile.append(cmd)

        # clip_subset_types
        if subset_conf['clip_subset_type'] == 'WHOLE_EARTH':
            metafile.append("clip_subset_type " + subset_conf['clip_subset_type'])
        elif subset_conf['clip_subset_type'] in [ 'SHAPEFILE' , 'AIGEN', 'GDAL'] and not subset_conf['clip_region_files'] is None:
            metafile.append("clip_subset_type " + subset_conf['clip_subset_type'])
            metafile.append("clip_region_files " + subset_conf['clip_region_files'])
        elif subset_conf['clip_subset_type'] in [ 'SEQNUMS'] and not subset_conf['clip_region_files'] is None:
            if not dggs.dggs_type in ['ISEA7H', 'FULLER7H', 'PLANETRISK']:
                metafile.append("clip_subset_type " + subset_conf['clip_subset_type'])
                metafile.append("clip_region_files " + subset_conf['clip_region_files'])
            else:
                # if dggs_aperture_type would be SEQUENCE
                # have to reset to WHOLE_EARTH and clip based on 
                # output_first_seqnum and output_last_seqnum 
                subset_conf['clip_subset_type'] = 'WHOLE_EARTH'
                metafile.append("clip_subset_type " + subset_conf['clip_subset_type'])
                # loading seqnums
                files = subset_conf['clip_region_files'].split(' ')
                seqnums = []
                for file in files:
                    seqs = pd.read_csv( file, header=None)[0].values
                    seqnums.append(seqs.min())
                    seqnums.append(seqs.max())

                first_seqnum = np.array(seqnums).min()
                last_seqnum = np.array(seqnums).max()
                subset_conf['output_first_seqnum'] = first_seqnum
                metafile.append("output_first_seqnum " + str(subset_conf['output_first_seqnum']))
                subset_conf['output_last_seqnum'] = last_seqnum
                metafile.append("output_last_seqnum " + str(subset_conf['output_last_seqnum']))
        else:
            raise ValueError('something is not correct in subset_conf')
        
        # join grid gen params add to metafile

        # cell_output_types
        if 'cell_output_type' in output_conf.keys():
            if output_conf['cell_output_type'] in [ 'SHAPEFILE' , 'AIGEN', 'GEOJSON', 'TEXT'] and not output_conf['cell_output_file_name'] is None:
                for elem in filter(lambda x: x.startswith('cell_output_') , output_conf.keys()):
                    metafile.append(f"{elem} " + output_conf[elem])
            elif output_conf['cell_output_type'] in [ 'GDAL'] and not output_conf['cell_output_gdal_format'] is None and not output_conf['cell_output_file_name'] is None:
                for elem in filter(lambda x: x.startswith('cell_output_') , output_conf.keys()):
                    metafile.append(f"{elem} " + output_conf[elem])
            elif output_conf['cell_output_type'] in [ 'NONE']:
                metafile.append("cell_output_type NONE")
            
            # check join cell grid params add to metafile

        # point_output_types
        if 'point_output_type' in output_conf.keys():
            if output_conf['point_output_type'] in [ 'SHAPEFILE' , 'AIGEN', 'GEOJSON', 'TEXT'] and not output_conf['point_output_file_name'] is None:
                for elem in filter(lambda x: x.startswith('point_output_') , output_conf.keys()):
                    metafile.append(f"{elem} " + output_conf[elem])
            elif output_conf['point_output_type'] in [ 'GDAL'] and not output_conf['point_output_gdal_format'] is None and not output_conf['point_output_file_name'] is None:
                for elem in filter(lambda x: x.startswith('point_output_') , output_conf.keys()):
                    metafile.append(f"{elem} " + output_conf[elem])
            elif output_conf['point_output_type'] in [ 'NONE']:
                metafile.append("point_output_type NONE")
            
            # check join point grid params add to metafile

        result = self.run(metafile)

        if not result == 0:
            if self.capture_logs == True:
                message = f"some error happened under the hood of dggrid (exit code {result}): " + self.capture_logs
                raise ValueError(message)
            else:
                message = f"some error happened under the hood of dggrid (exit code {result}), try capture_logs=True for dggrid instance"
                raise ValueError(message)

        return { 'metafile': metafile, 'output_conf': output_conf }


    def dgapi_grid_transform(self, dggs, subset_conf, output_conf):
        """
        Address Conversion. Transform a file of locations from one address form (such as longitude/latitude) to another (such as DGG cell indexes).
        """
        dggrid_operation = 'TRANSFORM_POINTS'
        metafile = []
        metafile.append("dggrid_operation " + dggrid_operation)

        dggs_config_meta = dg_grid_meta(dggs)

        for cmd in dggs_config_meta:
            metafile.append(cmd)
        
        # transform input_types
        if 'input_file_name' in subset_conf.keys() and 'input_address_type' in subset_conf.keys() and subset_conf['input_address_type'] in input_address_types:
            for elem in filter(lambda x: x.startswith('input_') , subset_conf.keys()):
                metafile.append(f"{elem} " + subset_conf[elem])
        else:
            raise ValueError('no input filename or type given')
        
        # join grid gen params add to metafile

        # transform output_types
        if 'output_file_name' in output_conf.keys() and 'output_address_type' in output_conf.keys() and output_conf['output_address_type'] in output_address_types:
            for elem in filter(lambda x: x.startswith('output_') , output_conf.keys()):
                metafile.append(f"{elem} " + output_conf[elem])
        else:
            raise ValueError('no output filename or type given')
        
        result = self.run(metafile)

        if not result == 0:
            if self.capture_logs == True:
                message = f"some error happened under the hood of dggrid (exit code {result}): " + self.capture_logs
                raise ValueError(message)
            else:
                message = f"some error happened under the hood of dggrid (exit code {result}), try capture_logs=True for dggrid instance"
                raise ValueError(message)

        return { 'metafile': metafile, 'output_conf': output_conf }


    def dgapi_point_value_binning(self, dggs):
        """
        Point Value Binning. Bin a set of floating-point values associated with point locations into the cells of a DGG, 
        by assigning to each DGG cell the arithmetic mean of the values which are contained in that cell.
        """
        dggrid_operation = 'BIN_POINT_VALS'
        metafile = []
        metafile.append("dggrid_operation " + dggrid_operation)

        raise ValueError("Not yet implemented")
        # return None


    def dgapi_pres_binning(self, dggs):
        """
        Presence/Absence Binning. Given a set of input files, each containing point locations associated with a particular class, DGGRID outputs, 
        for each cell of a DGG, a vector indicating whether or not each class is present in that cell.
        """
        dggrid_operation = 'BIN_POINT_PRESENCE'
        metafile = []
        metafile.append("dggrid_operation " + dggrid_operation)

        raise ValueError("Not yet implemented")
        # return None


    def dgapi_grid_stats(self, dggs):
        """
        Output Grid Statistics. Output a table of grid characteristics for the specified DGG.
        """
        import copy

        np_table_switch = True
        try:
            import numpy as np
        except ImportError:
            np_table_switch = False
            
        dggrid_operation = 'OUTPUT_STATS'
        metafile = []
        metafile.append("dggrid_operation " + dggrid_operation)

        dggs_config_meta = dg_grid_meta(dggs)

        for cmd in dggs_config_meta:
            metafile.append(cmd)
        
        # we need to capturethe logs for this one:
        save_state = copy.copy(self.capture_logs)
        self.capture_logs = True

        result = self.run(metafile)

        if not result == 0:
            if self.capture_logs == True:
                message = f"some error happened under the hood of dggrid (exit code {result}): " + self.last_run_logs
                raise ValueError(message)
            else:
                message = f"some error happened under the hood of dggrid (exit code {result}), try capture_logs=True for dggrid instance"
                raise ValueError(message)

        table = []
        earth_line_switch = False
        earth_radius_info = ''
        for line in self.last_run_logs.split('\n'):
            if "Earth Radius" in line:
                earth_line_switch = True
                earth_radius_info = line.strip().replace(',','')

            if earth_line_switch == True:
                table.append(line.strip().replace(',',''))
        
        # set capture logs back to original
        self.capture_logs == save_state

        if np_table_switch == True:
            np_table = np.genfromtxt(table, skip_header=3)

            return { 'metafile': metafile, 'output_conf': {'stats_output': np_table, 'earth_radius_info': earth_radius_info } }
        else:
            return { 'metafile': metafile, 'output_conf': {'stats_output': table, 'earth_radius_info': earth_radius_info } }


    """
    #################################################################################
    # Higher level API
    #################################################################################
    """
    def grid_stats_table(self, dggs_type, resolution, mixed_aperture_level=None):
        """
        generates the area and cell statististcs for the given DGGS from resolution 0 to the given resolution of the DGGS
        """
        dggs = dgselect(dggs_type = dggs_type, res= resolution, mixed_aperture_level=mixed_aperture_level)

        dggs_ops = self.dgapi_grid_stats(dggs)
        df = pd.DataFrame(dggs_ops['output_conf']['stats_output'])

        df.rename(columns={0: 'Resolution', 1: "Cells", 2:"Area (km^2)", 3: "CLS (km)"}, inplace=True)
        df['Resolution'] = df['Resolution'].astype(int)
        df['Cells'] = df['Cells'].astype(np.int64)
        return df


    def grid_cell_polygons_for_extent(self, dggs_type, resolution, mixed_aperture_level=None, clip_geom=None):
        """
        generates a DGGS grid and returns all the cells as Geodataframe with geometry type Polygon
            a) if clip_geom is empty/None: grid cell ids/seqnms for the WHOLE_EARTH
            b) if clip_geom is a shapely shape geometry, takes this as a clip area
        """
        tmp_id = uuid.uuid4()
        tmp_dir = self.working_dir
        dggs = dgselect(dggs_type = dggs_type, res= resolution, mixed_aperture_level=mixed_aperture_level)
        
        subset_conf = { 'update_frequency': 100000, 'clip_subset_type': 'WHOLE_EARTH' }

        if not clip_geom is None and clip_geom.area > 0:

            clip_gdf = gpd.GeoDataFrame(pd.DataFrame({'id' : [1], 'geometry': [clip_geom]}), geometry='geometry', crs=from_epsg(4326))
            clip_gdf.to_file(Path(tmp_dir) / f"temp_clip_{tmp_id}.geojson", driver='GeoJSON' )

            subset_conf.update({
                'clip_subset_type': 'GDAL',
                'clip_region_files': str( (Path(tmp_dir) / f"temp_clip_{tmp_id}.geojson").resolve()),
                })

        output_conf = {
            'cell_output_type': 'GDAL',
            'cell_output_gdal_format' : 'GeoJSON',
            'cell_output_file_name': str( (Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.geojson").resolve())
            }
        
        dggs_ops = self.dgapi_grid_gen(dggs, subset_conf, output_conf )

        gdf = gpd.read_file( Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.geojson", driver='GeoJSON' )

        try:
            os.remove( str( Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.geojson") )
            os.remove( str( Path(tmp_dir) / f"temp_clip_{tmp_id}.geojson") )
        except Exception:
            pass

        return gdf


    def grid_cell_polygons_from_cellids(self, cell_id_list, dggs_type, resolution, mixed_aperture_level=None):
        """
        generates a DGGS grid and returns all the cells as Geodataframe with geometry type Polygon
            a) if cell_id_list is empty/None: grid cells for the WHOLE_EARTH
            b) if cell_id_list is a list/numpy array, takes this list as seqnums ids for subsetting
        """
        tmp_id = uuid.uuid4()
        tmp_dir = self.working_dir
        dggs = dgselect(dggs_type = dggs_type, res= resolution, mixed_aperture_level=mixed_aperture_level)
        
        subset_conf = { 'update_frequency': 100000, 'clip_subset_type': 'WHOLE_EARTH' }
        seq_df = None

        if not cell_id_list is None and len(cell_id_list) > 0:

            seq_df = pd.DataFrame({ 'seqs': cell_id_list})
            seq_df.to_csv( str( (Path(tmp_dir) / f"temp_clip_{tmp_id}.txt").resolve()) , header=False, index=False, columns=['seqs'], sep=' ')

            subset_conf.update({
                'clip_subset_type': 'SEQNUMS',
                'clip_region_files': str( (Path(tmp_dir) / f"temp_clip_{tmp_id}.txt").resolve()),
                })

        output_conf = {
            'cell_output_type': 'GDAL',
            'cell_output_gdal_format' : 'GeoJSON',
            'cell_output_file_name': str( (Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.geojson").resolve())
            }
        
        dggs_ops = self.dgapi_grid_gen(dggs, subset_conf, output_conf )

        gdf = gpd.read_file( Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.geojson", driver='GeoJSON' )

        if not cell_id_list is None and len(cell_id_list) > 0 and not seq_df is None:
            # we have to adjust the columns formats for the IDs/Seqnums/Name field to ensure they are comparable for the join
            # as they are all cell IDs they should all be long integers
            seq_df['cell_exists'] = True
            seq_df['seqs'] = seq_df['seqs'].astype(np.int64)
            seq_df.set_index('seqs', inplace=True)
            gdf['Name'] = gdf['Name'].astype(np.int64)
            gdf = gdf.join( seq_df, how='inner', on='Name')
            gdf = gdf.loc[gdf['cell_exists']].drop(columns=['cell_exists'])

        try:
            os.remove( str( Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.geojson") )
            os.remove( str( Path(tmp_dir) / f"temp_clip_{tmp_id}.txt") )
        except Exception:
            pass

        return gdf


    def grid_cellids_for_extent(self, dggs_type, resolution, mixed_aperture_level=None, clip_geom=None):
        """
        generates a DGGS grid and returns all the cellids as a pandas dataframe
            a) if clip_geom is empty/None: grid cell ids/seqnms for the WHOLE_EARTH
            b) if clip_geom is a shapely shape geometry, takes this as a clip area
        """
        tmp_id = uuid.uuid4()
        tmp_dir = self.working_dir
        dggs = dgselect(dggs_type = dggs_type, res= resolution, mixed_aperture_level=mixed_aperture_level)
        
        subset_conf = { 'update_frequency': 100000, 'clip_subset_type': 'WHOLE_EARTH' }

        if not clip_geom is None and clip_geom.area > 0:

            clip_gdf = gpd.GeoDataFrame(pd.DataFrame({'id' : [1], 'geometry': [clip_geom]}), geometry='geometry', crs=from_epsg(4326))
            clip_gdf.to_file(Path(tmp_dir) / f"temp_clip_{tmp_id}.geojson", driver='GeoJSON' )

            subset_conf.update({
                'clip_subset_type': 'GDAL',
                'clip_region_files': str( (Path(tmp_dir) / f"temp_clip_{tmp_id}.geojson").resolve()),
                })

        output_conf = {
            'point_output_type': 'TEXT',
            'point_output_file_name': str( (Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}").resolve())
            }
        
        dggs_ops = self.dgapi_grid_gen(dggs, subset_conf, output_conf )

        df = pd.read_csv( Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.txt" , header=None)
        df = df.dropna()

        try:
            os.remove( str( Path(tmp_dir) / f"temp_{dggs_type}_{resolution}_out_{tmp_id}.txt") )
            os.remove( str( Path(tmp_dir) / f"temp_clip_{tmp_id}.geojson") )
        except Exception:
            pass

        return df


    def cells_for_geo_points(self, geodf_points_wgs84, cell_ids_only, dggs_type, resolution, mixed_aperture_level=None):
        """
        takes a geodataframe with point geometry and optional additional value columns and returns:
            a) if cell_ids_only == True: the same geodataframe with an additional column with the cell ids
            b) if cell_ids_only == False: a new Geodataframe with geometry type Polygon, with column of cell ids and the additional columns
        """
        tmp_id = uuid.uuid4()
        tmp_dir = self.working_dir
        dggs = dgselect(dggs_type = dggs_type, res= resolution, mixed_aperture_level=mixed_aperture_level)

        cols = set(geodf_points_wgs84.columns.tolist())
        cols = cols - set('geometry')
        geodf_points_wgs84['lon'] = geodf_points_wgs84['geometry'].x
        geodf_points_wgs84['lat'] = geodf_points_wgs84['geometry'].y
        cols_ordered = ['lon', 'lat']
        for col_name in cols:
            cols_ordered.append(col_name)

        geodf_points_wgs84[cols_ordered].to_csv( str( (Path(tmp_dir) / f"geo_{tmp_id}.txt").resolve()) , header=False, index=False, columns=cols_ordered, sep=' ')

        subset_conf = {
            'input_file_name':  str( (Path(tmp_dir) / f"geo_{tmp_id}.txt").resolve()),
            'input_address_type': 'GEO',
            'input_delimiter': "\" \""
            }

        output_conf = {
            'output_file_name': str( (Path(tmp_dir) / f"seqnums_{tmp_id}.txt").resolve()),
            'output_address_type': 'SEQNUM',
            'output_delimiter': "\",\""
            }
        
        dggs_ops = self.dgapi_grid_transform(dggs, subset_conf, output_conf)

        df = pd.read_csv( dggs_ops['output_conf']['output_file_name'] , header=None)
        df = df.dropna()
        cell_id_list = df[0].values

        try:
            os.remove( str( Path(tmp_dir) / f"geo_{tmp_id}.txt") )
            os.remove( str( Path(tmp_dir) / f"seqnums_{tmp_id}.txt") )
        except Exception:
            pass

        if cell_ids_only == True:
            geodf_points_wgs84['seqnums'] = cell_id_list
            return geodf_points_wgs84
        else:
            # grid_gen from seqnums
            gdf = self.grid_cell_polygons_from_cellids(cell_id_list=cell_id_list,
                                                    dggs_type=dggs_type,
                                                    resolution=resolution,
                                                    mixed_aperture_level=mixed_aperture_level)
            try:
                for col in cols_ordered:
                    gdf[col] = geodf_points_wgs84[col].values
            except Exception:
                pass
            return gdf


#############################################################
"""
below is work in progress on custom DGGS configuration, currently we only barely support the predefined DGGS_TYPES
"""

parameters = (
    'bin_coverage',
    'cell_output_control',
    'cell_output_file_name',
    'cell_output_gdal_format',
    'cell_output_type',
    'children_output_file_name',
    'children_output_type',
    'clipper_scale_factor',
    'clip_region_files',
    'clip_subset_type',
    'densification',
    'dggrid_operation',
    'dggs_aperture_sequence',
    'dggs_aperture_type',
    'dggs_num_aperture_4_res',
    'dggs_proj',
    'dggs_res_spec',
    'dggs_res_specify_area',
    'dggs_res_specify_rnd_down',
    'dggs_res_specify_type',
    'dggs_topology',
    'dggs_type',
    'geodetic_densify',
    'input_address_type',
    'input_delimiter',
    'input_file_name',
    'input_files',
    'kml_default_color',
    'kml_default_width',
    'kml_description',
    'kml_name',
    'max_cells_per_output_file',
    'neighbor_output_file_name',
    'neighbor_output_type',
    'output_address_type',
    'output_count',
    'output_delimiter',
    'output_file_name',
    'point_output_file_name',
    'point_output_gdal_format',
    'point_output_type',
    'precision',
    'shapefile_id_field_length',
    'update_frequency',
    'verbosity'
)

def specify_orient_type_args(orient_type,
                            dggs_vert0_lon=11.25,
                            dggs_vert0_lat=58.28252559,
                            dggs_vert0_azimuth=0.0,
                            dggs_orient_rand_seed=42):

    if orient_type == 'SPECIFIED':
        return {
            'dggs_vert0_lon' : dggs_vert0_lon,
            'dggs_vert0_lat' : dggs_vert0_lat,
            'dggs_vert0_azimuth' : dggs_vert0_azimuth
        }
    if orient_type == 'RANDOM':
        return { 'dggs_orient_rand_seed' : dggs_orient_rand_seed }

    # else default REGION_CENTER


def specify_topo_aperture(topology_type, aperture_type, aperture_res, dggs_num_aperture_4_res=0, dggs_aperture_sequence="333333333333"):
    if not topology_type in dggs_topologies or not aperture_type in dggs_aperture_types:
        raise ValueError('topology or aperture type unknow')

    if aperture_type == 'PURE':
        if topology_type == 'HEXAGON':
            if not aperture_res in [3, 4, 7]:
                print(f"combo not possible / {topology_type} {aperture_res} / setting 3H")
                return { '#short_name': "3H",
                    'dggs_topology': topology_type,
                    'dggs_aperture_type': aperture_type,
                    'dggs_aperture': 3
                    }
            else:
                return { '#short_name': f"{aperture_res}H",
                    'dggs_topology': topology_type,
                    'dggs_aperture_type': aperture_type,
                    'dggs_aperture': aperture_res
                    }
                
        if topology_type in ['TRIANGLE', 'DIAMOND']:
            if not aperture_res == 4:
                print(f"combo not possible / {topology_type} {aperture_res} / setting 4{topology_type[0]}")
                return { '#short_name': f"4{topology_type[0]}",
                    'dggs_topology': topology_type,
                    'dggs_aperture_type': aperture_type,
                    'dggs_aperture': 4
                    }
            else:
                return { '#short_name': f"4{topology_type[0]}",
                    'dggs_topology': topology_type,
                    'dggs_aperture_type': aperture_type,
                    'dggs_aperture': aperture_res
                    }

    elif aperture_type == 'MIXED43':
        # dggs_aperture is ignored, only HEXAGON can have MIXED34
        if topology_type == 'HEXAGON':
            # dggs_num_aperture_4_res (default 0)
            return { '#short_name': f"43H",
                    'dggs_topology': topology_type,
                    'dggs_aperture_type': aperture_type,
                    'dggs_num_aperture_4_res': dggs_num_aperture_4_res,
                    '#dggs_aperture': aperture_res
                    }
        else:
            raise ValueError('not yet implemented')

    elif aperture_type == "SEQUENCE":
        # dggs_aperture_sequence (default “333333333333”).
        return { '#short_name': f"SEQ{topology_type[0]}",
                'dggs_topology': topology_type,
                'dggs_aperture_type': aperture_type,
                'dggs_aperture_sequence': str(dggs_aperture_sequence),
                '#dggs_aperture': aperture_res
            }


def specify_resolution(proj_spec,
                        dggs_res_spec_type,
                        dggs_res_spec=9,
                        dggs_res_specify_area=120000,
                        dggs_res_specify_intercell_distance=4000,
                        dggs_res_specify_rnd_down=True):
    if not proj_spec in list(dggs_projections) or not dggs_res_spec_type in dggs_res_specify_types:
        raise ValueError("base projection (ISEA or FULLER) or resolution spec unknown")

    if dggs_res_spec_type == "SPECIFIED":
        return {
            'dggs_proj': proj_spec,
            'dggs_res_specify_type': dggs_res_spec
        }
    
    elif dggs_res_spec_type == 'CELL_AREA':
        return {
            'dggs_proj': proj_spec,
            'dggs_res_specify_area': dggs_res_specify_area, # (in square kilometers)
            'dggs_res_specify_rnd_down' : dggs_res_specify_rnd_down
        }
    elif dggs_res_spec_type == 'INTERCELL_DISTANCE':
        return {
            'dggs_proj': proj_spec,
            'dggs_res_specify_intercell_distance': dggs_res_specify_intercell_distance, # (in kilometers)
            'dggs_res_specify_rnd_down' : dggs_res_specify_rnd_down
        }


def dgconstruct(dggs_type: str   = "CUSTOM", # dggs_type
                projection: str   = 'ISEA',  # dggs_projection
                aperture: int     = 3,  # dggs_aperture_type / dggs_aperture
                topology: str     = 'HEXAGON', # dggs_topology
                res: int          = None, # dggs_res_spec
                precision: int    = 7,
                area: float         = None, # dggs_res_specify_area
                spacing: float      = None,
                cls_val: float          = None, # dggs_res_specify_intercell_distance
                resround: str     = 'nearest',
                metric: bool       = True,
                show_info: bool    = True,
                azimuth_deg: float  = 0, # dggs_vert0_azimuth
                pole_lat_deg: float = 58.28252559, # dggs_vert0_lat
                pole_lon_deg: float = 11.25 # dggs_vert0_lon
                ):
    
    if not len(list(filter(lambda x: not x is None, [res,area,spacing,cls_val])))  == 1:  
        raise ValueError('dgconstruct(): Only one of res, area, length, or cls can have a value!')

    #Use a dummy resolution, we'll fix it in a moment
    dggs = Dggs(
        dggs_type   = dggs_type,
        pole_lon_deg = pole_lon_deg,
        pole_lat_deg = pole_lat_deg,
        azimuth_deg  = azimuth_deg,
        aperture     = aperture,
        res          = 1,
        topology     = topology.upper(),
        projection   = projection.upper(),
        precision    = precision
    )

    if not res is None:
        dggs.res = res
    elif not area is None:
        dggs.res = dggs.dg_closest_res_to_area (area=area, round=resround,metric=metric,show_info=True)
    elif not spacing is None :
        dggs.res = dggs.dg_closest_res_to_spacing(spacing=spacing,round=resround,metric=metric,show_info=True)
    elif not cls_val is None:
        dggs.res = dggs.dg_closest_res_to_cls ( cls_val=cls_val, round=resround,metric=metric,show_info=True)
    else:
        raise ValueError('dgconstruct(): Logic itself has failed us.')

    dggs.dgverify()

    return dggs
