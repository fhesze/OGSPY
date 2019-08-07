
from ogspy.base import OGS_File

class PCS(OGS_File):
    
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
        
        self.f_type = '.pcs'
        
        self.pcs_type = []
        self.num_type = []
        self.prim_variable = []
        self.block_no = 0
        
    def add_block(self, pcs_type = 'GROUNDWATER_FLOW', num_type = '', 
                  prim_variable = ''):
        
        self.pcs_type.append(str(pcs_type))
        self.num_type.append(str(num_type))
        self.prim_variable.append(str(prim_variable))
        
        self.block_no += 1
        
    def gen_f_str(self):
        
        f_out = ''
        
        for block_i in range (0, self.block_no):
            
            f_out += '#PROCESS' + self.eol
            f_out += self.sid + '$PCS_TYPE' + self.eol 
            f_out += self.did + self.pcs_type[block_i] + self.eol
            if self.num_type[block_i]:
                f_out += self.sid + '$NUM_TYPE' + self.eol
                f_out += self.did + self.num_type[block_i] + self.eol
            if self.prim_variable[block_i]:
                f_out += self.sid + '$PRIMARY_VARIABLE' +self. eol 
                f_out += self.did + self.prim_variable[block_i] + self.eol
        
        f_out = f_out + '#STOP'
        self.f_str = f_out
