
from ogspy.base import OGS_File
from bidict import bidict

import numpy as np
import os
import shutil

elem_typ = {"line" : 0, "tri" : 1, "quad" : 2, "tet" : 3, "pyra" : 4,
            "pris" : 5, "hex" : 6}

node_no = {"line" : 2, "tri" : 3, "quad" : 4, "tet" : 4, "pyra" : 5,
           "pris" : 6, "hex" : 8}

class MSH(OGS_File):
    
    """
    Class for the ogs output file.

    History
    -------
    Written,  JM, Jul 2015
    Modified, FH, Jul 2015 - rewritten for geneneral purpose ogs projects    
    
    """
	
    def __init__(self, **OGS_Config):
        '''
        Input
        ----------
        
        OGS_Config dictonary         
		
        '''
        
        OGS_File.__init__(self, **OGS_Config)
        
        self.f_type = '.msh'
        
    def import_mesh(self, msh_root, msh_name):
        
        self.block_no = 1
        f_name = msh_root + msh_name
        
        with open(f_name, 'r') as f_obj:
            f_lines = f_obj.readlines()
        
        self.node_no = int(f_lines[4])
        self.element_no = int(f_lines[6 + self.node_no])
        element_type = f_lines[7 + self.node_no].split()
        self.element_type = element_type[2]
        self.node_per_element_no = len(element_type) - 3
        
        a = 5
        b = 5 + self.node_no
        node_lines = f_lines[a:b]
        a = 7 + self.node_no
        b = 7 + self.node_no + self.element_no
        element_lines = f_lines[a:b]
        
#        self.node_array = []
        self.node_array = bidict()
        self.element_array = []
        
        for node_i in range(self.node_no):
            self.node_array[node_i] = tuple([float(i) \
            for i in node_lines[node_i].split()[1:]])
            
        for element_i in range(self.element_no):
            line = element_lines[element_i].split()
            tmp = [None]*(len(line))
            tmp[0] = int(line[0])
            tmp[1] = int(line[1])
            tmp[2] = line[2]
            for i in range(len(line)-3):
                tmp[i+3] = int(line[i+3])
            self.element_array.append(tmp)
                
        self.get_centroid_of_elements()
        
        
    def get_centroid_of_elements(self):
        self.centroid_array = np.zeros((self.element_no, 3))
        for element_i in range(self.element_no):
            self.centroid_array[element_i,:] = self.get_centroid_of_single_element(element_i)
                
    def get_centroid_of_single_element(self, element_i):
        centroid = np.zeros((3))
        for i in range(len(centroid)):
            centroid[i] = np.mean([num[i] for num in \
            self.get_element_node_pos(self.element_array[element_i][3:])] )
        return centroid
    
    def slice_hexagon(self, min_x = None, max_x = None, min_y = None, 
                            max_y = None, min_z = None, max_z = None, 
                            slice_no = 1, direction = 'x'):

        ''' Method for slicing a hexagon into a number of equally spaced
        slices. As of yet, the method assumes a the hexaeder to be a cuboid.
        For other forms like a parallelepiped or trapezohedron, the method has 
        to and can be amended.'''

        node_per_slice_no = 4

        if direction == 'x':
            slice_pos_x = np.zeros((slice_no))   
            plane_down = [0, 3, 4, 7]
#            plane_up = [1, 2, 5, 7]
            node_list = [3, 6, 7, 10, 4, 5, 8, 9]
        elif direction == 'y':
            slice_pos_y = np.zeros((slice_no))
            plane_down = [0, 1, 4, 5]
#            plane_up = [2, 3, 6, 7]
            node_list = [3, 4, 7, 8, 6, 5, 10, 9]
        elif direction == 'z':
            slice_pos_z = np.zeros((slice_no))
            plane_down = [0, 1, 2, 3]
#            plane_up = [4, 5, 6, 7]
            node_list = [3, 4, 5, 6, 7, 8, 9, 10]

        selected_elements = self.select_elements(min_x, max_x, min_y, max_y, 
                                                 min_z, max_z)
        for element_i in selected_elements:
            
            slice_node_array = np.zeros((slice_no, node_per_slice_no, 3))  
            slice_id_array = np.zeros((slice_no, node_per_slice_no))                      
            element_nodes = self.expand_node_id(self.element_array[element_i][3:])
            
            # initialize the slice by copying the values from the leftmost plane and
            # correct the x values in every node of the slice (only works for cuboid)
            if direction == 'x':
                delta = np.abs(element_nodes[0][0] - element_nodes[1][0])
            elif direction == 'y':
                delta = np.abs(element_nodes[1][1] - element_nodes[2][1])
            elif direction == 'z':
                delta = np.abs(element_nodes[0][2] - element_nodes[4][2])
            
            for j in range(slice_no):
                if direction == 'x':
                    slice_pos_x[j] = element_nodes[0][0] + delta*(j+1)/(slice_no+1)
                elif direction == 'y':
                    slice_pos_y[j] = element_nodes[0][1] + delta*(j+1)/(slice_no+1)
                elif direction == 'z':
                    slice_pos_z[j] = element_nodes[0][2] + delta*(j+1)/(slice_no+1)
                for k in range(node_per_slice_no):
                    slice_node_array[j][k][:] = list(element_nodes[plane_down[k]])
                    if direction == 'x':
                        slice_node_array[j][k][0] = slice_pos_x[j]
                    elif direction == 'y':
                        slice_node_array[j][k][1] = slice_pos_y[j]
                    elif direction == 'z':
                        slice_node_array[j][k][2] = slice_pos_z[j]    
                # check whether these new nodes were already created and add only new nodes that weren't already created
                for k in range(node_per_slice_no):
                    slice_id_array[j][k] = self.insert_new_node(slice_node_array[j][k][:])

            # create the inner new elements and add it to the list
            if slice_no > 1:
                for j in range(1, slice_no):
                    self.element_array.append(self.element_array[element_i][:])
                    self.element_array[-1][0] = self.element_array[-2][0] + 1
                    for l in range(node_per_slice_no):
                        self.element_array[-1][node_list[l]] = slice_id_array[j-1][l]
                        self.element_array[-1][node_list[l+4]] = slice_id_array[j][l]
            
            # create the outer (right- and leftmost) new elements
            self.element_array.append(self.element_array[element_i][:])
            self.element_array[-1][0] = self.element_array[-2][0] + 1
            for l in range(node_per_slice_no):
                self.element_array[-1][node_list[l]] = slice_id_array[-1][l]                   
                self.element_array[element_i][node_list[l+4]] = slice_id_array[0][l]

        self.node_no = len(self.node_array)
        self.element_no = len(self.element_array)
    
    
    def refine_hexagon(self, min_x = None, max_x = None, min_y = None,
                             max_y = None, min_z = None, max_z = None,
                             slice_x = 0, slice_y = 0, slice_z = 0):
        ''' Method for refining the resolution of a hexagon by slicing it
        into smaller hexagons.'''
        
        selected_elements = self.select_elements(min_x, max_x, min_y, max_y, 
                                                 min_z, max_z, sort = True)     
        element_order = self.get_element_order(slice_x = slice_x,
                                               slice_y = slice_y,
                                               slice_z = slice_z)
        node_order = self.get_node_order(slice_x = slice_x, 
                                         slice_y = slice_y, 
                                         slice_z = slice_z)
