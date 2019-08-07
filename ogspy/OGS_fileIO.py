# -*- coding: utf-8 -*-
import math as m
import Pumpingtest_solution

"""
This is a python file for reading specific data from .tec files

positional arguments:
    --filename: the name of tec file
    --time: which time you want to read data from
the return value:
    --xlists: the x values
    --ylists: the y values   
"""
#----------------------------------------------------------------------------
def readtec(filename,time):
    
    '''
    Read the solution at specific time step of .tec files generated from OGS computing.
    
    Definition
    ----------
    def readtec(filename,time):
        
    Input
    ----------
    filename  (string)          -filename of txt files generated from OGS computing.
    time        (scalar)        -specific time
    '''
    
    infile=open(filename,'r')
    for line in infile:
        if 'ZONE' in line:
            Ti=float(line[14:-2]) #extract the number from string
            if Ti==time:
               #next(infile) #do not need to skip this line!
               xlists=[]
               ylists=[]
               for line in infile:
                   if 'TITLE' in line:
                       break
                   else:
                       words=line.split()
                       xlist=float(words[0]) #words[0] means the first word
                       ylist=float(words[1]) #words[1] means the second word
                       xlists.append(xlist)
                       ylists.append(ylist)   
    infile.close()
    return xlists,ylists
    
def readtecdim(filename,time,KG,Q):
    
    '''
    Calculate dimentionless solution at specific time step of .tec files generated from OGS computing.
    
    Definition
    ----------
    def readtec(filename,time):
        
    Input
    ----------
    filename  (string)          -filename of txt files generated from OGS computing.
    time        (scalar)        -specific time
    '''
    
    infile=open(filename,'r')
    for line in infile:
        if 'ZONE' in line:
            Ti=float(line[14:-2]) #extract the number from string
            if Ti==time:
               #next(infile) #do not need to skip this line!
               xlists=[]
               ylists=[]
               for line in infile:
                   if 'TITLE' in line:
                       break
                   else:
                       words=line.split()
                       xlist=float(words[0]) #words[0] means the first word
                       ylist=float(words[1])*2*m.pi*KG/Q #words[1] means the second word
                       xlists.append(xlist)
                       ylists.append(ylist)   
    infile.close()
    return xlists,ylists
    
