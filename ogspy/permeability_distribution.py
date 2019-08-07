# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 11:35:01 2015

@author: miao
"""
import os
#import sys
import shutil

class PER:

	"""
	Generate all input files according to specific radial mesh.
	"""
	
	def __init__(self, task_root, task_ID, Kfield_root, Kfield_name):
		'''
		Input
		----------
		
		task_root(string):  	-path of dir of this task
		
		task_ID(string)				--name of task
		
		'''
		#self.file_msh, self.well_radius, self.bound_radius = file_msh, well_radius, bound_radius
		#self.absolute_depth,self.layer_number = absolute_depth, layer_number
		self.task_root = task_root
		self.task_ID = task_ID
		self.Kfield_root = Kfield_root
		self.Kfield_name = Kfield_name
	def copy_file(self):
		'''
		move msh file from original dir to target dir.
		'''
		src_file= os.path.join(self.Kfield_root, self.Kfield_name)
		#os.chmod(src_file, 755)
		if not os.path.exists(self.task_root):
			os.makedirs(self.task_root)
		dst_file = os.path.join(self.task_root, self.Kfield_name)
		if not os.path.isfile(dst_file):
			shutil.copy2 (src_file, self.task_root)
		#dst_file = os.path.join(self.task_root, self.Kfield_name)
		#new_dst_file_name=os.path.join(self.task_root, self.task_ID + '.msh')
		#if not os.path.isfile(new_dst_file_name):
			#os.rename(dst_file, new_dst_file_name)
		print('MSH-file copied to dictionary: ' + self.task_root) 