# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 11:35:01 2015

@author: miao
"""

import os
import sys

if (os.name == 'posix'):
    lib_path = os.environ['HOME'] + '/Source/lib/Pumping_Test'
    sys.path.append( lib_path )
elif (os.name == 'nt'):
    #sys.path.append('C:\Users\miao\Documents\Python_Scripts\Pumping_Test')
	sys.path.append('C:\Users\miao\Documents\SVN-miao\ogspy')
#sys.path.append('\pre_post_processing')

from ogspy import *

#import preprocessing as prepro
#import tim
#import ogs_run

#-------------------------determin the parameters-----------------------------#
'''
Input
----------
msh_root(string):  		-- directory path of msh file
msh_name(string)		-- full name of mesh file (with extension)
task_root(string):  	-- directory path of this task
task_ID(string)				-- name of task
well_radius(float)			-- radius of well
bound_radius(float)			-- radius of boundary
absolute_depth(float)		-- absolute depth of model(positive)
layer_number(int)			-- the number of layers(in case of 2D equals to 0)
absolute_depth(float)		-- absolute depth of model(positive)
layer_number(int)			-- the number of layers(in case of 2D equals to 0)
permeability(float)			-- the mean of permeability
Kfield_type(int)			-- 1 corresponds to homogeneous Kfield and 2 heterogeneous Kfield
sigma_2(float)				-- variance
len_scale(float)			-- correlation length

Optional input
----------
ogs_root(string)			-- root of ogs executable file, default value is None.
Kfield_root(string)			-- root of permeability distribution file 
Kfeild_name(string)			-- name of Kfield file
'''

msh_root = lib_path + "/tutorials/pumping_test/data"
msh_name = "radial_mesh.msh"
Kfield_root = lib_path + "/tutorials/pumping_test/data"
Kfield_name = "conductivity_ogs.txt"
task_root = lib_path + "/tutorials/pumping_test/project"
task_ID = "fm"
well_radius = 0.01
bound_radius = 128
absolute_depth = 5
layer_number = 5
absolute_pumping_rate = 1.e-4
permeability = 1.e-4

Kfield_type = 2  #1 corresponds to homogeneous Kfield and 2 heterogeneous Kfield
sigma_2 = 1.
len_scale = [64, 64, 64]


#-------------------------generate input files--------------------------------#
#Test1.msh_copy()
msh_cfg = MSH(task_root, task_ID, msh_root, msh_name)
msh_cfg.copy_file()
#Test1.gli_generator()
gli_cfg = GLI(msh_root, msh_name, well_radius, bound_radius,absolute_depth,
				layer_number, task_root, task_ID)
gli_cfg.write_file()
#Test1.bc_generator()
bc_cfg = BC(task_root, task_ID, layer_number)
bc_cfg.write_file()
#Test1.radial_st_generator()
st_cfg = ST(msh_root, msh_name, well_radius, bound_radius,absolute_depth,
            layer_number, task_root, task_ID, absolute_pumping_rate, permeability)
st_cfg.write_file()
#Test1.mmp_generator(Kfield_type)
mmp_cfg = MMP(task_root, task_ID, layer_number, Kfield_type, permeability, Kfield_name)
mmp_cfg.write_file()
#Test1.ic_generator()
ic_cfg = IC(task_root, task_ID)
ic_cfg.write_file()
#Test1.mfp_generator()
mfp_cfg = MFP(task_root, task_ID)
mfp_cfg.write_file()
#Test1.num_generator()
num_cfg = NUM(task_root, task_ID)
num_cfg.write_file()
#Test1.out_generator()
out_cfg = OUT(task_root, task_ID)
out_cfg.write_file()
#Test1.pcs_generator()
pcs_cfg = PCS(task_root, task_ID)
pcs_cfg.write_file()
#Test1.tim_generator()
tim_cfg = TIM(task_root, task_ID)
tim_cfg.write_file()

#copy permeability file in heterogeneous case
if Kfield_type == 2:
	Kfield_cfg = PER(task_root,task_ID, Kfield_root, Kfield_name)
	Kfield_cfg.copy_file()
		
#--------------------------------------------run OGS simulation--------------------------------------------#
run (task_root, task_ID)