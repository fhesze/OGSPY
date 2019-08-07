
from ogspy.base import OGS_File

class MCP(OGS_File):
    """
    Class for the ogs component properties file.

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
        
        self.f_type = '.mcp'
        
        self.name = []
        self.mobile = []
    
    def add_block(self, name = 'TRACER', mobile = None):
        
        self.name.append(str(name))
        self.mobile.append(str(mobile))
        
        self.block_no += 1
        
    def gen_f_str(self):

        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#COMPONENT_PROPERTIES  ; comp0' + self.eol
            f_out += self.sid + '$NAME' + self.eol 
            f_out += self.did + self.name[block_i] + self.eol 
            f_out += self.sid + '$MOBIL' + self.eol 
            f_out += self.did + self.mobile[block_i] + self.eol
        
        f_out = f_out + '#STOP'
        
        self.f_str = f_out
        