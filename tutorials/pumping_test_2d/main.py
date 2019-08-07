
import os
import sys
import numpy as np

if (os.name == 'posix'):
    ogs_lib_path = os.environ['HOME'] + '/Source/lib/ogspy/'
    geo_lib_path = os.environ['HOME'] + '/Source/lib/geostat/'
    msh_lib_path = os.environ['HOME'] + '/Source/lib/meshpy/'
    sys.path.append( ogs_lib_path )
    sys.path.append( geo_lib_path )
    sys.path.append( msh_lib_path )
elif (os.name == 'nt'):
    ogs_lib_path = 'C:/Users/group/Source/lib/ogspy/'
    sys.path.append(ogs_lib_path)

from ogspy import OGS
from meshpy import MESH
from geospy import Transmissivity

#-------------------------ogs configuration-----------------------------------#

dim_no = 2

time_start = 0
time_steps = 1
step_size = 1000 
time_end = time_steps*step_size

pcs_type_flow = 'GROUNDWATER_FLOW'
var_name_flow = 'HEAD'

pcs_type_transport = 'MASS_TRANSPORT'
var_name_transport = 'TRACER'      

#-------------------------generate ogs base class-----------------------------#

ogs = OGS(task_root = ogs_lib_path + 'tutorials/pumping_test_2d/project/',
          task_id = 'fm')

#-------------------------analyze mesh----------------------------------------#

MeshConfig = {'mesh_type' : 'quad',
              'mesh_origin': [-128, -128, 0],
              'element_no': [256, 256, 1],
              'element_size': [1, 1, 1]}

mesh = MESH( **MeshConfig )
ogs.msh.set_mesh( mesh )
##msh.import_mesh( ogs_lib_path, '/tutorials/pumping_test_2d/data/fm.msh')
#msh.get_centroid_of_elements()

#-------------------------generate ogs transmissivity field-------------------#

SRFConfig = {'dim_no': dim_no,
             'model' : 'Exp',
             'sigma_2' : 1.0,
             'scale' : 10}

srf = Transmissivity( mu = -10, **SRFConfig )
srf.set_mesh('unstructured', ogs.msh.centroid_array[:,0], 
             ogs.msh.centroid_array[:,1])
srf.run( 5000 )

ogs.mpd.add_mpd(srf.data)

#-------------------------generate gli class----------------------------------#

ogs.gli.add_boundary(ogs.msh, 'BC')
ogs.gli.add_point(p_name = 'WELL',
                  p_pos_array = np.array([0, 0, 0]) )

#---------------generate different ogs input classes--------------------------#

ogs.bc.add_block(pcs_type = pcs_type_flow, prim_variable = var_name_flow,
                 geo_type = 'POLYLINE  BC', dis_type = 'CONSTANT 0.0')

ogs.ic.add_block(pcs_type = pcs_type_flow, prim_variable = var_name_flow,
                 geo_type = 'DOMAIN', dis_type = 'CONSTANT 0.0')

ogs.mfp.add_block(fluid_type = 'LIQUID', density = '999.7026',
                  viscosity = '1.308E-03')

ogs.mmp.add_block(geo_dim = int(dim_no), storage = '0.0',
                  per_tensor = 'ISOTROPIC 1.0e-004', per_dist = 'fm.mpd',
                  porosity = '0.2')

ogs.num.add_block(pcs_type = pcs_type_flow, solver = '$LINEAR_SOLVER ',
                  solver_01 = '; method error_tolerance max_iterations theta precond storage',
                  solver_02 = '  2      5 1.0e-06       1000           1.0   1       4',
                  prop_type = '$ELE_GAUSS_POINTS', prop = '3')

ogs.out.add_block(nod_values = var_name_flow, geo_type = 'DOMAIN',
                  dat_type = 'TECPLOT', tim_type = 'STEPS 1')

ogs.pcs.add_block(pcs_type = pcs_type_flow, num_type = 'NEW')

ogs.st.add_block(pcs_type = pcs_type_flow, prim_variable = var_name_flow,
                 geo_type = 'POINT WELL', dis_type = 'CONSTANT -1.0e-005')

ogs.tim.add_block(pcs_type = pcs_type_flow, time_start = str(time_start),
                  time_end = str(time_end), time_steps = str(time_steps),
                  step_size = str(step_size))

#---------------run OGS simulation--------------------------------------------#

#ogs.write_input( )
#ogs.run_model(ogs_lib_path + '/bin/posix/ogs')

#--------------postprocessing OGS simulation results--------------------------#

#ogs.import_results(nod_values = var_name_flow, geo_type = 'DOMAIN',
#                   dat_type = 'TECPLOT', tim_type = 'STEPS 1' )
#ogs.plot_mesh( )

mesh.plot( np.log(srf.data) )
#mesh.plot( srf.data )
#ogs.plot_mesh(msh)
#ogs.plot_srf(msh, srf)

