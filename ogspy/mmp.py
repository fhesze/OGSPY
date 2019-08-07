
from ogspy.base import OGS_File

class MMP(OGS_File):
    
    """
    Class for the ogs medium property file.

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
        
        self.f_type = '.mmp'
        
        self.geo_dim = []
        self.geo_area = []
        self.storage_flag = []
        self.storage = []
        self.per_sat_flag = []
        self.per_sat = []
        self.per_tensor = []
        self.per_dist = []
        self.porosity_flag = []
        self.porosity = []
        self.tortuosity_flag = []
        self.tortuosity = []
        self.mass_disp_flag = []
        self.mass_disp_x = []
        self.mass_disp_y = []
        self.mass_disp_z = []
        self.density_flag = []
        self.density = []
        self.block_no = 0
        
    def add_block(self, geo_dim = None, geo_area = '', 
                  storage_flag = '1', storage = '', 
                  per_sat_flag = '1', per_sat = '', 
                  per_tensor = None, per_dist = '', 
                  porosity_flag = '1', porosity = '', 
                  tortuosity_flag = '1', tortuosity = '',
                  mass_disp_flag = '1', 
                  mass_disp_x = '', mass_disp_y = '', mass_disp_z = '', 
                  density_flag = '1', density = ''):
        
        self.geo_dim.append(str(geo_dim))
        self.geo_area.append(str(geo_area))
        self.storage_flag.append(str(storage_flag))
        self.storage.append(str(storage))
        self.per_sat_flag.append(str(per_sat_flag))
        self.per_sat.append(str(per_sat))
        self.per_tensor.append(str(per_tensor))
        self.per_dist.append(str(per_dist))
        self.porosity_flag.append(str(porosity_flag))
        self.porosity.append(str(porosity))
        self.tortuosity_flag.append(str(tortuosity_flag))
        self.tortuosity.append(str(tortuosity))
        self.mass_disp_flag.append(str(mass_disp_flag))
        self.mass_disp_x.append(str(mass_disp_x))
        self.mass_disp_y.append(str(mass_disp_y))
        self.mass_disp_z.append(str(mass_disp_z))
        self.density_flag.append(str(density_flag))
        self.density.append(str(density))
        
        self.block_no += 1
        
    def gen_f_str(self):
        
        f_out = ''
        for block_i in range (0, self.block_no):
            
            f_out += '#MEDIUM_PROPERTIES' + self.eol
            
            f_out += self.sid + '$GEOMETRY_DIMENSION' + self.eol 
            f_out += self.did + self.geo_dim[block_i] + self.eol
            
            if self.geo_area[block_i]:
                f_out += self.sid + '$GEOMETRY_AREA' + self.eol
                f_out += self.did + self.geo_area[block_i] + self.eol
            
            f_out += self.sid + '$STORAGE' + self.eol
            f_out += self.did + self.storage_flag[block_i] + ' '
            f_out += self.storage[block_i] + self.eol
            
            if self.per_sat[block_i]:
                f_out += self.sid + '$PERMEABILITY_SATURATION' + self.eol 
                f_out += self.did + self.per_sat_flag[block_i] + ' '
                f_out += self.per_sat[block_i] + self.eol
            
            f_out += self.sid + '$PERMEABILITY_TENSOR' + self.eol 
            f_out += self.did + self.per_tensor[block_i] + self.eol
            
            if self.per_dist[block_i]:
                f_out += self.sid + '$PERMEABILITY_DISTRIBUTION' + self.eol 
                f_out += self.did + self.per_dist[block_i] + self.eol
            
            if self.porosity[block_i]:
                f_out += self.sid + '$POROSITY' + self.eol
                f_out += self.did + self.porosity_flag[block_i] + ' ' 
                f_out += self.porosity[block_i] + self.eol
            
            if self.tortuosity[block_i]:
                f_out += self.sid + '$TORTUOSITY' + self.eol 
                f_out += self.did + self.tortuosity_flag[block_i] + ' '
                f_out += self.tortuosity[block_i] + self.eol
            
            if self.mass_disp_x[block_i]:
                f_out += self.sid + '$MASS_DISPERSION' + self.eol
                f_out += self.did + self.mass_disp_flag[block_i]
                if self.mass_disp_x[block_i]:
                    f_out += ' ' + self.mass_disp_x[block_i]
                if self.mass_disp_y[block_i]:
                    f_out += ' ' + self.mass_disp_y[block_i]
                if self.mass_disp_z[block_i]:
                    f_out += ' ' + self.mass_disp_z[block_i]
                f_out += self.eol
            
            if self.density[block_i]:
                f_out += self.sid + '$DENSITY' + self.eol
                f_out += self.did + self.density_flag[block_i] + ' '
                f_out += self.density[block_i] + self.eol
            
        f_out = f_out + '#STOP'
            
        self.f_str = f_out
            