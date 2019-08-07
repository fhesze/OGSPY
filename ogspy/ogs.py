
import subprocess
import os
#from pylab import *
#import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.collections import PolyCollection
#import matplotlib as mpl

from ogspy import *

class OGS(object):
    
    """
    Class for ogs.

    History
    -------
    Written,  FH, Jul 2015   
    """
	
    def __init__(self, task_root, task_id, dim_no = 2):
        ''' Input
        ----------
		
        task_root(string):  -path of dir of this task
        task_id(string)	-name of task
        '''
        
        self.task_root = task_root
        self.task_id = task_id
        self.dim_no = dim_no
        self.cfg_list = []
        
        self.bc = BC(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.bc)
        self.ic = IC(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.ic)
        self.gli = GLI(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.gli)
        self.mcp = MCP(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.mcp)
        self.mfp = MFP(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.mfp)
        self.mmp = MMP(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.mmp)
        self.mpd = MPD(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.mpd)
        self.msh = MSH(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.msh)
        self.msp = MSP(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.msp)
        self.num = NUM(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.num)
        self.out = OUT(task_root = task_root, task_id = task_id, dim_no = dim_no) 
        self.cfg_list.append(self.out)
        self.pcs = PCS(task_root = task_root, task_id = task_id, dim_no = dim_no) 
        self.cfg_list.append(self.pcs)
        self.st = ST(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.st)
        self.tim = TIM(task_root = task_root, task_id = task_id, dim_no = dim_no)
        self.cfg_list.append(self.tim)


    def write_input(self):
        ''' 
        method to call all write_file() methods that have been aquired data 
        during run time
        '''
               
        for cfg_elem in self.cfg_list:
            if cfg_elem.block_no:
                cfg_elem.write_file()


    def run_model (self, ogs_root = ''):
        '''
        Definition
        ----------
        def ogs_run ( ogs_root ):
	
        Optional input
        ----------
        ogs_root(string) -root of ogs executable file, default value equals to 
        None.
        '''
    
        if not ogs_root:
            if os.name == 'posix':
                ogs_root = os.environ['HOME']+'/Source/lib/ogspy/bin/posix/ogs'
            elif os.name == 'nt':
                ogs_root = os.environ['HOME']+'/Documents/ogs.exe'

        script_path = self.task_root + self.task_id
        cmd = ogs_root + ' ' + script_path
        subproc = subprocess.Popen(cmd, shell = True)
        subproc.wait()
        
        
#    def import_input(self):
#        
#        with open( self.task_root + self.task_id + '.mpd' ) as f_id:
#            lines = f_id.readlines()
#            f_id.close()
#            
#        del lines[:8]
#        line_no = len(lines)
#        self.srf = np.zeros(( line_no ))
#        for line_i in range(0, line_no):
#            line = lines[line_i]
#            self.srf[line_i] = line.split()[1]
        
        
    def import_results(self, nod_values = '', geo_type = '', geo_name = '',
                       dat_type = '', tim_type = ''):
                 
        self.nod_values = nod_values
        self.geo_type = geo_type
        self.geo_name = geo_name
        self.dat_type = dat_type
        self.tim_type = dat_type
        
        if self.geo_type == 'POINT':
            self.import_point( )
        elif  self.geo_type == 'DOMAIN':
            if self.dat_type == 'TECPLOT':
                self.import_domain_tec( )
            elif self.dat_type == 'VTK':
                self.import_domain_vtk( )
            
        
    def import_point (self):
        
        f_path = self.task_root + self.task_id + '_time_' + self.geo_name
        
        if self.dat_type == 'TECPLOT':
            f_path += '.tec'
        elif self.dat_type == 'VTK':
            f_path += '.vtk'

        with open(f_path) as f_id:
            lines = f_id.readlines()
            f_id.close()
    
        line_no = len(lines)
        self.t = np.zeros((line_no - 3))
        self.btc = np.zeros((line_no - 3))
            
        for line_i in range(3,line_no):
            line = lines[line_i]
            line = line.split()
            self.t[line_i - 3] = line[0]
            self.btc[line_i - 3] = line[1]
            
                
    def import_domain_tec (self):
        
        f_path = self.task_root + self.task_id + '_domain_quad.tec'

        with open(f_path) as f_id:
            lines = f_id.readlines()
            f_id.close()
        
        t_no = int(self.tim.time_steps[0]) + 1
        node_no = self.msh.node_no
        line_per_time_no = self.msh.node_no + self.msh.element_no + 3
        self.out.flow = np.zeros(( node_no, t_no))
        for t_i in range(0, t_no):
            for node_i in range(0, node_no):
                line_i = t_i*line_per_time_no + 3 + node_i
                line = lines[line_i]
                line = line.split()
                self.out.flow[node_i,t_i] = float(line[3])
#        self.out.node = np.zeros(( self.msh.node_no ))
#        line_s = self.msh.node_no + self.msh.element_no + 6
#        for line_i in range(line_s, line_s + self.msh.node_no):
#            line = lines[line_i]
#            line = line.split()
#            self.out.node[line_i - line_s] = line[3]
           
#        print(self.msh.node_no)
#        print(self.msh.element_no)
#        print((self.msh.node_no + self.msh.element_no + 3))
#        print(int(self.tim.time_steps[0]))
#        print(len(lines))
 
    def plot_mesh(self):
           
#        plt.contour( node_mesh )
        
        x = np.arange(1, 102, 1)
        y = np.arange(1, 52, 1)
        X, Y = np.meshgrid(x, y)
        Z = self.out.node.reshape(X.shape)
        
        fig = plt.figure()
        
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        
#        ax = fig.gca(projection='3d')
#        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
#                               linewidth=0, antialiased=False)
#        ax.set_zlim(-1.01, 1.01)

#        ax.zaxis.set_major_locator(LinearLocator(10))
#        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

#        fig.colorbar(surf, shrink=0.5, aspect=5)
#        plt.title('Original Code')        
        
        
        
             
        plt.show( )
        
 
    def plot(self):
                
        plt.plot(self.t, self.btc)
        plt.xlabel('t')
        plt.ylabel('c')
        plt.show( )
