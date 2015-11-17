import numpy as np
import sys
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
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

def updateaxisCole(Z, line, ax, fig):
    line.set_data(Z.real, Z.imag) 
    ax.draw_artist(ax.patch)        
    ax.draw_artist(line)
    fig.canvas.update()       
    return

def updateaxisBodeMagn(Z, line, ax, fig):
    line.set_ydata(abs(Z))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)        
    fig.canvas.update()          
    return        

def updateaxisBodePhase(Z, line, ax, fig):
    line.set_ydata(abs(np.angle(Z, deg=True)))
    ax.draw_artist(ax.patch)
    ax.draw_artist(line)        
    fig.canvas.update()          
    return         

class Main(QMainWindow, Ui_MainWindow):
    def __init__(ZarcFitWindow, ):
        super(Main, ZarcFitWindow).__init__()
        ZarcFitWindow.setupUi(ZarcFitWindow)        
        ZarcFitWindow.SliderRh.valueChanged.connect(ZarcFitWindow.updateSldOutRh)
        ZarcFitWindow.SliderFh.valueChanged.connect(ZarcFitWindow.updateSldOutFh)      

    def updateSldOutRh(self, ZarcFitWindow, value):
        Rh = 10**(value/100.)
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(Rh))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        axCole.draw_artist(axCole.patch)        
        axCole.draw_artist(lineCole)
        axCole.grid(True)
        figCole.canvas.update()       
        # updateaxisCole(Z, lineCole, axCole, figCole)

        lineBodeMagn.set_ydata(abs(Z))
        axBodeMagn.draw_artist(axBodeMagn.patch)
        axBodeMagn.draw_artist(lineBodeMagn)        
        figBodeMagn.canvas.update()          
        # updateaxisBodeMagn(Z, lineBodeMagn, axBodeMagn, figBodeMagn)

        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        axBodePhase.draw_artist(axBodePhase.patch)
        axBodePhase.draw_artist(lineBodePhase)        
        figBodePhase.canvas.update()   
        # updateaxisBodePhase(Z, lineBodePhase, axBodePhase, figBodePhase)

    def updateSldOutFh(self, Z, arcFitWindow, value):
        Fh = 10**(value/100.)
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(10**(value/100.)))
        Z = CalculateImpedance(frequency, Rinf, Rh, Qh, Ph, Rl, Ql, Pl, Re, Qe, Pef, Pei)
        lineCole.set_data(Z.real, Z.imag)
        axCole.draw_artist(axCole.patch)
        axCole.draw_artist(lineCole)
        plt.grid(True)
        figCole.canvas.update()                

        lineBodeMagn.set_ydata(abs(Z))
        axBodeMagn.draw_artist(axBodeMagn.patch)
        axBodeMagn.draw_artist(lineBodeMagn)
        figBodeMagn.canvas.update()    

        lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        axBodePhase.draw_artist(axBodePhase.patch)
        axBodePhase.draw_artist(lineBodePhase)        
        figBodePhase.canvas.update()    
        # updateaxisCole(Z, lineCole, axCole, figCole)
        # updateaxisBodeMagn(Z, lineBodeMagn, axBodeMagn, figBodeMagn)
        # updateaxisBodePhase(Z, lineBodePhase, axBodePhase, figBodePhase)

    def addmplCole(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  

    def addmplBodeMagn(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplBodeMagn.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        
    def addmplBodePhase(ZarcFitWindow, fig):
        ZarcFitWindow.canvas = FigureCanvas(fig)
        ZarcFitWindow.mplBodePhase.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()         
 
if __name__ == '__main__':

    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'grid.color': 'black', 'grid.linewidth':1})

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

    figCole, axCole = plt.subplots()

    lineCole,= axCole.plot(Z.real, Z.imag, 'deepskyblue', lw=2)
    axCole.grid(True)
    axCole.invert_yaxis()
    axCole.set_xlabel("Real [Ohm]")
    axCole.set_ylabel("Imag [Ohm]")
    # axCole.hold (False)
    axCole.patch.set_facecolor('white')
    
    figBodeMagn, axBodeMagn = plt.subplots()
    lineBodeMagn, = axBodeMagn.loglog(frequency, abs(Z), 'deepskyblue', lw=2)
    axBodeMagn.grid(True)
    axBodeMagn.invert_xaxis()
    axBodeMagn.set_xlabel("Frequency [Hz]")
    axBodeMagn.set_ylabel("Total Impedance [Ohm]")
    # axBodeMagn.hold (False)
    axBodeMagn.patch.set_facecolor('white')
 
    figBodePhase, axBodePhase = plt.subplots()
    lineBodePhase,= axBodePhase.loglog(frequency, abs(np.angle(Z, deg=True)), 'deepskyblue', lw=2)    
    axBodePhase.grid(True)
    axBodePhase.invert_xaxis()
    axBodePhase.set_xlabel("Frequency [Hz]")
    axBodePhase.set_ylabel("Phase [deg]")
    # axBodePhase.hold (False)    
    axBodePhase.patch.set_facecolor('white')
 
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addmplCole(figCole)
    main.addmplBodeMagn(figBodeMagn)
    main.addmplBodePhase(figBodePhase)
    
    main.show()
    sys.exit(app.exec_())   