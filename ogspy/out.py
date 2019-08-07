
from ogspy.base import OGS_File

class OUT(OGS_File):
    
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
        
        self.f_type = '.out'
        
        self.nod_values = []
        self.geo_type = []
        self.geo_name = []
        self.dat_type = []
        self.tim_type = []
        self.block_no = 0
        
    def add_block(self, nod_values = 'HEAD', geo_type = 'DOMAIN', 
                  geo_name = None, dat_type = 'VTK', tim_type = 'STEPS 1'):
        
        self.nod_values.append(nod_values)
        self.geo_type.append(geo_type)
        self.geo_name.append(geo_name)
        self.dat_type.append(dat_type)
        self.tim_type.append(tim_type)
        
        self.block_no += 1
        
    def gen_f_str(self):

        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#OUTPUT' + self.eol
            f_out += self.sid + '$NOD_VALUES' + self.eol
            f_out += self.did + str(self.nod_values[block_i]) + self.eol
            f_out += self.sid + '$GEO_TYPE' + self.eol
            f_out += self.did + str(self.geo_type[block_i])
            if self.geo_name[block_i]:
                f_out += ' ' + str(self.geo_name[block_i])
            f_out += self.eol
            f_out += self.sid + '$DAT_TYPE' + self.eol
            f_out += self.did + str(self.dat_type[block_i]) + self.eol
            f_out += self.sid + '$TIM_TYPE' + self.eol
            f_out += self.did + str(self.tim_type[block_i]) + self.eol
        
        f_out += '#STOP'
        self.f_str = f_out
 