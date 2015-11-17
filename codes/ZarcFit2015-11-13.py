import numpy as np
import sys
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
Ui_MainWindow, QMainWindow = loadUiType('ZarcFit2015-11-13.ui')  

def Zarc(Rx, Qx, Px, freq):
    Zx = np.zeros_like(freq, dtype=np.complex128)
    Zx = 1./(1./Rx + Qx*(np.pi*2*freq*1j)**Px)
    return Zx

def ZarcElectrode(Re, Qe, Pef, Pei, freq):
    Ze = np.zeros_like(freq, dtype=np.complex128)
    Ze = 1./(1./Re + Qe*(np.pi*2*freq)**Pef*(1j)**Pei)
    return Ze

def CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei):
    Zh = Zarc(Rh, Qh, Ph, frequency)
    Zl = Zarc(Rl, Ql, Pl, frequency)
    Ze = ZarcElectrode(Re, Qe, Pef, Pei, frequency)
    Z = Rinf + Zh + Zl + Ze
    return Z


class Main(QMainWindow, Ui_MainWindow):
    def __init__(ZarcFitWindow, ):
        super(Main, ZarcFitWindow).__init__()
        ZarcFitWindow.setupUi(ZarcFitWindow)        
        ZarcFitWindow.SliderLinf.valueChanged.connect(ZarcFitWindow.updateSldOutLinf)
        ZarcFitWindow.SliderRinf.valueChanged.connect(ZarcFitWindow.updateSldOutRinf)
        ZarcFitWindow.SliderRh.valueChanged.connect(ZarcFitWindow.updateSldOutRh)
        ZarcFitWindow.SliderFh.valueChanged.connect(ZarcFitWindow.updateSldOutFh)
        ZarcFitWindow.SliderPh.valueChanged.connect(ZarcFitWindow.updateSldOutPh)
        ZarcFitWindow.SliderRm.valueChanged.connect(ZarcFitWindow.updateSldOutRm)
        ZarcFitWindow.SliderFm.valueChanged.connect(ZarcFitWindow.updateSldOutFm)
        ZarcFitWindow.SliderPm.valueChanged.connect(ZarcFitWindow.updateSldOutPm)
        ZarcFitWindow.SliderRl.valueChanged.connect(ZarcFitWindow.updateSldOutRl)
        ZarcFitWindow.SliderFl.valueChanged.connect(ZarcFitWindow.updateSldOutFl)
        ZarcFitWindow.SliderPl.valueChanged.connect(ZarcFitWindow.updateSldOutPl)
        ZarcFitWindow.SliderRe.valueChanged.connect(ZarcFitWindow.updateSldOutRe)
        ZarcFitWindow.SliderQe.valueChanged.connect(ZarcFitWindow.updateSldOutQe)
        ZarcFitWindow.SliderPef.valueChanged.connect(ZarcFitWindow.updateSldOutPef)
        ZarcFitWindow.SliderPei.valueChanged.connect(ZarcFitWindow.updateSldOutPei)


    def updateSldOutLinf(ZarcFitWindow, value):
        Linf = 10**(value/100.)
        ZarcFitWindow.SldOutLinf.setText("{:.2E}".format(Linf))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        figCole.canvas.draw()
        
    def updateSldOutRinf(ZarcFitWindow, value):
        Rinf = 10**(value/100.)
        ZarcFitWindow.SldOutRinf.setText("{:.2E}".format(Rinf))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        figCole.canvas.draw()

    def updateSldOutRh(ZarcFitWindow, value):
        Rh = 10**(value/100.)
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(Rh))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        figCole.canvas.draw()

    def updateSldOutFh(ZarcFitWindow, value):
        Fh = 10**(value/100.)
        Qh = 1./(Rh*(2.*np.pi*Fh)**Ph)
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(Fh))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()

    def updateSldOutPh(ZarcFitWindow, value):
        Ph = value/1000.
        ZarcFitWindow.SldOutPh.setText("{:.2E}".format(Ph))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()
        
    def updateSldOutRm(ZarcFitWindow, value):
        Rm = 10**(value/100.)
        ZarcFitWindow.SldOutRm.setText("{:.2E}".format(Rm))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        figCole.canvas.draw()

    def updateSldOutFm(ZarcFitWindow, value):
        Fm = 10**(value/100.)
        Qm = 1./(Rm*(2.*np.pi*Fm)**Pm)
        ZarcFitWindow.SldOutFm.setText("{:.2E}".format(Fm))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()

    def updateSldOutPm(ZarcFitWindow, value):
        Pm = value/1000.
        ZarcFitWindow.SldOutPm.setText("{:.2E}".format(Pm))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()
        
    def updateSldOutRl(ZarcFitWindow, value):
        Rl = 10**(value/100.)
        ZarcFitWindow.SldOutRl.setText("{:.2E}".format(Rl))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        figCole.canvas.draw()

    def updateSldOutFl(ZarcFitWindow, value):
        Fl = 10**(value/100.)
        Ql = 1./(Rl*(2.*np.pi*Fl)**Pl)
        ZarcFitWindow.SldOutFl.setText("{:.2E}".format(Fl))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()
        
    def updateSldOutPl(ZarcFitWindow, value):
        Pl = value/1000.
        ZarcFitWindow.SldOutPl.setText("{:.2E}".format(Pl))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()

    def updateSldOutRe(ZarcFitWindow, value):
        Re = 10**(value/100.)
        ZarcFitWindow.SldOutRe.setText("{:.2E}".format(Re))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        figCole.canvas.draw()

    def updateSldOutQe(ZarcFitWindow, value):
        Qe = 10**(value/100.)
        ZarcFitWindow.SldOutQe.setText("{:.2E}".format(Qe))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()

    def updateSldOutPef(ZarcFitWindow, value):
        Pef = value/1000.
        ZarcFitWindow.SldOutPef.setText("{:.2E}".format(Pef))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()

    def updateSldOutPei(ZarcFitWindow, value):
        Pei = value/1000.
        ZarcFitWindow.SldOutPei.setText("{:.2E}".format(Pei))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        lineBodeMagn.set_ydata(abs(Z))
        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))     
        figCole.canvas.draw()
        

    def addmplCole(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        ZarcFitWindow.toolbar = NavigationToolbar(ZarcFitWindow.canvas, 
                ZarcFitWindow, coordinates=True)
        ZarcFitWindow.addToolBar(ZarcFitWindow.toolbar)     
      
 
if __name__ == '__main__':
    Rinf = 1.E4
    Rh = 1.E5
    Qh = 2.E-10
    Ph = 0.8
    Rl = 5.E4
    Ql = 1.E-5
    Pl = 0.5    
    Re = 1.E10
    Qe = 1.E-4
    Pef = 0.5
    Pei = 0.05    

    frequency = 10.**np.arange(6,-2,-0.2)
    
    Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)

    figCole = Figure()
    axCole = figCole.add_subplot(121)
    lineCole,= axCole.plot(Z.real, Z.imag, 'ro')
    axCole.grid(True)
    axCole.invert_yaxis()
    axCole.set_xlabel("Real [Ohm]")
    axCole.set_ylabel("Imag [Ohm]")
    axCole.hold (False)
    
    axBodeMagn = figCole.add_subplot(222)
    lineBodeMagn, = axBodeMagn.loglog(frequency, abs(Z), 'ro')
    axBodeMagn.grid(True)
    axBodeMagn.invert_xaxis()
    axBodeMagn.set_xlabel("Frequency [Hz]")
    axBodeMagn.set_ylabel("Total Impedance [Ohm]")
    axBodeMagn.hold (False)
 
    axBodePhase = figCole.add_subplot(224)
    lineBodePhase,= axBodePhase.loglog(frequency, abs(np.angle(Z, deg=True)), 'ro')    
    axBodePhase.grid(True)
    axBodePhase.invert_xaxis()
    axBodePhase.set_xlabel("Frequency [Hz]")
    axBodePhase.set_ylabel("Phase [deg]")
    axBodePhase.hold (False)    
 
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addmplCole(figCole)

    main.show()
    sys.exit(app.exec_())   