
from pylab import *

import os

class OGS_File(object):
    
    """
    OGS Base class from which the other file classes are derived.

    History
    -------
    Written,  FH, Jul 2015    
    
    """
	
    def __init__(self, task_root, task_id, dim_no = 2):
        
        '''
        Input
        ----------
        
        task_root(string): -path to dir of this task
        task_id(string):   -name of task
        
        '''
        
        self.task_root = task_root
        self.task_id = task_id
        self.dim_no = dim_no
        self.f_type = ''
        self.f_str = ''
        
        self.block_no = 0
        
        if (os.name == 'posix'):
            self.eol = '\n'
#            self.eol = '\r\n'
        elif (os.name == 'nt'):
            self.eol = '\r\n'
        self.sid = ' '
        self.did = '  '
        
            
    def write_file(self):
        
        self.gen_f_str()
        
        f_path = os.path.join(self.task_root,self.task_id + self.f_type)
        with open(f_path,'w') as f_id:
            f_id.write(self.f_str)                 
 	