# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 11:35:01 2015

@author: miao
"""
import os
import sys
import shutil

class MESH_ANA:
	"""
	Class for preprocessing of radial meshes.
	"""
	def __init__(self, msh_root, msh_name, well_radius, bound_radius, absolute_depth=0,layer_number=0):
		'''
		Input
		----------
		msh_root(string):  			-- full path of msh file dir 
		
		msh_name(string)			-- name of mesh file
		
		well_radius(float)			--radius of well
	 
		bound_radius(float)			--radius of boundary
		
		Optional Input
		----------
		absolute_depth(float)		--absolute depth of model(positive)
	 
		layer_number(int)			--the number of layers(in case of 2D equals to 0)
		'''
		self.msh_root, self.msh_name, self.well_radius, self.bound_radius\
          = msh_root, msh_name, well_radius, bound_radius
		self.absolute_depth,self.layer_number = absolute_depth, layer_number
		
	def __call__(self):
		'''
		Return the number of segments, the x coordinates of points at x axis(list), the information of well points and the information of boundary points.
		
		Output
		----------
		radial_node_dis(lis --x coordinates of points located at x axis (list).
	 
		well_infs(dictionary)		--dictionary of information(index,coordinates) of well points 
	 
		BC_infs(dictionary)		--dictionary of information(index,coordinates) of BC points
		
		'''
		
		file_msh = os.path.join( self.msh_root, self.msh_name)
		infile=open(file_msh,'r')
		#node_coos=[]
		indexs={}
		radial_node_dis=[] #list of x coordinates of nodes in x axis in the ascending order
		for i, line in enumerate(infile):
			if i==4:
				nod_num=int(line)
			elif i>4:
				break
		infile.close()
				
		infile=open(file_msh,'r')
		for i, line in enumerate(infile):

			if (i>4)and(i<=nod_num+4):
				coos=line.split()
				index=int(coos[0])
				coo_x=float(coos[1])
				coo_y=float(coos[2])
				coo_z=float(coos[3])
				if (not coo_y) and (not coo_z) and (coo_x>0):#extract those points located at x axis
					
					radial_node_dis.append(coo_x)
					indexs[coo_x]=index
			elif i>(nod_num+6):
				break
		infile.close()
		radial_node_dis=sorted(radial_node_dis) #sort the numbers in the ascending number
		num_inds=[]
		for coo_x in radial_node_dis:
			num_ind=indexs[coo_x]
			num_inds.append(num_ind)
		
		#welltype=('Well type:vector' if radial_node_dis[0] else 'well type:point')
		#print nod_num,ele_num,radial_node_dis
		infile=open(file_msh,'r')
		well_infs={}
		BC_infs={}
		for layer in range(self.layer_number+1):
			well_infs[layer]=[]
			BC_infs[layer]=[]
		for i, line in enumerate(infile):
			if (i>4)and(i<=nod_num+4):
				coos=line.split()
				index=int(coos[0])
				coo_x=float(coos[1])
				coo_y=float(coos[2])
				coo_z=float(coos[3])
				for layer in range(self.layer_number+1):
					try:
						layer_depth=-layer*(self.absolute_depth/self.layer_number)
					except: # 2D case
						layer_depth=0
					if (abs((coo_x*coo_x+coo_y*coo_y)-self.well_radius*self.well_radius)<1e-5) and (abs(coo_z-layer_depth)<1e-5):
						well_inf=[index,coo_x,coo_y,coo_z]
						well_infs[layer].append(well_inf)
					elif (abs((coo_x*coo_x+coo_y*coo_y)-self.bound_radius*self.bound_radius)<1e-1) and (abs(coo_z-layer_depth)<1e-5):
						BC_inf=[index,coo_x,coo_y,coo_z]
						BC_infs[layer].append(BC_inf)
		seg_num=len(well_infs[0])				
		infile.close()
		
		return seg_num,radial_node_dis, well_infs, BC_infs
