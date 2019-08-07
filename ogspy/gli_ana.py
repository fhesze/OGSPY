
import os

from .mesh_ana import MESH_ANA

class GLI(MESH_ANA):

	"""
	Generate all input files according to specific radial mesh.
	"""
	
	def __init__(self, msh_root, msh_name, well_radius, bound_radius,absolute_depth,
				layer_number, task_root, task_ID):
		'''
		Input
		----------
		
		task_root(string):  	-path of dir of this task
		
		task_ID(string)				--name of task
		
		'''
		MESH_ANA.__init__(self, msh_root, msh_name, well_radius, bound_radius, absolute_depth,layer_number)
		self.task_root = task_root
		self.task_ID = task_ID
				
	def write_file(self):
	
		'''
		Generate a .gli file according to .msh file of radial mesh. Applicable to both 2D and 3D meshes.
		
		'''
		#from pre_processing import MESH_ANA
		seg_num,radial_node_dis, well_infs_ori, BC_infs_ori= MESH_ANA.__call__(self)
		point_index=0
		well_infs={}
		BC_infs={}
		for layer in range(self.layer_number+1):
			well_inf_layer=well_infs_ori[layer]
			BC_inf_layer=BC_infs_ori[layer]
			well_infs[layer]=[]
			BC_infs[layer]=[]
			for well_inf_ori in well_inf_layer:
				well_inf=[point_index,well_inf_ori[1],well_inf_ori[2],well_inf_ori[3]]
				point_index+=1
				well_infs[layer].append(well_inf)
			for BC_inf_ori in BC_inf_layer:
				BC_inf=[point_index,BC_inf_ori[1],BC_inf_ori[2],BC_inf_ori[3]]
				point_index+=1
				BC_infs[layer].append(BC_inf)
		
		file_gli=os.path.join(self.task_root, self.task_ID+'.gli')
		with open(file_gli,'w') as outfile:
			outfile.write('#POINTS\n')
			for layer in range(self.layer_number+1):
				well_inf_layer=well_infs[layer]
				BC_inf_layer=BC_infs[layer]
				for well_inf in well_inf_layer:
					outfile.write(str(well_inf[0])+'  '+str(well_inf[1])+'  '+str(well_inf[2])+'  '+str(well_inf[3])+'\n') 
				for BC_inf in BC_inf_layer:
					outfile.write(str(BC_inf[0])+'  '+str(BC_inf[1])+'  '+str(BC_inf[2])+'  '+str(BC_inf[3])+'\n')
			for layer in range(self.layer_number+1):
				well_inf_layer=well_infs[layer]
				BC_inf_layer=BC_infs[layer]
				outfile.write('#POLYLINE\n$NAME\nWELL_%d\n$EPSILON\n0.0001\n$POINTS\n'%layer)
				for well_inf in well_inf_layer:
					outfile.write(str(well_inf[0])+'\n')
				outfile.write(str(well_inf_layer[0][0])+'\n') #write the index of first point to make polyline closed
				outfile.write('#POLYLINE\n$NAME\nBC_%d\n$EPSILON\n0.0001\n$POINTS\n'%layer)
				for BC_inf in BC_inf_layer:
					outfile.write(str(BC_inf[0])+'\n')
				outfile.write(str(BC_inf_layer[0][0])+'\n') #write the index of first point to make polyline closed
			outfile.write('#STOP')
		print('GLI-file generated according to given MSH-file: ' + file_gli)  