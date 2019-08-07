
from ogspy.base import OGS_File

class TIM(OGS_File):
    """
    Class for the ogs time file.

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

        self.f_type = '.tim'
        
        self.pcs_type = []
        self.time_start = []
        self.time_end = []
        self.time_steps = []
        self.step_size = []
        self.block_no = 0
    
    def add_block(self, pcs_type = 'GROUNDWATER_FLOW', time_start = 0.0, 
                  time_end = 10, time_steps = 10, step_size = 1):
        
        self.pcs_type.append(str(pcs_type))
        self.time_start.append(str(time_start))
        self.time_end.append(str(time_end))
        self.time_steps.append(str(time_steps))
        self.step_size.append(str(step_size))
        
        self.block_no += 1
        
    def gen_f_str(self):

        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#TIME_STEPPING' + self.eol
            f_out += self.sid + '$PCS_TYPE' + self.eol 
            f_out += self.did + self.pcs_type[block_i] + self.eol 
            f_out += self.sid + '$TIME_START' + self.eol 
            f_out += self.did + self.time_start[block_i] + self.eol 
            f_out += self.sid + '$TIME_END' + self.eol 
            f_out += self.did + self.time_end[block_i] + self.eol 
            f_out += self.sid + '$TIME_STEPS' + self.eol 
            f_out += self.did + self.time_steps[block_i]
            f_out += ' ' + self.step_size[block_i] + self.eol
        
        f_out = f_out + '#STOP'
        
        self.f_str = f_out
