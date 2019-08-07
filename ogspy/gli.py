
from ogspy.base import OGS_File
from pylab import *

class GLI(OGS_File):
    
    """
    Class for the ogs gli file.

    History
    -------
    Written,  FH, Jul 2015   
    
    """
	
    def __init__(self, **OGS_Config):
        '''
        Input
        ----------
        
        OGS_Config dictonary         
		
        '''
        
        OGS_File.__init__(self, **OGS_Config)
        
        self.f_type = '.gli'
        
        self.p_name = []
        self.p_pos_x = []
        self.p_pos_y = []
        self.p_pos_z = []
        
        self.l_name = []
        self.l_pos_start = [] 
        self.l_pos_no = []   
        self.l_type = [] 
        
        self.s_name = []
        self.s_polylines = []
        self.s_type = []
        
        self.point_no = 0
        self.line_no = 0
        self.surface_no = 0
    
    def add_boundary(self, msh, l_name, z_no=None):

        line_point_no = 4
        
        if z_no == None:            
            
            l_pos_array = np.zeros((line_point_no, 3))
            l_pos_array[0,0] = np.min(msh.node_array[:,1])
            l_pos_array[0,1] = np.min(msh.node_array[:,2])
            l_pos_array[0,2] = np.min(msh.node_array[:,3])
            l_pos_array[1,0] = np.min(msh.node_array[:,1])
            l_pos_array[1,1] = np.max(msh.node_array[:,2])
            l_pos_array[1,2] = np.min(msh.node_array[:,3])
            l_pos_array[2,0] = np.max(msh.node_array[:,1])
            l_pos_array[2,1] = np.max(msh.node_array[:,2])
            l_pos_array[2,2] = np.min(msh.node_array[:,3])
            l_pos_array[3,0] = np.max(msh.node_array[:,1])
            l_pos_array[3,1] = np.min(msh.node_array[:,2])
            l_pos_array[3,2] = np.min(msh.node_array[:,3])
                    
            self.add_line(l_name, l_pos_array, l_type = 'closed')

        else:

            l_pos_array = np.zeros((line_point_no, 3))
            l_pos_array[0,0] = np.min(msh.node_array[:,1])
            l_pos_array[0,1] = np.min(msh.node_array[:,2])
            l_pos_array[0,2] = msh.node_array[z_no,3]
            l_pos_array[1,0] = np.min(msh.node_array[:,1])
            l_pos_array[1,1] = np.max(msh.node_array[:,2])
            l_pos_array[1,2] = msh.node_array[z_no,3]
            l_pos_array[2,0] = np.max(msh.node_array[:,1])
            l_pos_array[2,1] = np.max(msh.node_array[:,2])
            l_pos_array[2,2] = msh.node_array[z_no,3]
            l_pos_array[3,0] = np.max(msh.node_array[:,1])
            l_pos_array[3,1] = np.min(msh.node_array[:,2])
            l_pos_array[3,2] = msh.node_array[z_no,3]

            self.add_line(l_name+str(z_no), l_pos_array, l_type = 'closed')
           
                             
    def add_point(self, p_name = '', p_pos_array = ''):
        
        self.p_pos_x.append(str(p_pos_array[0]))
        self.p_pos_y.append(str(p_pos_array[1]))
        self.p_pos_z.append(str(p_pos_array[2]))
        self.p_name.append(str(p_name))
        
        self.point_no += 1            
        
    def add_line(self, l_name = '', l_pos_array = '', l_type = 'open'):
        
        l_pos_no = len(l_pos_array[:,0])
        l_pos_start = self.point_no
        
        for l_pos_i in range(0, l_pos_no):          
            self.add_point(p_name = '', p_pos_array = l_pos_array[l_pos_i,:])
        
        self.l_name.append(str(l_name))
        self.l_pos_start.append(str(l_pos_start))
        self.l_pos_no.append(str(l_pos_no))
        self.l_type.append(str(l_type))
        
        self.line_no += 1        
        
    def add_surface(self, s_name = '', s_polylines = '', s_type = ''):
        
        self.s_name.append(str(s_name))
        self.s_polylines.append(str(s_polylines))
        self.s_type.append(str(s_type))
        
        self.surface_no += 1
        
    def gen_f_str(self):
        
        f_out = ''
        
        f_out += '#POINTS' + self.eol
        for point_i in range (0, self.point_no):
            f_out += str(point_i)
            f_out += ' ' + str(self.p_pos_x[point_i])
            f_out += ' ' + str(self.p_pos_y[point_i])
            f_out += ' ' + str(self.p_pos_z[point_i])
            if self.p_name[point_i]:
                f_out += ' ' + '$NAME'
                f_out += ' ' + str(self.p_name[point_i])
            f_out += self.eol
        
        for line_i in range (0, self.line_no):
            f_out += '#POLYLINE' + self.eol       
            f_out += self.sid + '$NAME' + self.eol
            f_out += self.did + str(self.l_name[line_i]) + self.eol
            f_out += self.sid + '$POINTS' + self.eol
            for i in range(0, int(self.l_pos_no[line_i])):
                tmp = str(i + int(self.l_pos_start[line_i]))
                f_out += self.did + tmp + self.eol
            if self.l_type[line_i] == 'closed':
                f_out += self.did + str(self.l_pos_start[line_i]) + self.eol
        
        for surface_i in range (0, self.surface_no):
            f_out += '#SURFACE' + self.eol
            f_out += self.sid + '$NAME' + self.eol 
            f_out += self.did + self.s_name[surface_i] + self.eol
            f_out += self.sid + '$POLYLINES' + self.eol
            f_out += self.did + self.s_polylines[surface_i] + self.eol
            f_out += self.sid + '$TYPE' + self.eol 
            f_out += self.did + self.s_type[surface_i] + self.eol
            
        f_out = f_out + '#STOP'
        
        self.f_str = f_out
