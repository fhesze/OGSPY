
from pylab import *
from ogspy.base import OGS_File

class MPD(OGS_File):
    
    """
    Class for the ogs distributed medium property file.

    History
    -------
    Written,  FH, Jul 2015 -    
    
    """
	
    def __init__(self, **OGS_Config):
        '''
        Input
        ----------
        
        OGS_Config dictonary         
		
        '''
        
        OGS_File.__init__(self, **OGS_Config)
        
        self.f_type = '.mpd'
        
    def add_mpd(self, field):
        
        self.mpd = field
        self.element_no = len(self.mpd)
            
    def gen_f_str(self):
        
        f_out = ''
                  
        f_out += '#MEDIUM_PROPERTIES_DISTRIBUTED' + self.eol
        f_out += self.sid + '$MSH_TYPE' + self.eol 
        f_out += self.did + 'NONE' + self.eol
        f_out += self.sid + '$MMP_TYPE' + self.eol
        f_out += self.did + 'PERMEABILITY' + self.eol
        f_out += self.sid + '$DIS_TYPE' + self.eol
        f_out += self.did + 'ELEMENT' + self.eol
        f_out += self.sid + '$DATA' + self.eol        
        
        for element_i in range(0, self.element_no):
            f_out += str(element_i) + ' '
            f_out += str(self.mpd[element_i])            
            f_out += self.eol            
            
#        f_out += '#STOP'
            
        self.f_str = f_out        
 	