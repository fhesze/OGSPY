
import os
import sys

if (os.name == 'posix'):
    ogs_lib_path = os.environ['HOME'] + '/Source/lib/ogspy'
    geo_lib_path = os.environ['HOME'] + '/Source/lib/geostat'
    msh_lib_path = os.environ['HOME'] + '/Source/lib/meshpy'
elif (os.name == 'nt'):
    ogs_lib_path = 'C:/Users/group/Source/lib/ogspy'
    geo_lib_path = 'C:/Users/group/Source/lib/geostat'
sys.path.append(ogs_lib_path)
sys.path.append(geo_lib_path)
sys.path.append(msh_lib_path)

from ogspy import *
from geospy import *
from meshpy import *

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

#-------------------------config dictionaries---------------------------------#

OGS_Config              = {'task_root' : ogs_lib_path + '/tutorials/transport/project',
                           'task_id'   : 'fm',
                           'dim_no'    : dim_no}
              
BC_Config_Flow          = {'pcs_type' : pcs_type_flow,
                           'prim_variable' : var_name_flow,
                           'geo_type' : 'POLYLINE  r_bc',
                           'dis_type' : 'CONSTANT 0.0'}
              
IC_Config_Flow          = {'pcs_type' : pcs_type_flow,
                           'prim_variable' : var_name_flow,
                           'geo_type' : 'DOMAIN',
                           'dis_type' : 'CONSTANT 0.0'}
                  
IC_Config_Transport     = {'pcs_type' : pcs_type_transport,
                           'prim_variable' : var_name_transport,
                           'geo_type' : 'DOMAIN',
                           'dis_type' : 'CONSTANT 0.0'}
                       
IC_Config_Init          = {'pcs_type' : pcs_type_transport,
                           'prim_variable' : var_name_transport,
                           'geo_type' : 'SURFACE CSS',
                           'dis_type' : 'CONSTANT 5.0'}
              
MCP_Config              = {'name' : var_name_transport,
                           'mobile' : '1; MOBIL-Flag: 0=immobile, 1=mobile/transported'}
              
MMP_Config              = {'geo_dim' : int(dim_no),
                           'geo_area' : '1.0',
                           'storage' : '1.02e-7',
                           'per_sat' : '1.0',
                           'per_tensor' : 'ISOTROPIC  1',
                           'per_dist' : 'fm.mpd',
                           'porosity' : '0.2',
                           'tortuosity' : '1.0',
                           'mass_disp_x' : '5.0',
                           'mass_disp_y' : '0.5',
                           'density' : '2000.0'}
              
MFP_Config              = {'fluid_type' : 'LIQUID',
                           'density' : '999.7026',
                           'viscosity' : '1.308E-03'}           
              
MSP_Config              = {'density' : '2.00000e+003'}

NUM_Config_Flow         = {'pcs_type' : pcs_type_flow, 
                           'solver' : '$LINEAR_SOLVER ',
                           'solver_01' : '; method error_tolerance max_iterations theta precond storage',
                           'solver_02' : '  2      5 1.e-014       1000           1.0   100     4',
                           'prop_type' : '$RENUMBER', 
                           'prop' : '2 -1'}
                           
NUM_Config_Transport    = {'pcs_type' : pcs_type_transport,
                           'solver' : '$LINEAR_SOLVER ',
                           'solver_01' : '; method error_tolerance max_iterations theta precond storage',
                           'solver_02' : '  2      6 1.e-014       1000           0.5   1       2',
                           'prop_type' : '$ELE_GAUSS_POINTS',
                           'prop' : '3'}
              
OUT_Config_Transport    = {'nod_values' : var_name_transport,
                           'geo_type' : 'POINT',
                           'geo_name' : 'point2',
                           'dat_type' : 'TECPLOT',
                           'tim_type' : 'STEPS 1'}
                        
PCS_Config_Flow         = {'pcs_type' : pcs_type_flow,
                           'num_type' : 'NEW',
                           'prim_variable' : var_name_flow}
                   
PCS_Config_Transport    = {'pcs_type' : pcs_type_transport,
                           'prim_variable' : var_name_transport}
                        
ST_Config_Flow          = {'pcs_type' : pcs_type_flow,
                           'prim_variable' : var_name_flow,
                           'geo_type' : 'POINT WELL',
                           'dis_type' : 'CONSTANT_NEUMANN -5E-3'}  
                        
