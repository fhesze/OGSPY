import math as m
import scipy as sp 

def hThiem2D(r,Q,K,R,D=1,hR=0):
    
    """
    This function is to calculate 2D's Thiem's solution of pumping test.

    Definition:         usage: hThiem.py

    Input
    r   (1D array or list)  -   distance from the centre of the well
    Q   (scalar)            -   constant discharge of pumping well
    D   (scalar)            -   thickness of confined aquifer
    K   (scalar)            -   hydraulic conductivity
    R   (scalar)            -   referenced distance from the well
    
    Optional Input
    hR  (scalar)            -   the fixed hydraulic head at the distance R

    Output
    hThiem2D (1D array or list) -   Thiem's solution of pumping test
    """
    hThiem2D=.5*Q/m.pi/D/K*m.log(r/R)+hR
    return hThiem2D
    
def hThiem2D_Dimles(r,R):
    
    """
    This function is to calculate Thiem's solution of pumping test.

    Definition:         usage: hThiem.py

    Input
    r   (1D array or list)  -   distance from the centre of the well
    R   (scalar)            -   referenced distance from the well
    
    Output
    hThiem2D (1D array or list) -   Thiem's solution of pumping test
    """
    hThiem2D=m.log(r/R)
    return hThiem2D
#def KA()

def KCG2D(r,KG,sigma,psi,ell):
    '''
    Calculate radially dependent upscaled hydraulic conductivity.
    
    Definition
    ----------
    def KCG2D(r,KG,sigma,ell,psi):
        
    Input
    -----------
    r   (1D array or list)  - distance from the centre of the well
    KG  (scalar)            - geometric mean of hydraulic conductivity K
    sigma(scalar)           - standard deviation
    psi(scalar)             - factor of proportionality
    ell(scalar)             - correlation length of the log-normally distributed hydraulic
                                conductivity
                                
    Output
    -----------
    KCG2D (1D array or list) - radially dependent upscaled hydraulic conductivity
    '''

    KCG2D=KG*m.exp(-.5*sigma*sigma/(1+(psi*r)**2/ell/ell))
    return KCG2D

def hCG2D_Dimles(r,R,sigma,psi,ell):

    '''
    Calculate the hydraulic head for large scale pumping tests in a two-dimensional flow regime.
    
    Definition
    -----------
    def hCG2D(r,Qw,TG,R,sigma,hR=0,psi,l):
    
    Input
    ----------- 
    r   (1D array or list)  - distance from the centre of the well
    R   (scalar)            - referenced distance from the well
    sigma(scalar)           - standard deviation
    ell(scalar)             - correlation length of the log-normally distributed hydraulic                            conductivity
    psi(scalar)             - factor of proportionality
  
    Output
    ----------
    hCG2D (1D array or list) - hydraulic head
    '''

    
    zed_r=sigma*sigma/2/(1+(psi*r/ell)**2)
    zed_R=sigma*sigma/2/(1+(psi*R/ell)**2)
    
            
    hCG2D=-0.5*((sp.special.expi(zed_r)-sp.special.expi(zed_R))\
    -m.exp(.5*sigma**2)*sp.special.expi(zed_r-.5*sigma**2)+m.exp(.5*sigma**2)\
    *sp.special.expi(zed_R-.5*sigma**2))
    return hCG2D
    
    
    
#def gamma(ee):

#def Kefu(KG,sigma,ee):

#def KCG3D(r,KG,sigma,ell,ee):  
    
    ### Statistical quantities:
    #ell=
    #ee=
    
    
#   Kefu=Kefu(KG, sigma,ee)
#   xi=
#   psi=
    
#   KCG=Kefu*np.exp(xi*(1+(psi*r)/(ee**(1/3)*ell**2))**(-3/2))
    
#   hCG=0
    
#   return KCG3D

#def hCG3D(r):  
    
#   hCG=0
    
#   return hCH
