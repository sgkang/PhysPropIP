import numpy as np

def Zarcfun(Rx, Qx, px, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = 1./(1./Rx + Qx*(np.pi*2*freq*1j)**px)
    return out

def ZarcElecfun(Rx, Qx, Pei, Pef, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = 1./(1./Rx + Qx*(1j)**Pei*(np.pi*2*freq)**Pef)
    return out

def RplusCPEfun(Rx, Qx, px, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = Rx + 1./(Qx*(np.pi*2*freq*1j)**px)
    return out

def Zseries(Rinf, Rh, Qh, Ph, Rm, Qm, Pm, Rl, Ql, Pl, Re, Qe, Pei, Pef, freq):
    out = Rinf + Zarcfun(Rh, Qh, Ph, freq) + Zarcfun(Rm, Qm, Pm, freq) + Zarcfun(Rl, Ql, Pl, freq) \
               + ZarcElecfun(Re, Qe, Pei, Pef, freq)
    return out