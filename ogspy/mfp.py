
from ogspy.base import OGS_File

class MFP(OGS_File):
    
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
        self.f_type = '.mfp'

        self.fluid_type = []
        self.pcs_type = []
        self.density_flag = []
        self.density = []
        self.viscosity = []
        self.viscosity_flag = []
    
    def add_block(self, fluid_type = 'LIQUID', pcs_type = '',
                  density_flag = '1', density = '999.7026',
                  viscosity_flag = '1', viscosity = '1.308E-03'):
        
        self.fluid_type.append(str(fluid_type))
        self.pcs_type.append(str(pcs_type))
        self.density.append(str(density))
        self.density_flag.append(str(density_flag))
        self.viscosity.append(str(viscosity))
        self.viscosity_flag.append(str(viscosity_flag))
        
        self.block_no += 1
        
    def gen_f_str(self):

        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#FLUID_PROPERTIES' + self.eol
            f_out += self.sid + '$FLUID_TYPE' + self.eol 
            f_out += self.did + self.fluid_type[block_i] + self.eol
            if self.pcs_type[block_i]:
                f_out += self.sid + '$PCS_TYPE' + self.eol
                f_out += self.did + self.pcs_type[block_i] + self.eol
            f_out += self.sid + '$DENSITY' + self.eol
            f_out += self.did + self.density_flag[block_i] + ' ' 
            f_out += self.density[block_i] + self.eol 
            f_out += self.sid + '$VISCOSITY' + self.eol 
            f_out += self.did + self.viscosity_flag[block_i] + ' '
            f_out += self.viscosity[block_i] + self.eol
        
        f_out = f_out + '#STOP'
        
        self.f_str = f_out
