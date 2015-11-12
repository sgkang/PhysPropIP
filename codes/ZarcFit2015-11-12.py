
import numpy as np
import sys
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
Ui_MainWindow, QMainWindow = loadUiType('ZarcFit2015-11-12.ui')  

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

        
        ZarcFitWindow.SliderRh.valueChanged.connect(ZarcFitWindow.updateSldOutRh)
        ZarcFitWindow.SliderFh.valueChanged.connect(ZarcFitWindow.updateSldOutFh)


    def updateSldOutRh(ZarcFitWindow, value):
        Rh = 10**(value/100.)
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(Rh))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        axCole.hold (False)
        axCole.plot(Z.real, Z.imag, 'ro')
        axCole.grid(True)
        figCole.canvas.draw()
        axBodeMagn.hold (False)
        axBodeMagn.loglog(frequency, abs(Z), 'ro')
        axBodeMagn.grid(True)
        figBodeMagn.canvas.draw()
        axBodePhase.hold (False)
        axBodePhase.loglog(frequency, abs(np.angle(Z, deg=True)), 'ro')
        axBodePhase.grid(True)
        figBodePhase.canvas.draw()

    def updateSldOutFh(ZarcFitWindow, value):
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(10**(value/100.)))

    def addmplCole(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
#        ZarcFitWindow.toolbar = NavigationToolbar(ZarcFitWindow.canvas, 
#                ZarcFitWindow, coordinates=True)
#        ZarcFitWindow.addToolBar(ZarcFitWindow.toolbar)     

    def addmplBodeMagn(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplBodeMagn.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        
    def addmplBodePhase(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplBodePhase.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
       
 
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
    Pei = 0.1    

    frequency = 10.**np.arange(6,-2,-0.2)
    
    Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)

    figCole = Figure()
    axCole = figCole.add_subplot(111)
    axCole.plot(Z.real, Z.imag, 'ro')
    axCole.grid(True)
    axCole.invert_yaxis()
    axCole.set_xlabel("Real [Ohm]")
    axCole.set_ylabel("Imag [Ohm]")
    
    figBodeMagn = Figure()
    axBodeMagn = figBodeMagn.add_subplot(111)
    axBodeMagn.loglog(frequency, abs(Z), 'ro')
    axBodeMagn.grid(True)
    axBodeMagn.invert_xaxis()
    axBodeMagn.set_xlabel("Frequency [Hz]")
    axBodeMagn.set_ylabel("Total Impedance [Ohm]")
 
    figBodePhase = Figure()
    axBodePhase = figBodePhase.add_subplot(111)
    axBodePhase.loglog(frequency, abs(np.angle(Z, deg=True)), 'ro')
    axBodePhase.grid(True)
    axBodePhase.invert_xaxis()
    axBodePhase.set_xlabel("Frequency [Hz]")
    axBodePhase.set_ylabel("Phase [deg]")
 
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addmplCole(figCole)
    main.addmplBodeMagn(figBodeMagn)
    main.addmplBodePhase(figBodePhase)
    
    main.show()
    sys.exit(app.exec_())   