def KCG_assignment(filename,KG,sigma,psi,ell):
    '''
    This is a python file to assign the heterogeneous permeability field obeying
    Coarse Graining method to every element of meshes.
    
    Definition
    ----------
    def KCG_assignment(filename):
    
    Input
    -----------
    filename (string)        -filename of .msh file
    
    KG  (scalar)            - geometric mean of hydraulic conductivity K
    
    sigma(scalar)           - standard deviation
    
    ell(scalar)             - correlation length of the log-normally distributed hydraulic
                                conductivity
    psi(scalar)             - factor of proportionality 
    
    Output
    ----------
    Store the KCG field with assignment to every element into a .txt file    
    '''
    
    
    infile=open(filename,'r')
    #lines=infile.readlines() #This line is wrong! the bug!
     
    elelists=[]  # number of elements
    nod1lists=[] # corresponding node number of node1; length: element number
    nod2lists=[] # corresponding node number of node2; length: element number
    nod3lists=[]
    nod4lists=[]  # corresponding node number of node4; length: element number
   
    for line in infile:
        if 'ELEMENTS' in line:
            next(infile) #skip the next line     
                       
            for line in infile:
                if 'STOP' in line:
                    break
                else:
                    words=line.split()
                    elelist=int(words[0])
                    nod1list=int(words[3])
                    nod2list=int(words[4])
                    nod3list=int(words[5])
                    nod4list=int(words[6])
                    elelists.append(elelist)
                    nod1lists.append(nod1list)
                    nod2lists.append(nod2list)
                    nod3lists.append(nod3list)
                    nod4lists.append(nod4list)
    infile.close()
     
    infile=open(filename,'r')
    lines=infile.readlines() # load all lines into a list of strings
    nodnum=int(lines[4]) # extract the number of node amounts from line4
    nodcorlists=lines[5:5+nodnum] #load all node number and coordinate into a list
    
    nod1corlists=[] # all information(number and coordinate) of node1; length: element number
    nod2corlists=[]
    nod3corlists=[]
    nod4corlists=[]
    nod1xlists=[] # x value of node1 of every element
    nod1ylists=[]    
    nod2xlists=[]
    nod2ylists=[]
    nod3xlists=[]
    nod3ylists=[]
    nod4xlists=[]
    nod4ylists=[]
    elexlists=[] # x value of the center of element 
    eleylists=[] # y value of the center of element
    radlists=[] # distance from element's centre to well
    KCGlists=[]
    eleraddic={} # a dictionary of all radlist ()
    eleKCGdic={} # a dictionary of all KCGlist ()
    for nod1list in nod1lists:
        nod1corlist=nodcorlists[nod1list] # extract certain coordinate with index of nod1list
        cors=nod1corlist.split()
        nod1xlist=float(cors[1])
        nod1ylist=float(cors[2])
        nod1corlists.append(nod1corlist)
        nod1xlists.append(nod1xlist)
        nod1ylists.append(nod1ylist)
    for nod2list in nod2lists:
        nod2corlist=nodcorlists[nod2list]
        cors=nod2corlist.split()
        nod2xlist=float(cors[1])
        nod2ylist=float(cors[2])
        nod2corlists.append(nod2corlist)
        nod2xlists.append(nod2xlist)
        nod2ylists.append(nod2ylist)
    for nod3list in nod3lists:
        nod3corlist=nodcorlists[nod3list]
        cors=nod3corlist.split()
        nod3xlist=float(cors[1])
        nod3ylist=float(cors[2])
        nod3corlists.append(nod3corlist)
        nod3xlists.append(nod3xlist)
        nod3ylists.append(nod3ylist)
    for nod4list in nod4lists:
        nod4corlist=nodcorlists[nod4list]
        cors=nod4corlist.split()
        nod4xlist=float(cors[1])
        nod4ylist=float(cors[2])
        nod4corlists.append(nod4corlist)
        nod4xlists.append(nod4xlist)
        nod4ylists.append(nod4ylist)
    for elelist in elelists:
        elexlist=.25*(nod1xlists[elelist]+nod2xlists[elelist]+nod3xlists[elelist]\
                    +nod4xlists[elelist])
        eleylist=.25*(nod1ylists[elelist]+nod2ylists[elelist]+nod3ylists[elelist]\
                    +nod4ylists[elelist])
        radlist=m.sqrt(elexlist**2+eleylist**2)
        
        KCGlist=Pumpingtest_solution.KCG2D(radlist,KG,sigma,psi,ell)

        '''
        to add elements into dictionary"eleraddic"
        '''
        eleraddic[elelist]=radlist
        eleKCGdic[elelist]=KCGlist
        elexlists.append(elexlist)
        eleylists.append(eleylist)
        radlists.append(radlist)
        KCGlists.append(KCGlist)
        #eleradlists.append(eleradlist)

          
    #write the result in eleKCGdic into a .txt file
    outfile_path=filename.replace('msh','txt') 
    outfile_path=outfile_path.replace('Pumping_Test_G','KCGfile_G')  
	
    with open(outfile_path,'w') as outfile:
        '''        
        for en, rn in eleraddic.items(): #extract every keys and values in the dictionary       
            outfile.write(str(en)+'   '+str(rn))
            outfile.write('\n')
        '''
        outfile.write('#MEDIUM_PROPERTIES_DISTRIBUTED\n'+'$MSH_TYPE\n'+
                     'GROUNDWATER_FLOW\n'+
                    '$MSH_TYPE\n'+
                      'GROUNDWATER_FLOW\n'+
                    '$MMP_TYPE\n'+
                     'PERMEABILITY\n'+
                    '$DIS_TYPE\n'+
                     'ELEMENT\n'+
                    '$DATA\n')
        for en, Kn in eleKCGdic.items():
            outfile.write(str(en)+'   '+str(Kn))
            outfile.write('\n')
    
     #outfile.write(eleraddic)
        
    #return elexlists, eleylists, eleraddic #nod3xlists,nod3ylists 
    #nod1lists, nodcorlists, nod1xlists, words#lines nod1lists,nod2lists,nod3lists,nod4lists
    #return elexlists, eleylists, nod1xlists, nod1ylists,nod2xlists,nod2ylists,nod3xlists,\
    #        nod3ylists,nod4xlists,nod4ylists

    '''
    nod1lists,nod2lists,nod3lists,nod4lists,\
            nod1xlists, nod1ylists,nod2xlists,nod2ylists,nod3xlists,\
            nod3ylists,nod4xlists,nod4ylists\
            =OGS_fileIO.readKCG('C:\Users\miao\Documents\Pumping_Test\Simulation\Test\Test.msh')
    '''
