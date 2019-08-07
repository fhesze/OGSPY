
from ogspy.base import OGS_File

class IC(OGS_File):
    
    """
    Generate all input files according to specific radial mesh.
    """
    
    def __init__(self, **OGS_Config):
        '''
        Input
        ----------
        
        OGS_Config dictonary         
		
        '''
        
        OGS_File.__init__(self, **OGS_Config)
        
        self.f_type = '.ic'
        
        self.pcs_type = []
        self.prim_variable = []
        self.geo_type = []
        self.dis_type = []
		
    def add_block(self, pcs_type = 'GROUNDWATER_FLOW', prim_variable = 'HEAD', 
                  geo_type = 'POLYLINE  WELL_0', dis_type = 'CONSTANT  -1e-01'):
        
        self.pcs_type.append(str(pcs_type))
        self.prim_variable.append(str(prim_variable))
        self.geo_type.append(str(geo_type))
        self.dis_type.append(str(dis_type))
        
        self.block_no += 1
        
    def gen_f_str(self):
        
        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#INITIAL_CONDITION' + self.eol
            f_out += self.sid + '$PCS_TYPE' + self.eol 
            f_out += self.did + self.pcs_type[block_i] + self.eol
            f_out += self.sid + '$PRIMARY_VARIABLE' + self.eol
            f_out += self.did + self.prim_variable[block_i] + self.eol
            f_out += self.sid + '$GEO_TYPE' + self.eol 
            f_out += self.did + self.geo_type[block_i] + self.eol
            f_out += self.sid + '$DIS_TYPE' + self.eol 
            f_out += self.did + self.dis_type[block_i] + self.eol
            
        f_out = f_out + '#STOP'
            
        self.f_str = f_out