#        print(node_order)
#        print(element_order)
        self.replace_elements(selected_elements, element_order, node_order)
        self.get_centroid_of_elements()
        
    def hex_transition(self, min_x = None, max_x = None, min_y = None,
                             max_y = None, min_z = None, max_z = None,
                             direction = 'lower', rotation = [0, 0, 0],
                             slice_no = 1):
        ''' Method for transition a hexagon between two resolutions.'''
        
        selected_elements = self.select_elements(min_x, max_x, min_y, max_y, 
                                                 min_z, max_z)
        selected_elements = sorted(selected_elements, reverse=True)

        if slice_no == 1:
            element_order = [[ 2, 10,  1,  7, 11,  6], [ 2,  3, 10,  7,  4, 11],
                             [ 0,  8, 10,  5,  9, 11], [ 8,  1, 10,  9,  6, 11], 
                             [ 0, 10,  3,  5, 11,  4]]           
            pre_node_order = [[0.0, 0.0, 0], [1.0, 0.0, 0], [1.0, 1.0, 0],
                              [0.0, 1.0, 0], [0.0, 1.0, 1], [0.0, 0.0, 1],
                              [1.0, 0.0, 1], [1.0, 1.0, 1], [0.5, 0.0, 0],
                              [0.5, 0.0, 1], [0.5, 0.5, 0], [0.5, 0.5, 1]]        
        elif slice_no == 4:
            element_order = [[8, 9, 10, 11, 12, 13, 14, 15], [11, 10, 2, 3, 15, 14, 6, 7,],
                             [20, 21, 9, 8, 22, 23, 13, 12], [0, 8, 11, 3, 4, 12, 15, 7],
                             [9, 1, 2, 10, 13, 5, 6, 14], [0, 16, 8, 4, 18, 12],
                             [16, 20,  8, 18, 22, 12], [21, 17, 9, 23, 19, 13],
                             [17,  1,  9, 19,  5, 13]]
            pre_node_order = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], 
                              [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], 
                              [1.0, 1.0, 1.0], [0.0, 1.0, 1.0], [0.2, 0.2, 0.0],
                              [0.8, 0.2, 0.0], [0.8, 0.8, 0.0], [0.2, 0.8, 0.0],
                              [0.2, 0.2, 1.0], [0.8, 0.2, 1.0], [0.8, 0.8, 1.0],
                              [0.2, 0.8, 1.0], [0.2, 0.0, 0.0], [0.8, 0.0, 0.0], 
                              [0.2, 0.0, 1.0], [0.8, 0.0, 1.0], [0.4, 0.0, 0.0], 
                              [0.6, 0.0, 0.0], [0.4, 0.0, 1.0], [0.6, 0.0, 1.0]]
        elif slice_no == 9:
            element_order = [[20, 12, 21, 27, 19, 28], [21, 13, 20, 28, 14, 27],
                             [12,  2, 21, 19,  6, 28], [21,  3, 13, 28,  7, 14],
                             [22,  8,  9, 29, 15, 16], [23, 10, 11, 25, 17, 18],
                             [23, 12, 20, 25, 19, 27], [20, 13, 22, 27, 14, 29],
                             [24,  9, 10, 26, 16, 17], [ 0,  8, 22,  4, 15, 29],
                             [22,  9, 24, 29, 16, 26], [24, 10, 23, 26, 17, 25],
                             [23, 11,  1, 25, 18,  5], [22, 13,  0, 29, 14,  4],
                             [ 1, 12, 23,  5, 19, 25], [23, 20, 24, 25, 27, 26],
                             [24, 20, 22, 26, 27, 29], [21,  2,  3, 28,  6,  7],
                             [30, 31,  8,  0, 36, 37, 15,  4],
                             [31, 32,  9,  8, 37, 38, 16, 15],
                             [32, 33, 10,  9, 38, 39, 17, 16],
                             [33, 34, 11, 10, 39, 40, 18, 17],
                             [34, 35,  1, 11, 40, 41,  5, 18]]
            pre_node_order = [[0.0, 0.25,0], [1.0, 0.25,0], [1.0, 1.0, 0],
                              [0.0, 1.0, 0], [0.0, 0.25,1], [1.0, 0.25,1],
                              [1.0, 1.0, 1], [0.0, 1.0, 1], [0.2, 0.25,0],
                              [0.4, 0.25,0], [0.6, 0.25,0], [0.8, 0.25,0],
                              [1.0, 0.5, 0], [0.0, 0.5, 0], [0.0, 0.5, 1],
                              [0.2, 0.25,1], [0.4, 0.25,1], [0.6, 0.25,1], 
                              [0.8, 0.25,1], [1.0, 0.5, 1], [0.5, 0.5, 0],
                              [0.5, 0.75,0], [0.2, 0.37,0], [0.8, 0.37,0],
                              [0.5, 0.37,0], [0.8, 0.37,1], [0.5, 0.37,1],
                              [0.5, 0.5, 1], [0.5, 0.75,1], [0.2, 0.37,1],
                              [0.0, 0.0, 0], [0.2, 0.0, 0], [0.4, 0.0, 0],
                              [0.6, 0.0, 0], [0.8, 0.0, 0], [1.0, 0.0, 0],
                              [0.0, 0.0, 1], [0.2, 0.0, 1], [0.4, 0.0, 1],
                              [0.6, 0.0, 1], [0.8, 0.0, 1], [1.0, 0.0, 1]]
        
        if np.sum(rotation) == 0:
            node_order = pre_node_order
        else:
            node_order = self.rotate_element(pre_node_order, rotation = rotation)
        self.replace_elements(selected_elements, element_order, node_order)
        self.get_centroid_of_elements()
    
    def hex_transition_2(self, min_x = None, max_x = None, min_y = None,
                               max_y = None, min_z = None, max_z = None,
                               direction = 'lower', rotation = [0, 0, 0]):
        ''' Method for transition a hexagon between two resolutions.'''
        
        ##-- refine all elements ----------------------------------------------
        
        self.refine_hexagon(min_x, max_x, min_y, max_y, min_z, max_z,
                            slice_x = 4, slice_y = 4, slice_z = 0)
        
        ##-- refine lower elements --------------------------------------------
        
        if direction == 'lower':
            self.hex_transition(min_x = min_x, max_x = max_x,
                                min_y = min_y - 25, max_y = max_y + 25,
                                rotation = rotation, slice_no = 1)
            self.refine_hexagon(min_x, max_x, 
                                min_y - 75, max_y - 25, 
                                min_z, max_z,
                                slice_x = 1, slice_y = 0, slice_z = 0)
        elif direction == 'upper':
            self.hex_transition(min_x = min_x, max_x = max_x,
                                min_y = min_y - 25, max_y = max_y + 25,
                                rotation = rotation, slice_no = 1)
            self.refine_hexagon(min_x, max_x, 
                                min_y + 25, max_y + 75, 
                                min_z, max_z,
                                slice_x = 1, slice_y = 0, slice_z = 0)
        elif direction == 'left':
            self.hex_transition(min_x = min_x - 25, max_x = max_x + 25,
                                min_y = min_y, max_y = max_y,
                                rotation = rotation, slice_no = 1)
            self.refine_hexagon(min_x - 75, max_x - 25, 
                                min_y, max_y, 
                                min_z, max_z,
                                slice_x = 0, slice_y = 1, slice_z = 0)                    
        elif direction == 'right':
            self.hex_transition(min_x = min_x - 25, max_x = max_x + 25,
                                min_y = min_y, max_y = max_y,
                                rotation = rotation, slice_no = 1)
            self.refine_hexagon(min_x + 25, max_x + 75, 
                                min_y, max_y, 
                                min_z, max_z,
                                slice_x = 0, slice_y = 1, slice_z = 0)                               
        self.get_centroid_of_elements()
        
        ##-- lower elements ---------------------------------------------------
        
        if direction == 'lower':
            self.refine_hexagon(min_x, max_x, 
                                min_y - 125, max_y - 75, 
                                min_z, max_z,
                                slice_x = 1, slice_y = 3, slice_z = 0)
            self.hex_transition(min_x, max_x, 
                                min_y - 125, max_y - 112, 
                                min_z, max_z,
                                rotation = [0, 1, 0], slice_no = 4)  
        elif direction == 'upper':
            self.refine_hexagon(min_x, max_x, 
                                min_y + 75, max_y + 125, 
                                min_z, max_z,
                                slice_x = 1, slice_y = 3, slice_z = 0)     
            self.hex_transition(min_x, max_x, 
                                min_y + 112, max_y + 125, 
                                min_z, max_z, 
                                rotation = [0, 1, 2], slice_no = 4) 
        elif direction == 'left':
            self.refine_hexagon(min_x - 125, max_x - 75, 
                                min_y, max_y, 
                                min_z, max_z,
                                slice_x = 3, slice_y = 1, slice_z = 0)     
            self.hex_transition(min_x - 125, max_x - 112, 
                                min_y, max_y, 
                                min_z, max_z, 
                                rotation = [0, 1, 1], slice_no = 4) 
        elif direction == 'right':
            self.refine_hexagon(min_x + 75, max_x + 125, 
                                min_y, max_y, 
                                min_z, max_z,
                                slice_x = 3, slice_y = 1, slice_z = 0) 
            self.hex_transition(min_x + 112, max_x + 125, 
                                min_y, max_y, 
                                min_z, max_z, 
                                rotation = [0, 1, 3], slice_no = 4) 
        self.get_centroid_of_elements()


    def hex_transition_3(self, min_x = None, max_x = None, min_y = None,
                               max_y = None, min_z = None, max_z = None,
                               direction = 'lower-right'):
        ''' Method for transition a hexagon between two resolutions at the 
        corner.'''
        
        ##-- all elements -----------------------------------------------------
        
        self.refine_hexagon(min_x, max_x, min_y, max_y, min_z, max_z,
                            slice_x = 4, slice_y = 4, slice_z = 0)
        
        ##-- border elements --------------------------------------------------
        
        if direction == 'lower-right':
            self.hex_to_prism(min_x = min_x + 25, max_x = max_x + 75,
                              min_y = min_y - 125, max_y = max_y - 75,
                              right = True)
            self.hex_to_prism(min_x = min_x + 75, max_x = max_x + 125,
                              min_y = min_y - 75, max_y = max_y - 25,
                              lower = True)
            self.refine_hexagon(min_x = min_x + 75, max_x = max_x + 125,
                                min_y = min_y - 125, max_y = max_y - 75,
                                slice_x = 1, slice_y = 1, slice_z = 0)
            self.hex_to_prism(min_x = min_x + 75, max_x = max_x + 100,
                              min_y = min_y - 125, max_y = max_y - 100,
                              lower = True, right = True)
            self.hex_to_prism(min_x = min_x + 100, max_x = max_x + 125,
                              min_y = min_y - 100, max_y = max_y - 75,
                              lower = True, right = True)                  
            self.refine_hexagon(min_x = min_x + 100, max_x = max_x + 125,
                                min_y = min_y - 125, max_y = max_y - 100,
                                slice_x = 1, slice_y = 1, slice_z = 0)
        elif direction == 'upper-right':
            self.hex_to_prism(min_x = min_x + 25, max_x = max_x + 75,
                              min_y = min_y + 75, max_y = max_y + 125,
                              right = True)
            self.hex_to_prism(min_x = min_x + 75, max_x = max_x + 125,
                              min_y = min_y + 25, max_y = max_y + 75,
                              upper = True)
            self.refine_hexagon(min_x = min_x + 75, max_x = max_x + 125,
                                min_y = min_y + 75, max_y = max_y + 125,
                                slice_x = 1, slice_y = 1, slice_z = 0)
            self.hex_to_prism(min_x = min_x + 75, max_x = max_x + 100,
                              min_y = min_y + 100, max_y = max_y + 125,
                              upper = True, right = True)
            self.hex_to_prism(min_x = min_x + 100, max_x = max_x + 125,
                              min_y = min_y + 75, max_y = max_y + 100,
                              upper = True, right = True)                  
            self.refine_hexagon(min_x = min_x + 100, max_x = max_x + 125,
                                min_y = min_y + 100, max_y = max_y + 125,
                                slice_x = 1, slice_y = 1, slice_z = 0)
        elif direction == 'lower-left':
            self.hex_to_prism(min_x = min_x - 75, max_x = max_x - 25,
                              min_y = min_y - 125, max_y = max_y - 75,
                              left = True)
            self.hex_to_prism(min_x = min_x - 125, max_x = max_x - 75,
                              min_y = min_y - 75, max_y = max_y - 25,
                              lower = True)
            self.refine_hexagon(min_x = min_x -125, max_x = max_x - 75,
                                min_y = min_y - 125, max_y = max_y - 75,
                                slice_x = 1, slice_y = 1, slice_z = 0)
        
            self.hex_to_prism(min_x = min_x - 100, max_x = max_x - 75,
                              min_y = min_y - 125, max_y = max_y - 100,
                              lower = True, left = True)
            self.hex_to_prism(min_x = min_x - 125, max_x = max_x - 100,
                              min_y = min_y - 100, max_y = max_y - 75,
                              lower = True, left = True)
            self.refine_hexagon(min_x = min_x - 125, max_x = max_x - 100,
                                min_y = min_y - 125, max_y = max_y - 100,
                                slice_x = 1, slice_y = 1, slice_z = 0)
        elif direction == 'upper-left':
            self.hex_to_prism(min_x = min_x - 75, max_x = max_x - 25,
                              min_y = min_y + 75, max_y = max_y + 125,
                              left = True)
            self.hex_to_prism(min_x = min_x - 125, max_x = max_x - 75,
                              min_y = min_y + 25, max_y = max_y + 75,
                              upper = True)
            self.refine_hexagon(min_x = min_x -125, max_x = max_x - 75,
                                min_y = min_y + 75, max_y = max_y + 125,
                                slice_x = 1, slice_y = 1, slice_z = 0)
        
            self.hex_to_prism(min_x = min_x - 100, max_x = max_x - 75,
                              min_y = min_y + 100, max_y = max_y + 125,
                              upper = True, left = True)
            self.hex_to_prism(min_x = min_x - 125, max_x = max_x - 100,
                              min_y = min_y + 75, max_y = max_y + 100,
                              upper = True, left = True)
            self.refine_hexagon(min_x = min_x - 125, max_x = max_x - 100,
                                min_y = min_y + 100, max_y = max_y + 125,
                                slice_x = 1, slice_y = 1, slice_z = 0)
    
    def hex_corner_z(self, min_x = None, max_x = None, min_y = None,
                           max_y = None, min_z = None, max_z = None, 
                           direction = 'lower-right', axis = 'z'):
        
        selected_elements = self.select_elements(min_x, max_x, min_y, max_y, 
                                                 min_z, max_z, sort = True)
                           
        element_order = [[ 8, 9,10,11,12,13,14,15], [11,10, 2, 3,15,14, 6, 7],
                         [12,13,14,15, 4, 5, 6, 7], [16,17, 9, 8,18,19,13,12],
                         [ 0, 1, 2, 3, 8, 9,10,11], [ 0, 8,11, 3, 4,12,15, 7],
                         [ 9,20,21,10,13,23,22,14], [10,21, 2,14, 22, 6],
                         [ 0,16, 8, 1,17, 9], [ 4,18,12, 5,19,13], [ 0,16, 8, 4,18,12],
                         [ 1,20, 9, 2,21,10], [ 5,23,13, 6,22,14], [17,24,20, 9, 1],
                         [19,25,23,13, 5], [17,26, 9,19,27,13], [ 9,26,20,13,27,23],
                         [17,24,20, 9,26], [19,25,23,13,27]]
                         
        pre_node_order = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0],
                          [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0],
                          [1.0, 1.0, 1.0], [0.0, 1.0, 1.0], [0.2, 0.2, 0.2],
                          [0.8, 0.2, 0.2], [0.8, 0.8, 0.2], [0.2, 0.8, 0.2],
                          [0.2, 0.2, 0.8], [0.8, 0.2, 0.8], [0.8, 0.8, 0.8],
                          [0.2, 0.8, 0.8], [0.2, 0.0, 0.2], [0.8, 0.0, 0.2],
                          [0.2, 0.0, 0.8], [0.8, 0.0, 0.8], [1.0, 0.2, 0.2],
                          [1.0, 0.8, 0.2], [1.0, 0.8, 0.8], [1.0, 0.2, 0.8],
                          [1.0, 0.0, 0.2], [1.0, 0.0, 0.8], [1.0, 0.0, 0.4],
                          [1.0, 0.0, 0.6]]
                
        node_order = self.rotate_node_order(pre_node_order, direction, axis)
        self.replace_elements(selected_elements, element_order, node_order)
        self.get_centroid_of_elements()

    
    def replace_elements(self, selected_elements, element_order, node_order):
        
        for element_i in selected_elements:
            
            ##-- creating the list of nodes -----------------------------------
            old_node_list = self.expand_node_id(self.element_array[element_i][3:])

            x_max = old_node_list[1][0]
            y_max = old_node_list[2][1]
            z_max = old_node_list[4][2]
            dx = np.abs(old_node_list[0][0] - x_max)
            dy = np.abs(old_node_list[1][1] - y_max)
            dz = np.abs(old_node_list[0][2] - z_max)
            node_zero = old_node_list[0][:]
            
            node_list = []
            for i in range(len(node_order)):
                node_list.append(node_zero[:])
                if node_order[i][0] == 1.:
                    node_list[-1][0] = x_max
                else:
                    node_list[-1][0] += node_order[i][0]*dx
                if node_order[i][1] == 1.:
                    node_list[-1][1] = y_max
                else:
                    node_list[-1][1] += node_order[i][1]*dy
                if node_order[i][2] == 1.:
                    node_list[-1][2] = z_max
                else:
                    node_list[-1][2] += node_order[i][2]*dz
            
            ##-- creating the list of id's of the nodes -----------------------
            node_id_list = [None]*len(node_list)
            for i in range(len(node_list)):
                node_id_list[i] = self.insert_new_node(node_list[i])
                
            ##-- creating the list of new elements ----------------------------
            element_list = [None]*len(element_order)
            geo_unit = self.element_array[element_i][1]
            for i in range(len(element_order)):
                element_len = len(element_order[i])
