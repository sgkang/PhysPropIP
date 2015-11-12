
import numpy as np
import sys
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
Ui_MainWindow, QMainWindow = loadUiType('ZarcFit2015-11-11.ui')  

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

        
        ZarcFitWindow.Slider.valueChanged.connect(ZarcFitWindow.updateSliderNumber)
        ZarcFitWindow.Slider_2.valueChanged.connect(ZarcFitWindow.updateSliderNumber_2)


    def updateSliderNumber(ZarcFitWindow, value):
        Rh = 10**(value/100.)
        ZarcFitWindow.SliderNumber.setText("{:.3E}".format(Rh))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        axCole.hold (False)
        axCole.plot(Z.real, Z.imag, 'ro')
        fig1.canvas.draw()

    def updateSliderNumber_2(ZarcFitWindow, value):
        ZarcFitWindow.SliderNumber_2.setText("{:.3E}".format(10**(value/100.)))

    def addmpl(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplvl.addWidget(ZarcFitWindow.canvas)
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
    Pei = 0.1    

    frequency = 10.**np.arange(6,-2,-0.2)
    
    Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)

    fig1 = Figure()
    axCole = fig1.add_subplot(111)
    axCole.plot(Z.real, Z.imag, 'ro')
    axCole.grid(True)
    axCole.invert_yaxis()
    axCole.set_xlabel("Real [Ohm]")
    axCole.set_ylabel("Imag [Ohm]")
 
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addmpl(fig1)
    
    main.show()
    sys.exit(app.exec_())   