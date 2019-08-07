
import subprocess
import os
from pylab import *

def plot_btc (task_root, task_id,  f_path = None):
    
    '''
    Definition
    ----------
    def ogs_run ( ogs_root, task_root, task_ID):
        
    Input
    ----------
    task_root(string) -root of task_id
    task_id(string)   -name of task without extension
    
    Optional input
    ----------
    f_path(string)  path to the file
    '''

    with open(f_path) as f_id:
        lines = f_id.readlines()
    f_id.close()
    
    line_no = len(lines)
    t = np.zeros((line_no - 3))
    u = np.zeros((line_no - 3))
    
    for line_i in range(3,line_no):
        
        line = lines[line_i]
        line = line.split()
        t[line_i - 3] = line[0]
        u[line_i - 3] = line[1]
        
    plot(t, u)
    xlabel('t')
    ylabel('c')
    show()
