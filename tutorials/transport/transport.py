
import os
import sys

if (os.name == 'posix'):
    ogs_lib_path = os.environ['HOME'] + '/Dropbox/fhesse/Source/lib/ogspy/'
    geo_lib_path = os.environ['HOME'] + '/Dropbox/fhesse/Source/lib/geostat/'
    msh_lib_path = os.environ['HOME'] + '/Dropbox/fhesse/Source/lib/meshpy/'
elif (os.name == 'nt'):
    ogs_lib_path = 'C:/Users/group/Source/lib/ogspy/'
    geo_lib_path = 'C:/Users/group/Source/lib/geostat/'
sys.path.append(ogs_lib_path)
sys.path.append(geo_lib_path)
sys.path.append(msh_lib_path)

from ogspy import *
from meshpy import MESH
from geospy import Transmissivity

#-------------------------ogs configuration-----------------------------------#

dim_no = 2

time_start = 0
time_no = 960
step_size = 90
time_end = time_no*step_size

pcs_type_flow = 'LIQUID_FLOW'
var_name_flow = 'PRESSURE1'

pcs_type_transport = 'MASS_TRANSPORT'
var_name_transport = 'TRACER'            

#-------------------------generate ogs base class-----------------------------#
                           
ogs = OGS(task_root = ogs_lib_path + 'tutorials/transport/project/',
          task_id = 'fm', dim_no = dim_no)

#-----------------generate and add og smesh-----------------------------------#

mesh = MESH(mesh_type = 'quad', mesh_origin = [0, 0, 0], 
            element_no = [100, 50, 1], element_size = [1, 1, 1]  )
ogs.msh.set_mesh(mesh)
#ogs.msh.gen_mesh( )
#msh.import_mesh( ogs_lib_path, '/tutorials/transport/data/fm.msh')

#-----------------generate and add ogs transmissivity field-------------------#

SRFConfig = {
    'dim_no': dim_no,
    'model' : 'Gau',
    'sigma_2' : 1.0,
    'scale' : 10
}

srf = Transmissivity( mu = -10, **SRFConfig )
srf.set_mesh('unstructured', ogs.msh.centroid_array[:,0], 
             ogs.msh.centroid_array[:,1])
srf.run( 5000 )

ogs.mpd.add_mpd(srf.data)


#-------------------------generate gli class----------------------------------#

ogs.gli.add_point(p_name = 'WELL', p_pos_array = np.array([10, 25, 0]))
ogs.gli.add_boundary(ogs.msh, 'AROUND')
ogs.gli.add_point(p_name = 'point1', p_pos_array = np.array([20, 25, 0]))
ogs.gli.add_point(p_name = 'point2', p_pos_array = np.array([60, 25, 0]))
ogs.gli.add_point(p_name = 'point3', p_pos_array = np.array([65, 25, 0]))
ogs.gli.add_line(l_name = 'r_bc', l_pos_array = np.array([[100,0,0], [100,50,0]]))
ogs.gli.add_line(l_name = 'CS', 
             l_pos_array = np.array([[70,24,0],[70.5,24,0],[70.5,26,0],[70,26,0]]), 
             l_type = 'closed')
ogs.gli.add_surface(s_name = 'CSS', s_polylines = 'CS', s_type = '0')

#-------------------------generate ogs input classes--------------------------#

ogs.bc.add_block(pcs_type = pcs_type_flow,  prim_variable = var_name_flow,
                 geo_type = 'POLYLINE  r_bc', dis_type = 'CONSTANT 0.0')

ogs.ic.add_block(pcs_type = pcs_type_flow, prim_variable = var_name_flow,
                 geo_type = 'DOMAIN', dis_type = 'CONSTANT 0.0')
ogs.ic.add_block(pcs_type = pcs_type_transport,
                 prim_variable = var_name_transport, geo_type = 'DOMAIN',
                 dis_type = 'CONSTANT 0.0')
ogs.ic.add_block(pcs_type = pcs_type_transport, 
                 prim_variable = var_name_transport, geo_type = 'SURFACE CSS',
                 dis_type = 'CONSTANT 5.0')  

ogs.mcp.add_block(name = var_name_transport,
                  mobile = '1; MOBIL-Flag: 0=immobile, 1=mobile/transported')

ogs.mfp.add_block(fluid_type = 'LIQUID', density = '999.7026',
                  viscosity = '1.308E-03')

ogs.mmp.add_block(geo_dim = int(dim_no), geo_area = '1.0', storage = '1.02e-7',
                  per_sat = '1.0', per_tensor = 'ISOTROPIC  1',
                  per_dist = 'fm.mpd', porosity = '0.2', tortuosity = '1.0',
                  mass_disp_x = '5.0', mass_disp_y = '0.5', density = '2000.0')

ogs.msp.add_block(density = '2.00000e+003')

ogs.num.add_block(pcs_type = pcs_type_flow, solver = '$LINEAR_SOLVER ',
                  solver_01 = '; method error_tolerance max_iterations theta precond storage',
                  solver_02 = '  2      5 1.e-014       1000           1.0   100     4',
                  prop_type = '$RENUMBER', prop = '2 -1') 
ogs.num.add_block(pcs_type = pcs_type_transport, solver = '$LINEAR_SOLVER ',
                  solver_01 = '; method error_tolerance max_iterations theta precond storage',
                  solver_02 = '  2      6 1.e-014       1000           0.5   1       2',
                  prop_type = '$ELE_GAUSS_POINTS', prop = '3')

ogs.out.add_block(nod_values = var_name_transport, geo_type = 'POINT',
                  geo_name = 'point2', dat_type = 'TECPLOT',
                  tim_type = 'STEPS 1')

ogs.pcs.add_block(pcs_type = pcs_type_flow, num_type = 'NEW',
                  prim_variable = var_name_flow)
ogs.pcs.add_block(pcs_type = pcs_type_transport, 
                  prim_variable = var_name_transport) 

ogs.st.add_block(pcs_type = pcs_type_flow, prim_variable = var_name_flow,
                 geo_type = 'POINT WELL', dis_type = 'CONSTANT_NEUMANN -5E-3')
		
ogs.tim.add_block(pcs_type = pcs_type_flow, time_start = str(time_start),
                  time_end = str(time_end), time_steps = str(time_no),
                  step_size = str(step_size))
ogs.tim.add_block(pcs_type = pcs_type_transport, time_start = str(time_start),
                  time_end = str(time_end), time_steps = str(time_no),
                  step_size = str(step_size))

#---------------run OGS simulation--------------------------------------------#
              
ogs.write_input()
#ogs.run_model(ogs_lib_path + '/bin/posix/ogs')

#--------------postprocessing OGS simulation results--------------------------#

#ogs.import_results(**OUT_Config_Transport)
ogs.plot()

#ogs.plot_mesh(msh)
#ogs.plot_srf(msh, srf)


