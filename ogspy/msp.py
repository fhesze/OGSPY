
from ogspy.base import OGS_File

class MSP(OGS_File):
    
    """
    Class for the ogs material fluid property file.

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
        self.f_type = '.msp'

        self.density_flag = []
        self.density = []
    
    def add_block(self, density_flag = '1', density = '2.00000e+003'):
        
        self.density_flag.append(str(density_flag))
        self.density.append(str(density))
        
        self.block_no += 1
        
    def gen_f_str(self):

        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#SOLID_PROPERTIES' + self.eol
            f_out += self.sid + '$DENSITY' + self.eol
            f_out += self.did + self.density_flag[block_i] + ' '
            f_out += self.density[block_i] + self.eol 
        
        f_out = f_out + '#STOP'
        
        self.f_str = f_out
            