#                print(element_len)
                new_element = [None]*(element_len+3)
                if i == 0:
                    new_element[0] = self.element_array[element_i][0]
                else:
                    new_element[0] = int(self.element_no + i - 1)
                new_element[1] = geo_unit
                if element_len == 5:
                    new_element[2] = 'pyra'
                if element_len == 6:
                    new_element[2] = 'pris'
                elif element_len == 8:
                    new_element[2] = 'hex'
                for j in range(element_len):
                    new_element[j+3] = node_id_list[element_order[i][j]]
                element_list[i] = new_element
            
            ##-- adding the new elements to the list --------------------------
            self.element_array[element_i] = element_list[0]
            for i in range(1, len(element_list)):
                self.element_array.append(element_list[i]) 
            
        self.element_no = len(self.element_array)
        self.node_no = len(self.node_array)
    
    
    def get_element_order(self, slice_x = 0, slice_y = 0, slice_z = 0):
        ''' Method for determining the order of the elements.'''
        
        element_no = ((slice_z + 1)*(slice_y + 1)*(slice_x + 1))
        element_order = [None]*element_no
        
        element_i = 0
        for k in range(slice_z + 1):
            for j in range(slice_y + 1):
               for i in range(slice_x + 1):
                   tmp = [None]*8
                   tmp[0] = i + j*(slice_x+2)
                   tmp[1] = i + j*(slice_x+2) + 1
                   tmp[2] = i + (j+1)*(slice_x+2) + 1
                   tmp[3] = i + (j+1)*(slice_x+2)
                   tmp[4] = i + j*(slice_x+2) + (k+1)*(slice_x+2)*(slice_y+2)
                   tmp[5] = i + j*(slice_x+2) + (k+1)*(slice_x+2)*(slice_y+2) + 1
                   tmp[6] = i + (j+1)*(slice_x+2) + (k+1)*(slice_x+2)*(slice_y+2) + 1
                   tmp[7] = i + (j+1)*(slice_x+2) + (k+1)*(slice_x+2)*(slice_y+2)
                   element_order[element_i] = tmp 
                   element_i += 1
                         
        return element_order
        
    def get_node_order(self, direction = 'lower', 
                       slice_x = 0, slice_y = 0, slice_z = 0):
        ''' Method for determining the order of the nodes.'''
        
        pre_node_order = [None]*((slice_z + 2)*(slice_y + 2)*(slice_x + 2))
        pre_node_order_i = 0
        for k in range(slice_z + 2):
            for j in range(slice_y + 2):
               for i in range(slice_x + 2):
                   pre_node_order[pre_node_order_i] = [None]*3
                   pre_node_order[pre_node_order_i][0] = i/(slice_x + 1.)
                   pre_node_order[pre_node_order_i][1] = j/(slice_y + 1.)
                   pre_node_order[pre_node_order_i][2] = k/(slice_z + 1.)
                   pre_node_order_i += 1
        return pre_node_order
        
    
    def hex_to_prism(self, min_x = None, max_x = None, min_y = None,
                           max_y = None, min_z = None, max_z = None,
                           lower = False, left = False, 
                           upper = False, right = False):
        ''' Method for replacing a hexagon by a set of prisms.'''
        
        node_list_order = [[0.5, 0.5, 0.0], [0.5, 0.5, 1.0]]
        node_order = [[0, 1, 8, 4, 5, 9], [0, 8, 3, 4, 9, 7],
                      [2, 3, 8, 6, 7, 9], [2, 8, 1, 6, 9, 5]]
