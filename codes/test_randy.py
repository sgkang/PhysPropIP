"""ZarcFit2015-10-14a.py"""
 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
 
 
 
def CPEfun(Rx, Qx, px, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = 1./(1./Rx + Qx*(np.pi*2*freq*1j)**px)
    return out
 
def CPEfunElec(Rx, Qx, pex, pix, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = 1./(1./Rx + (1j)**pix*Qx*(np.pi*2*freq)**pex)
    return out
 
def CPEfunSeries(Rx, Qx, px, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = Rx + 1./(Qx*(np.pi*2*freq*1j)**px)
    return out
 
def CalculateImpedance(frequency, R0, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei):
    Zh = CPEfunSeries(Rh, Qh, Ph, frequency)
    Zl = CPEfunSeries(Rl, Ql, Pl, frequency)
    Ze = CPEfunElec(Re, Qe, Pef, Pei, frequency)
    Z = 1./(1./R0+1./Zh+1./Zl)+Ze
    return Z
 
if __name__ == '__main__':
    import pandas as pd
    pathforPK = "./data/nt01213a.z"
    pathfordata = "./data/Kimberlite-2015-07-17.xls"
    temp = np.loadtxt(pathforPK, skiprows=11, delimiter=",")
    data = pd.read_excel(pathfordata)
    data_active = data.loc[np.logical_and((data['Facies'] == 'XVK')|(data['Facies'] == 'PK')|(data['Facies'] == 'HK')|(data['Facies'] == 'VK'), data.notnull()['Rinf']==True)][["Facies", "0LabID (PCG)", "Peregrine ID", "(Latitude)", "(Longitude)", "Depth (m)","Mag Susc [SI]","Resistivity [Ohm.m]","Geometric Factor [m]","Sat Geometric Dens [g/cc]","Chargeability [ms]","Rinf","Ro","Rh","Qh","Ph", "Fh","pRh", "pQh","Rm","Qm","Pm", "pRm", "pQm","Rl","Ql","Pl", "Fl", "pRl", "pQl","Re","Qe","Pe-f","Pe-i"]]
    Ro = data_active[data['0LabID (PCG)'] == 'NT01213']['Ro'].values[0]
    Rinf = data_active[data['0LabID (PCG)'] == 'NT01213']['Rinf'].values[0]
    Rh = data_active[data['0LabID (PCG)'] == 'NT01213']['Rh'].values[0]
    Qh = data_active[data['0LabID (PCG)'] == 'NT01213']['Qh'].values[0]
    pRh = data_active[data['0LabID (PCG)'] == 'NT01213']['pRh'].values[0]
    pQh = data_active[data['0LabID (PCG)'] == 'NT01213']['pQh'].values[0]
    Ph = data_active[data['0LabID (PCG)'] == 'NT01213']['Ph'].values[0]
    Fh = data_active[data['0LabID (PCG)'] == 'NT01213']['Fh'].values[0]
    Rl = data_active[data['0LabID (PCG)'] == 'NT01213']['Rl'].values[0]
    Ql = data_active[data['0LabID (PCG)'] == 'NT01213']['Ql'].values[0]
    pRl = data_active[data['0LabID (PCG)'] == 'NT01213']['pRl'].values[0]
    pQl = data_active[data['0LabID (PCG)'] == 'NT01213']['pQl'].values[0]
    Pl = data_active[data['0LabID (PCG)'] == 'NT01213']['Pl'].values[0]   
    Re = data_active[data['0LabID (PCG)'] == 'NT01213']['Re'].values[0]
    Qe = data_active[data['0LabID (PCG)'] == 'NT01213']['Qe'].values[0]
    Pef = data_active[data['0LabID (PCG)'] == 'NT01213']['Pe-f'].values[0]
    Pei = data_active[data['0LabID (PCG)'] == 'NT01213']['Pe-i'].values[0]   
    frequency = temp[:,0].copy()
    ObsReal = temp[:,4].copy()
    ObsImag = temp[:,5].copy()
    ObsZ = ObsReal + 1j*ObsImag
    ObsMag = abs(ObsZ)
    ObsPh = np.angle(ObsZ, deg=True)
    
    Ro0 = Ro
    Ph0 = Ph  
    
    Z = CalculateImpedance(frequency, Ro, pRh, pQh, Ph, pRl, pQl, Pl, Re, Qe, Pef, Pei)
   
    fig = plt.figure(figsize = (15, 8))
    axReal = plt.subplot(333)
    axImag = plt.subplot(336)
    axMag = plt.subplot(332)
    axPh = plt.subplot(335)
    axCole = plt.subplot(331)
 
    axReal.loglog(frequency, ObsReal, 'k.')
    axReal.loglog(frequency, Z.real, 'k-')
    axReal.grid(True)
    axReal.invert_xaxis()
    axReal.set_xlabel("Frequency [Hz]")
    axReal.set_ylabel("Real impedance [Ohm]")
#    axReal.legend(("Observed", "Predicted"))
 
    axImag.loglog(frequency, abs(ObsImag), 'r.')
    axImag.loglog(frequency, abs(Z.imag), 'r-')
    axImag.grid(True)
    axImag.invert_xaxis()
    axImag.set_xlabel("Frequency [Hz]")
    axImag.set_ylabel("Imaginary impedance [Ohm]")
#    axImag.legend(("Observed", "Predicted"))
   
    axMag.loglog(frequency, ObsMag, 'k.')
    axMag.loglog(frequency, abs(Z), 'k-')
    axMag.grid(True)
    axMag.invert_xaxis()
    axMag.set_xlabel("Frequency [Hz]")
    axMag.set_ylabel("Total impedance [Ohm]")
#    axMag.legend(("Observed", "Predicted"))
 
    axPh.loglog(frequency, abs(ObsPh), 'k.')
    axPh.loglog(frequency, abs(np.angle(Z, deg=True)) , 'k-')
    axPh.grid(True)
    axPh.invert_xaxis()
    axPh.set_xlabel("Frequency [Hz]")
    axPh.set_ylabel("Phase")
#    axPh.legend(("Observed", "Predicted"))
 
    axCole.plot(ObsReal, ObsImag, 'k.')
    axCole.plot(Z.real, Z.imag, 'k-')
    axCole.grid(True)
    axCole.invert_yaxis()
    axCole.set_xlabel("Real [Ohm]")
    axCole.set_ylabel("Imag [Ohm]")
#    axCole.legend(("Observed", "Predicted"))
 
 
    axcolor = 'lightgoldenrodyellow'
    axRo = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    axPh  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
    sRo = Slider(axRo, 'Ro', 0.1, 100000, valinit=Ro0)
    sPh = Slider(axPh, 'Ph', 0., 1., valinit=Ph0)
 
    def update(val):
        Ro = sRo.val
        Ph = sPh.val
        Z = CalculateImpedance(frequency, Ro, pRh, pQh, Ph, pRl, pQl, Pl, 
                               Re, Qe, Pef, Pei)
        axCole.plot(Z.real, Z.imag, 'k-')
        fig.canvas.draw_idle()
    sRo.on_changed(update)
    sPh.on_changed(update)
   
    plt.show()