TIM_Config_Flow         = {'pcs_type' : pcs_type_flow,
                           'time_start' : str(time_start),
                           'time_end' : str(time_end),
                           'time_steps' : str(time_no),
                           'step_size' : str(step_size)}                          

TIM_Config_Transport    = {'pcs_type' : pcs_type_transport,
                           'time_start' : str(time_start),
                           'time_end' : str(time_end),
                           'time_steps' : str(time_no),
                           'step_size' : str(step_size)}                    

#-------------------------generate ogs base class-----------------------------#

ogs = OGS(**OGS_Config)

#-------------------------generate mesh---------------------------------------#

MeshConfig = {
    'mesh_type' : 'quad',
    'mesh_origin': [0, 0, 0],
    'mesh_size': [100, 50, 1],
    'cell_size': [1, 1, 1]
}

msh = MSH(**OGS_Config)
msh.gen_mesh(**MeshConfig)
#msh.import_mesh( ogs_lib_path, '/tutorials/transport/data/fm.msh')
msh.write_file()

#mesh = MESH(**MeshConfig)
#print(mesh.centroid_array[:,0])

#-------------------------generate ogs transmissivity field-------------------#

SRFConfig = {
    'dim_no': dim_no,
    'cov_model' : 'Gau',
    'mu' : -15,
    'sigma_2' : 1.0,
    'len_scale' : [10, 10]
}

srf = Transmissivity( **SRFConfig )
srf.set_mesh('unstructured', msh.centroid_array[:,0], msh.centroid_array[:,1])
srf.gen_srf()

mpd = MPD(**OGS_Config)
mpd.add_srf(srf)
mpd.write_file()

#-------------------------generate gli class----------------------------------#

gli = GLI(**OGS_Config)
gli.add_point(p_name = 'WELL', p_pos_array = np.array([10, 25, 0]))
gli.add_boundary(msh, 'AROUND')
gli.add_point(p_name = 'point1', p_pos_array = np.array([20, 25, 0]))
gli.add_point(p_name = 'point2', p_pos_array = np.array([60, 25, 0]))
gli.add_point(p_name = 'point3', p_pos_array = np.array([65, 25, 0]))
gli.add_line(l_name = 'r_bc', l_pos_array = np.array([[100,0,0], [100,50,0]]))
gli.add_line(l_name = 'CS', 
             l_pos_array = np.array([[70,24,0],[70.5,24,0],[70.5,26,0],[70,26,0]]), 
             l_type = 'closed')
gli.add_surface(s_name = 'CSS', s_polylines = 'CS', s_type = '0')
gli.write_file()

#-------------------------generate ogs input classes--------------------------#

bc = BC(**OGS_Config)
bc.add_block(**BC_Config_Flow)
bc.write_file()

ic = IC(**OGS_Config)
ic.add_block(**IC_Config_Flow)
ic.add_block(**IC_Config_Transport)
ic.add_block(**IC_Config_Init)            
ic.write_file()

mcp = MCP(**OGS_Config)
mcp.add_block(**MCP_Config)
mcp.write_file()

mfp = MFP(**OGS_Config)
mfp.add_block(**MFP_Config)
mfp.write_file()

mmp = MMP(**OGS_Config)
mmp.add_block(**MMP_Config)
mmp.write_file()

msp = MSP(**OGS_Config)
msp.add_block(**MSP_Config)
msp.write_file()

num = NUM(**OGS_Config)
num.add_block(**NUM_Config_Flow) 
num.add_block(**NUM_Config_Transport)
num.write_file()

out = OUT(**OGS_Config) 
out.add_block(**OUT_Config_Transport)
out.write_file()

pcs = PCS(**OGS_Config) 
pcs.add_block(**PCS_Config_Flow)
pcs.add_block(**PCS_Config_Transport)           
pcs.write_file()

st = ST(**OGS_Config)
st.add_block(**ST_Config_Flow)
st.write_file()
		
tim = TIM(**OGS_Config)
tim.add_block(**TIM_Config_Flow)
tim.add_block(**TIM_Config_Transport)              
tim.write_file()

#---------------run OGS simulation--------------------------------------------#

ogs.run_model(ogs_lib_path + '/bin/posix/ogs')

#--------------postprocessing OGS simulation results--------------------------#

#ogs.import_results(**OUT_Config_Transport)
#ogs.plot()

#ogs.plot_mesh(msh)
#ogs.plot_srf(msh, srf)