#        new_element_order = ['lower', 'left', 'upper', 'right']
        
        selected_elements = self.select_elements(min_x, max_x, min_y, max_y, 
                                                 min_z, max_z)
        selected_elements = sorted(selected_elements, reverse=True)
        
        for element_i in selected_elements:
            
            # creating the list of nodes
            node_list = [None]*8
#            print(node_list)
            node_list = self.expand_node_id(self.element_array[element_i][3:])
#            print(node_list)
            dx = np.abs(node_list[0][0] - node_list[1][0])
            dy = np.abs(node_list[1][1] - node_list[2][1])
#            dz = np.abs(node_list[0][2] - node_list[4][2])
            
            for i in range(2):
                if node_list_order[i][2] == 1.:
                    node_list.append(node_list[4][:])
                else:
                    node_list.append(node_list[0][:])
                node_list[-1][0] += node_list_order[i][0]*dx
                node_list[-1][1] += node_list_order[i][1]*dy
            
            # creating the list of node id's
            node_id_list = [None]*len(node_list)
            for i in range(len(node_list)):
                node_id_list[i] = self.insert_new_node(node_list[i])
#            print(len(self.node_array) - tmp)
#            tmp = len(self.node_array)
            
#            node_list.append(node_list[0][:])
#            node_list[-1][0] += node_x_list[1]*dx
#            node_list[-1][1] += node_y_list[1]*dy
#            node_list[-1][2] += node_z_list[1]*dz
#            self.insert_new_node(node_list[-1])
#            print(len(self.node_array) - tmp)
#            if (len(self.node_array) - tmp) > 0:
#                print('hello')
#                print(dz)
#                print(node_list[-2])
#                print(node_list[-1])
            # create the list of new elements
            element_list = [None]*4
            geo_unit = self.element_array[element_i][1]
            for i in range(len(element_list)):
                new_element = [None]*9
                if i == 0:
                    new_element[0] = self.element_array[element_i][0]
                else:
                    new_element[0] = int(self.element_no + i - 1)
                new_element[1] = geo_unit
                new_element[2] = 'pris'
                for j in range(6):
                    new_element[j+3] = node_id_list[node_order[i][j]]
                element_list[i] = new_element
            
            # mesh refinement if necessary  
            
            if lower == True:
                new_node_list = [None]*2
                new_node_id_list = [None]*2
                new_element = [None]*9
            
                new_node_list[0]= node_list[0][:]
                new_node_list[0][0] += dx/2
                new_node_list[1]= node_list[4][:]
                new_node_list[1][0] += dx/2
                
                new_node_id_list[0] = self.insert_new_node(new_node_list[0])
                new_node_id_list[1] = self.insert_new_node(new_node_list[1])
                
                new_element[:] = element_list[0][:]
                new_element[0] = int(self.element_no + len(element_list) - 1)
                new_element[3] = new_node_id_list[0]
                new_element[6] = new_node_id_list[1]
                element_list.append(new_element)
                
                element_list[0][4] = new_node_id_list[0]
                element_list[0][7] = new_node_id_list[1]
            if left == True:
                new_node_list = [None]*2
                new_node_id_list = [None]*2
                new_element = [None]*9
                
                new_node_list[0] = node_list[0][:]
                new_node_list[0][1] += dy/2
                new_node_list[1] = node_list[4][:]
                new_node_list[1][1] += dy/2
                
                new_node_id_list[0] = self.insert_new_node(new_node_list[0])
                new_node_id_list[1] = self.insert_new_node(new_node_list[1])
    
                new_element[:] = element_list[1][:]
                new_element[0] = int(self.element_no + len(element_list) - 1)
                new_element[3] = new_node_id_list[0]
                new_element[6] = new_node_id_list[1]
                element_list.append(new_element)
                
                element_list[1][5] = new_node_id_list[0]
                element_list[1][8] = new_node_id_list[1]
            if upper == True:
                new_node_list = [None]*2
                new_node_id_list = [None]*2
                new_element = [None]*9
                
                new_node_list[0] = node_list[3][:]
                new_node_list[0][0] += dx/2
                new_node_list[1] = node_list[7][:]
                new_node_list[1][0] += dx/2
                
                new_node_id_list[0] = self.insert_new_node(new_node_list[0])
                new_node_id_list[1] = self.insert_new_node(new_node_list[1])
                
                new_element[:] = element_list[2][:]
                new_element[0] = int(self.element_no + len(element_list) - 1)
                new_element[3] = new_node_id_list[0]
                new_element[6] = new_node_id_list[1]
                element_list.append(new_element)
                
                element_list[2][4] = new_node_id_list[0]
                element_list[2][7] = new_node_id_list[1]
            if right == True:
                new_node_list = [None]*2
                new_node_id_list = [None]*2
                new_element = [None]*9
                
                new_node_list[0] = node_list[1][:]
                new_node_list[0][1] += dy/2
                new_node_list[1] = node_list[5][:]
                new_node_list[1][1] += dy/2
                
                new_node_id_list[0] = self.insert_new_node(new_node_list[0])
                new_node_id_list[1] = self.insert_new_node(new_node_list[1])
                
                new_element[:] = element_list[3][:]
                new_element[0] = int(self.element_no + len(element_list) - 1)
                new_element[3] = new_node_id_list[0]
                new_element[6] = new_node_id_list[1]
                element_list.append(new_element)
                element_list[3][5] = new_node_id_list[0]
                element_list[3][8] = new_node_id_list[1]
