# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 14:25:28 2015

@author: miao
"""
import math as m

class Mean_generator:
	'''
	Extract data from vtk file and then save data with cylindrical coordinates.
	'''
	def __init__(self, Ens, Geo_type, Mesh_type, assemble_num, seg_num, layer_num=0):
		'''
		Ens(integer)					--Ensemble type
	
		Geo_typ(integer)				--Geometry type
	
		Mes_typ(integer_				--Mesh type
	
		seg_num(int)					 --the number of segments
	 			
		Optional input
		----------
		layer_num(int)					--number of layers
		
		'''
		self.Ens, self.Geo_type, self.Mesh_type, self.assemble_num, self.seg_num, self.layer_num =\
		Ens, Geo_type, Mesh_type, assemble_num, seg_num, layer_num
		#self.sim_num_start, self.total_sim_num = sim_num_start, total_sim_num
		if layer_num:
			self.file_path='/gpfs1/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d_L%d/S%d/Theis3D_Ens%d_G%d_M%d_L%d'\
                       %(Ens, Geo_type, Mesh_type, layer_num, assemble_num,\
							Ens, Geo_type, Mesh_type, layer_num)
		else:
			self.file_path='/gpfs1/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d/S%d/Theis2D_Ens%d_G%d_M%d'\
                       %(Ens, Geo_type, Mesh_type, assemble_num, Ens, Geo_type, Mesh_type)							
	def convert_to_dat(self):
		'''
		Extract data from vtk file and then save data with cylindrical coordinates.
		'''
		
							
		file_vtk=self.file_path+'0001.vtk' #path of vtk file of steady flow
		file_dat=self.file_path+'0001.dat'
		
		coo_cyl_lists=[]
		inf_rad_segs=[] #nest list with first index of segment and second index of index of node
		dd_values=[]	#list to store all points' drawdown 
		
		#-----------------------extract coordinate of every nodes------------------------------#
		with open(file_vtk,'r') as infile:
			for i, line in enumerate(infile):		 
				#if (i>4)and(i<=nod_num+4):
				if 'POINTS' in line:
								  
					for line in infile:
						try:  
							coos=line.split()
							coo_x=float(coos[0])
							coo_y=float(coos[1])
							coo_z=float(coos[2])
							rad=m.sqrt(coo_x*coo_x+coo_y*coo_y)
							phi=m.atan2(coo_y,coo_x)
							coo_cyl=[rad,phi,coo_z]
							coo_cyl_lists.append(coo_cyl)
						except:
							break
				elif 'POINT_DATA' in line:
					next(infile)
					next(infile)
					for i, line in enumerate(infile):
						dd_value=float(line)
						dd_values.append(dd_value)
				
		for coo_cyl in coo_cyl_lists:
			index=coo_cyl_lists.index(coo_cyl)
			corresponding_dd=dd_values[index]
			coo_cyl.append(corresponding_dd)
		with open(file_dat,'w') as outfile:
			for words in coo_cyl_lists:
				outfile.write(str(words[0])+'   '+str(words[1])+'   '+str(words[2])+'   '+str(words[3])+'\n')
				
		print('output data saved to:'+file_dat)
		return coo_cyl_lists
	
	def spatial_mean(self):
		'''
		Calculate spatial mean of drawdowns. Suitable for 2D or 3D Radial meshes.
		'''
		'''
		if self.layer_num:
			file_path='/gpfs1/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d_L%d/S%d/\
							Theis3D_Ens%d_G%d_M%d_L%d'%(self.Ens, self.Geo_type, self.Mesh_type, self.layer_num, self.assemble_num,\
							self.Ens, self.Geo_type, self.Mesh_type, self.layer_num)
		else:
			file_path='/gpfs1/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d/S%d/\
							Theis2D_Ens%d_G%d_M%d'%(self.Ens, self.Geo_type, self.Mesh_type, self.assemble_num, self.Ens, self.Geo_type, self.Mesh_type)
		'''
		file_dat=self.file_path+'0001.dat'
		file_mean=self.file_path+'_spa_mean.dat'
		
		infile=open(file_dat,'r')
		lines=infile.readlines()
		infile.close()
		
		rad_distribution=[]
		dd_layer={} # drawdown with the key of segment number\
		phi_per_seg=2*m.pi/self.seg_num
		node_num_per_layer=len(lines)/(self.layer_num+1)
		node_num_per_phi=node_num_per_layer/self.seg_num
		
		mean_in_phi_layers=[] #mean in layers
		
		dd_dictionary={}
		#dd_array=np.zeros((int(node_num_per_phi),seg_num,layer_num))
		
		#----------------------------------find radial nodes distribution---------------------------------------#
		inf_layer_0=lines[0:node_num_per_layer]
		for line in inf_layer_0:
			inf_node=line.split()
			rad_node=float(inf_node[0])
			phi_node=float(inf_node[1])
			if abs(phi_node)<1e-6 and rad_node:
				rad_distribution.append(rad_node)
			
		
		#----------------------------------extract nodes' drawdowns---------------------------------------------#
		if self.layer_num:
			for layer_index in xrange(self.layer_num):
				inf_layers=lines[node_num_per_layer*(layer_index):\
                            node_num_per_layer*(layer_index+1)] #extract information of those nodes in specific layer
				for seg_index in xrange(self.seg_num):
					dd_layer[seg_index]=[]
				for line in inf_layers:
					inf_node=line.split()
					phi_node=float(inf_node[1])
					dd_node=float(inf_node[3])
					for seg_index in xrange(self.seg_num):
						phi_seg=phi_per_seg*seg_index if (phi_per_seg*seg_index)<m.pi else (phi_per_seg*seg_index-2*m.pi)
						if abs(phi_node-phi_seg)<1.e-6:
							dd_layer[seg_index].append(dd_node)
				dd_dictionary[layer_index]=dd_layer
		else:
			for seg_index in xrange(self.seg_num):
				dd_layer[seg_index]=[]
			for line in lines:
				inf_node=line.split()
				rad_node=inf_node[0]
				phi_node=float(inf_node[1])
				dd_node=float(inf_node[3])
				for seg_index in xrange(self.seg_num):
					phi_seg=phi_per_seg*seg_index if (phi_per_seg*seg_index)<m.pi else (phi_per_seg*seg_index-2*m.pi)
					if abs(phi_node-phi_seg)<1.e-6:
						dd_layer[seg_index].append(dd_node)
			dd_dictionary[self.layer_num]=dd_layer
		
		#---------------------------------------calculate the mean-----------------------------------------------#
		if self.layer_num:
			for rad_index in xrange(node_num_per_phi):
				sum_in_phi_layer=0
				for seg_index in xrange(self.seg_num):
					for layer_index in xrange(self.layer_num):
						dd_specific_point=dd_dictionary[layer_index][seg_index][rad_index]
						sum_in_phi_layer+=dd_specific_point
				mean_in_phi_layer=sum_in_phi_layer/(self.seg_num*self.layer_num) 
				mean_in_phi_layers.append(mean_in_phi_layer)
		else:
			for rad_index in xrange(node_num_per_phi):
				sum_in_phi_layer=0
				for seg_index in xrange(self.seg_num):
					dd_specific_point=dd_dictionary[self.layer_num][seg_index][rad_index]
					sum_in_phi_layer+=dd_specific_point
				mean_in_phi_layer=sum_in_phi_layer/(self.seg_num) 
				mean_in_phi_layers.append(mean_in_phi_layer)
		#file_mean=file_dat.replace('.dat','_mean.txt')
		
		with open(file_mean,'w') as outfile:
			for word in rad_distribution:
				outfile.write(str(word)+'  ')
			outfile.write('\n')
			for word in mean_in_phi_layers:
				outfile.write(str(word)+'  ')
				
		print('spatial mean of %s saved to:'%file_dat+file_mean)
		return rad_distribution,mean_in_phi_layers
	
class Ensemble_mean:
	'''
	Calculate the mean of drawdown values of many ensembles with the property of radial meshes.
	'''
	def __init__(self, Ens, Geo_type, Mesh_type, seg_num, layer_num=0):
		'''
		Ens(integer)					--Ensemble type
	
		Geo_typ(integer)				--Geometry type
	
		Mes_typ(integer_				--Mesh type
	
		seg_num(int)					 --the number of segments
	 			
		Optional input
		----------
		layer_num(int)					--number of layers
		
		'''
		self.Ens, self.Geo_type, self.Mesh_type, self.seg_num, self.layer_num=\
		Ens, Geo_type, Mesh_type, seg_num, layer_num
		
	def __call__(self, sim_num_start, total_sim_num):
		'''
		Calculate the mean of drawdown values of many ensembles with the property of radial meshes.
		
		Definition
		----------
		def mean_generator_radial_mesh(Ens,Geo_typ,Mes_typ,sim_num_start,sim_num_start+total_sim_num):
		
		Input
		----------
		sim_num_start(int)					--the start number of simulation			  

		total_sim_num(int)					--the number of simulations
		
		
		'''
		dd_infs=[]#a list to store all ensembles' drawdowns with every element being a list of drawdowns of ensemble
		dd_means=[]
		for sim_index in range(sim_num_start,sim_num_start+total_sim_num):
			if self.layer_num: #3D
				infile_path='/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d_L%d/S%d/Theis3D_Ens%d_G%d_M%d_L%d_spa_mean.dat'\
				%(self.Ens, self.Geo_type, self.Mesh_type, self.layer_num, sim_index, self.Ens, self.Geo_type, self.Mesh_type, self.layer_num)
			else:
				infile_path='/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d/S%d/Theis2D_Ens%d_G%d_M%d_spa_mean.dat'\
				%(self.Ens, self.Geo_type, self.Mesh_type, sim_index, self.Ens, self.Geo_type,self.Mesh_type)
				
			with open(infile_path,'r') as infile:
				distances=[]
				dds=[]
				for i,line in enumerate(infile):
					words=line.split()
					if i==0:
						
						for word in words:
							distances.append(float(word))
					elif i==1:	
						for word in words:
							dds.append(float(word))
			dd_inf=dds
			dd_infs.append(dd_inf)
		
		
		for rad_index in range(len(dds)):
			dd_point_sum=0
			for sim_index in range(total_sim_num):
				dd_point_inf=dd_infs[sim_index][rad_index]
				dd_point_sum+=dd_point_inf
			dd_point_mean=dd_point_sum/total_sim_num
			dd_means.append(dd_point_mean)	
			
		if not self.layer_num: #2D
			outfile_path='/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d/Ensemble_mean_%d-%d.txt'\
			%(self.Ens, self.Geo_type, self.Mesh_type, sim_num_start, sim_num_start+total_sim_num-1)
		else:
			outfile_path='/work/miao/Pumping_Test/log-normal_Kfield_Ens%d_G%d_M%d_L%d/Ensemble_mean_%d-%d.txt'\
			%(self.Ens, self.Geo_type, self.Mesh_type, self.layer_num, sim_num_start, sim_num_start+total_sim_num-1)

		with open(outfile_path,'w') as outfile:
			for word in distances:
					outfile.write(str(word)+'  ')
			outfile.write('\n')
			for word in dd_means:
					outfile.write(str(word)+'  ')
		
		'''	
		#save results with format 2
		with open(outfile_path,'w') as outfile:
			for i in range(len(distances)):
				column0=distances[i]
				column1=dd_means[i]
				outfile.write(str(column0)+'	'+str(column1)+'\n')
		'''
		return distances, dd_means
		