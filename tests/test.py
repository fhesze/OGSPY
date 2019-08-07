
import subprocess
import filecmp

path = '/home/fhesse/Source/lib/Pumping_Test/tutorials/transport/'

subprocess.call(['python', path + 'main.py'])

answer = filecmp.cmp(path + 'data/fm.bc', path + 'project/fm.bc') 

print(answer)