#                print(new_node_list)

            # adding the new elements to the list
            self.element_array[element_i] = element_list[0]
            for i in range(1, len(element_list)):
                self.element_array.append(element_list[i])                
        
        # updating metainformation of the mesh
        self.element_no = len(self.element_array)
        self.node_no = len(self.node_array)
        self.get_centroid_of_elements()    
    
    def rotate_node_order(self, pre_node_order, direction, axis = 'z'):
        
        node_order = [None]*len(pre_node_order)
        for i in range(len(pre_node_order)):
            node_order[i] = pre_node_order[i][:]
        if (direction == 'left') or (direction == 'lower-left'):
            node_order = self.rotate_element(pre_node_order, rotation = [0, 0, 1])
        elif direction == 'upper' or (direction == 'upper-left'):
            node_order = self.rotate_element(pre_node_order, rotation = [0, 0, 2])
        elif direction == 'right' or (direction == 'upper-right'):
            node_order = self.rotate_element(pre_node_order, rotation = [0, 0, 3])
        return node_order

    def rotate_element(self, pre_node_order, rotation = [0, 0, 0]):
        node_order = pre_node_order[:]
        if rotation[0]:
            node_order = self.rotate_node(node_order, rotation = 90, axis = 'x')
            if rotation[0] > 1:
                node_order = self.rotate_node(node_order, rotation = 90, axis = 'x')
                if rotation[0] > 2:
                    node_order = self.rotate_node(node_order, rotation = 90, axis = 'x')
        if rotation[1]:
            node_order = self.rotate_node(node_order, rotation = 90, axis = 'y')
            if rotation[1] > 1:
                node_order = self.rotate_node(node_order, rotation = 90, axis = 'y')
                if rotation[1] > 2:
                    node_order = self.rotate_node(node_order, rotation = 90, axis = 'y')
        if rotation[2]:
            node_order = self.rotate_node(node_order, rotation = 90, axis = 'z')
            if rotation[2] > 1:
                node_order = self.rotate_node(node_order, rotation = 90, axis = 'z')
                if rotation[2] > 2:
                    node_order = self.rotate_node(node_order, rotation = 90, axis = 'z')
        return node_order
    
    def rotate_node(self, pre_node_order, rotation = 90, axis = 'z'):
        
        node_order = [None]*len(pre_node_order)
        for i in range(len(pre_node_order)):
            node_order[i] = pre_node_order[i][:]
            if rotation == 90:
                if axis == 'z':
                    node_order[i][0] = pre_node_order[i][1]
                    node_order[i][1] = 1.0 - pre_node_order[i][0]
                    node_order[i][2] = pre_node_order[i][2]
                elif axis == 'y':
                    node_order[i][0] = pre_node_order[i][2]
                    node_order[i][1] = pre_node_order[i][1]
                    node_order[i][2] = 1.0 - pre_node_order[i][0]
                elif axis == 'x':
                    node_order[i][0] = pre_node_order[i][0]
                    node_order[i][1] = 1.0 - pre_node_order[i][2]
                    node_order[i][2] = pre_node_order[i][1]

            elif rotation == 180:
                if axis == 'z':
                    node_order[i][0] = 1.0 - pre_node_order[i][0]
                    node_order[i][1] = 1.0 - pre_node_order[i][1]
                    node_order[i][2] = pre_node_order[i][2]
                elif axis == 'y':
                    node_order[i][0] = 1.0 - pre_node_order[i][0]
                    node_order[i][1] = pre_node_order[i][1]
                    node_order[i][2] = 1.0 - pre_node_order[i][2]
                elif axis == 'x':
                    node_order[i][0] = 1.0 - pre_node_order[i][0]
                    node_order[i][1] = 1.0 - pre_node_order[i][1]
                    node_order[i][2] = pre_node_order[i][2]

            elif rotation == 270:
                if axis == 'z':
                    node_order[i][0] = 1.0 - pre_node_order[i][1]
                    node_order[i][1] = pre_node_order[i][0]
                    node_order[i][2] = pre_node_order[i][2]
                elif axis == 'y':
                    node_order[i][0] = 1.0 - pre_node_order[i][2]
                    node_order[i][1] = pre_node_order[i][1]
                    node_order[i][2] = pre_node_order[i][0]
                elif axis == 'x':
                    node_order[i][0] = pre_node_order[i][0]
                    node_order[i][1] = pre_node_order[i][2]
                    node_order[i][2] = 1.0 - pre_node_order[i][1]
        return node_order
    

    
    def select_elements(self, min_x = None, max_x = None, min_y = None, 
                              max_y = None, min_z = None, max_z = None,
                              sort = False):
        ''' Method for selecting elements from the mesh that lie within a
        certain range defined by the  minimum and maximum x, y and z 
        coordinates.'''
        
        self.get_centroid_of_elements()
                                  
        if not min_x:
            min_x = np.min(self.centroid_array[:,0])
        if not max_x:
            max_x = np.max(self.centroid_array[:,0])
        if not min_y:
            min_y = np.min(self.centroid_array[:,1])
        if not max_y:
            max_y = np.max(self.centroid_array[:,1])
        if not min_z:
            min_z = np.min(self.centroid_array[:,2])
        if not max_z:
            max_z = np.max(self.centroid_array[:,2])

        if sort:
            return sorted(np.where((self.centroid_array[:,0] >= min_x) & 
                                   (self.centroid_array[:,0] <= max_x) &
                                   (self.centroid_array[:,1] >= min_y) & 
                                   (self.centroid_array[:,1] <= max_y) &
                                   (self.centroid_array[:,2] >= min_z) & 
                                   (self.centroid_array[:,2] <= max_z))[0], 
                          reverse=True)
        else:
            return np.where((self.centroid_array[:,0] >= min_x) & 
                            (self.centroid_array[:,0] <= max_x) &
                            (self.centroid_array[:,1] >= min_y) & 
                            (self.centroid_array[:,1] <= max_y) &
                            (self.centroid_array[:,2] >= min_z) & 
                            (self.centroid_array[:,2] <= max_z))[0]
    
    def delete_elements(self, min_x = None, max_x = None, min_y = None, 
                              max_y = None, min_z = None, max_z = None):
        
        selected_elements = self.select_elements(min_x, max_x, min_y, max_y, 
                                                 min_z, max_z)
        selected_elements = sorted(selected_elements, reverse=True)
        
