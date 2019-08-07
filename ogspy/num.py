
from ogspy.base import OGS_File

class NUM(OGS_File):
    
    '''
    Class for the ogs numerics file.

    History
    -------
    Written,  JM, Jul 2015
    Modified, FH, Jul 2015 - rewritten for geneneral purpose ogs projects    
    '''
    
    def __init__(self, **OGS_Config):
        '''
        Input
        ----------
        
        OGS_Config dictonary         
		
        '''
        
        OGS_File.__init__(self, **OGS_Config)
        
        self.f_type = '.num'

        self.pcs_type = []
        self.solver = []
        self.solver_01 = []
        self.solver_02 = []
        self.prop_type = []
        self.prop = []
    
    def add_block(self, pcs_type = None, 
                  solver = None, solver_01 = None, solver_02 = None,
                  prop_type = None, prop = None):
        
        self.pcs_type.append(str(pcs_type))
        self.solver.append(str(solver))
        self.solver_01.append(str(solver_01))
        self.solver_02.append(str(solver_02))
        self.prop_type.append(str(prop_type))
        self.prop.append(str(prop))
        
        self.block_no += 1
        
    def gen_f_str(self):

        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#NUMERICS' + self.eol
            f_out += self.sid + '$PCS_TYPE' + self.eol 
            f_out += self.did + self.pcs_type[block_i] + self.eol 
            f_out += self.sid + self.solver[block_i] + self.eol
            f_out += self.did + self.solver_01[block_i] + self.eol
            if (self.solver_02[block_i]) != (str(None)):
                f_out += self.did + self.solver_02[block_i] + self.eol
            if (self.prop_type[block_i]) != (str(None)):
                f_out += self.sid + self.prop_type[block_i] + self.eol
            if (self.prop[block_i]) != (str(None)):
                f_out += self.did + self.prop[block_i] + self.eol
        
        f_out = f_out + '#STOP'
        
        self.f_str = f_out             
