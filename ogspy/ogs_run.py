
import subprocess
import os


def run (task_root, task_id,  ogs_root = None):
    
    '''
    Definition
    ----------
    def ogs_run ( ogs_root, task_root, task_ID):
	
    Input
    ----------
    task_root(string)			--root of task_ID
    task_ID(string)				--name of task without extension
    
    Optional input
    ----------
    ogs_root(string)			--root of ogs executable file, default value equals to None.
    '''
    
    if not ogs_root:
        if os.name == 'posix':
            ogs_root = os.environ['HOME'] + '/Source/lib/Pumping_Test/'
        elif os.name == 'nt':
            ogs_root = 'C:/Users/miao/Documents/ogs.exe'

    script_path = os.path.join(task_root, task_id)
    cmd = ogs_root + ' ' + script_path
    subproc = subprocess.Popen(cmd, shell = True)
    subproc.wait()
	
#	print('OGS calculation completed!\nTask root: %s, task ID: %s.'%(task_root, task_id))