#        print(selected_elements)
        print(len(self.element_array))
#        for element_i in selected_elements:
#            del self.element_array[element_i]
        for element_i in reversed(range(self.element_no)):
            if element_i not in selected_elements:
                del self.element_array[element_i]
        self.element_no = len(self.element_array)
        
        # combine all the nodes in the element list
        selected_nodes = []
        for element_i in range(self.element_no):
            selected_nodes += self.element_array[element_i][3:]
        
        # delete all the nodes that are not in the element list
        selected_nodes = set(selected_nodes)
        selected_nodes = sorted(selected_nodes, reverse=True)
        for node_i in reversed(range(self.node_no)):
            if node_i not in selected_nodes:
                del self.node_array[node_i]
        self.node_no = len(self.node_array)
                
        print(self.node_array)
        
        
    def insert_new_node(self, node_pos):
        ''' Method for determining wether a node does already exist, insert the
        node if it does not and return the index of the node.'''
        if tuple(node_pos[:]) in self.node_array.inv:
            return self.node_array.inv[tuple(node_pos[:])]
        else:
            node_no = len(self.node_array)
            self.node_array[node_no] = tuple(node_pos[:])
            return self.node_array.inv[tuple(node_pos[:])]
        
            		
    def copy_file(self, msh_root, msh_name):
        
        '''
        move msh file from original directory to target directory.
        '''

        src_file= os.path.join(self.msh_root, self.msh_name)
        #os.chmod(src_file, 755)
        dst_dir = self.task_root
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy2 (src_file, dst_dir)
        dst_file = os.path.join(dst_dir, self.msh_name)
        new_dst_file_name=os.path.join(dst_dir, self.task_id + '.msh')
        if not os.path.isfile(new_dst_file_name):
            os.rename(dst_file, new_dst_file_name)


    def gen_f_str(self):
        
        f_out = ''
                  
        f_out += '#FEM_MSH' + self.eol
        f_out += self.sid + '$PCS_TYPE' + self.eol 
        f_out += self.did + 'NO_PCS' + self.eol
        f_out += self.sid + '$NODES' + self.eol
        f_out += self.did + str(int(self.node_no)) + self.eol
        for node_i in range(self.node_no):
            f_out += str(int(node_i))
            for pos_i in range(3):
                f_out += ' ' + str((self.node_array[node_i][pos_i]))            
            f_out += self.eol                
        f_out += self.sid + '$ELEMENTS' + self.eol 
        f_out += self.did + str(int(self.element_no)) + self.eol
        for element_i in range(self.element_no):
            f_out += str(int(element_i)) 
            f_out += ' ' + str(int(self.element_array[element_i][1]))
            f_out += ' ' + self.element_array[element_i][2]
            for pos_i in range(3, len(self.element_array[element_i])):
                f_out += ' ' + str(int(self.element_array[element_i][pos_i]))
            f_out += self.eol            
            
        f_out += '#STOP'
            
        self.f_str = f_out    
        
    def get_element_node_pos(self, element_nodes):
        
        element_node_pos = []
        for node_i in element_nodes:
            element_node_pos.append(self.node_array[node_i])
        return element_node_pos

    def expand_node_id(self, id_list):
        
        for i in range(len(id_list)):
            id_list[i] = list(self.node_array[id_list[i]])
            
#        x_max = np.max([num[0] for num in id_list])
#        x_min = np.min([num[0] for num in id_list])
#        y_max = np.max([num[1] for num in id_list])
#        y_min = np.min([num[1] for num in id_list])
#        z_max = np.max([num[2] for num in id_list])
#        z_min = np.min([num[2] for num in id_list])
        
#        id_symb_list = [None]*len(id_list)
#        for i in range(len(id_list)):
#            tmp = [None]*3
#            if id_list[i][0] == x_max:
#                tmp[0] = 'max'
#            else:
#                tmp[0] = 'min'
#            if id_list[i][1] == y_max:
#                tmp[1] = 'max'
#            else:
#                tmp[1] = 'min'
#            if id_list[i][2] == z_max:
#                tmp[2] = 'max'
#            else:
#                tmp[2] = 'min'
#            id_symb_list[i] = tmp       
#        print(id_symb_list)
        
        return id_list
        

#    def select_element(self):
#        
#        print(np.where(4409816 < self.centroid_array[:,0] < 4409817))
#        print(set(self.centroid_array[:,0]))
