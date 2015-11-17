import numpy as np
import sys
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from Zarcfit import *
    
Ui_MainWindow, QMainWindow = loadUiType('ZarcFit2015-11-13.ui')  

class Main(QMainWindow, Ui_MainWindow):
    

    def __init__(ZarcFitWindow, zarc, obs, frequency):
        ZarcFitWindow.zarc = zarc
        ZarcFitWindow.obs = obs
        ZarcFitWindow.frequency = frequency

        figCole = Figure()
        gs = gridspec.GridSpec(7, 7)
        axCole = figCole.add_subplot(gs[:, :3])
        axBodeMagn = figCole.add_subplot( gs[:3,4:])
        axBodePhase = figCole.add_subplot(gs[4:,4:])

        # if ZarcFitWindow.radioButtonSerial.isChecked():
        Z = ZarcFitWindow.zarc.Zseries(frequency)  
        # else:
        #     Z = ZarcFitWindow.zarc.Zparallel(frequency)  

        lineColeobs,= axCole.plot(obs.real, obs.imag, 'kx-', lw=3)
        lineCole,= axCole.plot(Z.real, Z.imag, 'ro')    
        # axCole.grid(True)
        axCole.invert_yaxis()
        axCole.set_xlabel("Real [Ohm]")
        axCole.set_ylabel("Imag [Ohm]")
        axCole.hold (False)
        
                
        lineBodeMagnobs, = axBodeMagn.loglog(frequency, abs(obs), 'kx-', lw=3)
        lineBodeMagn, = axBodeMagn.loglog(frequency, abs(Z), 'ro')    
        # axBodeMagn.grid(True)
        axBodeMagn.invert_xaxis()
        axBodeMagn.set_xlabel("Frequency [Hz]")
        axBodeMagn.set_ylabel("Total Impedance [Ohm]")
        axBodeMagn.legend(("Obs","Pred"), bbox_to_anchor=(1.25, 1.), fontsize = 10)
        axBodeMagn.hold (False)    
                    
        lineBodePhaseobs,= axBodePhase.loglog(frequency, abs(np.angle(obs, deg=True)), 'kx-', lw=3)    
        lineBodePhase,= axBodePhase.loglog(frequency, abs(np.angle(Z, deg=True)), 'ro')        
        # axBodePhase.grid(True)
        axBodePhase.invert_xaxis()
        axBodePhase.set_xlabel("Frequency [Hz]")
        axBodePhase.set_ylabel("Phase [deg]")
        axBodePhase.hold (False)            

        ZarcFitWindow.figCole = figCole
        ZarcFitWindow.axCole = axCole
        ZarcFitWindow.axBodeMagn = axBodeMagn
        ZarcFitWindow.axBodePhase = axBodePhase
        
        ZarcFitWindow.lineCole = lineCole
        ZarcFitWindow.lineBodeMagn = lineBodeMagn
        ZarcFitWindow.lineBodePhase = lineBodePhase        

        ZarcFitWindow.lineColeobs = lineColeobs
        ZarcFitWindow.lineBodeMagnobs = lineBodeMagnobs
        ZarcFitWindow.lineBodePhaseobs = lineBodePhaseobs

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
 
    def updateFigs(ZarcFitWindow,Z):
        ZarcFitWindow.lineCole.set_data(Z.real, Z.imag)
        ZarcFitWindow.lineColeobs.set_data(ZarcFitWindow.obs.real, ZarcFitWindow.obs.imag)
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.patch)        
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineCole)
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineColeobs)

        ZarcFitWindow.lineBodeMagn.set_ydata(abs(Z))
        ZarcFitWindow.lineBodeMagnobs.set_ydata(abs(ZarcFitWindow.obs))
        ZarcFitWindow.axBodeMagn.draw_artist(ZarcFitWindow.axBodeMagn.patch)
        ZarcFitWindow.axBodeMagn.draw_artist(ZarcFitWindow.lineBodeMagn)
        ZarcFitWindow.axBodeMagn.draw_artist(ZarcFitWindow.lineBodeMagnobs)        

        ZarcFitWindow.lineBodePhase.set_ydata(abs(np.angle(Z, deg=True)))
        ZarcFitWindow.lineBodePhaseobs.set_ydata(abs(np.angle(ZarcFitWindow.obs, deg=True)))
        ZarcFitWindow.axBodePhase.draw_artist(ZarcFitWindow.axBodePhase.patch)
        ZarcFitWindow.axBodePhase.draw_artist(ZarcFitWindow.lineBodePhase)        
        ZarcFitWindow.axBodePhase.draw_artist(ZarcFitWindow.lineBodePhaseobs)        
        ZarcFitWindow.figCole.canvas.update()     

    def updateSldOutLinf(ZarcFitWindow, value):
        Linf = 10**(value/1000.)
        ZarcFitWindow.SldOutLinf.setText("{:.2E}".format(Linf))
        ZarcFitWindow.zarc.Linf = Linf
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 
        
    def updateSldOutRinf(ZarcFitWindow, value):
        Rinf = 10**(value/1000.)
        ZarcFitWindow.SldOutRinf.setText("{:.2E}".format(Rinf))
        ZarcFitWindow.zarc.Rinf = Rinf
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutRh(ZarcFitWindow, value):

        Rh = 10**(value/1000.)
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(Rh))
        ZarcFitWindow.zarc.Rh = Rh
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z)                 

    def updateSldOutFh(ZarcFitWindow, value):
        Fh = 10**(value/1000.)
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(Fh))
        ZarcFitWindow.zarc.Fh = Fh
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutPh(ZarcFitWindow, value):
        Ph = value/1000.
        ZarcFitWindow.SldOutPh.setText("{:.2E}".format(Ph))
        ZarcFitWindow.zarc.Ph = Ph
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 
        
    def updateSldOutRm(ZarcFitWindow, value):
        Rm = 10**(value/1000.)
        ZarcFitWindow.SldOutRm.setText("{:.2E}".format(Rm))
        ZarcFitWindow.zarc.Rm = Rm
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutFm(ZarcFitWindow, value):
        Fm = 10**(value/1000.)
        ZarcFitWindow.SldOutFm.setText("{:.2E}".format(Fm))
        ZarcFitWindow.zarc.Fm = Fm
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutPm(ZarcFitWindow, value):
        Pm = value/1000.
        ZarcFitWindow.SldOutPm.setText("{:.2E}".format(Pm))
        ZarcFitWindow.zarc.Pm = Pm
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 
        
    def updateSldOutRl(ZarcFitWindow, value):
        Rl = 10**(value/1000.)
        ZarcFitWindow.SldOutRl.setText("{:.2E}".format(Rl))
        ZarcFitWindow.zarc.Rl = Rl
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutFl(ZarcFitWindow, value):
        Fl = 10**(value/1000.)
        ZarcFitWindow.SldOutFl.setText("{:.2E}".format(Fl))
        ZarcFitWindow.zarc.Fl = Fl
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 
        
    def updateSldOutPl(ZarcFitWindow, value):
        Pl = value/1000.
        ZarcFitWindow.SldOutPl.setText("{:.2E}".format(Pl))
        ZarcFitWindow.zarc.Pl = Pl
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutRe(ZarcFitWindow, value):
        Re = 10**(value/1000.)
        ZarcFitWindow.SldOutRe.setText("{:.2E}".format(Re))
        ZarcFitWindow.zarc.Re = Re
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutQe(ZarcFitWindow, value):
        Qe = 10**(value/1000.)
        ZarcFitWindow.SldOutQe.setText("{:.2E}".format(Qe))
        ZarcFitWindow.zarc.Qe = Qe
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutPef(ZarcFitWindow, value):
        Pef = value/1000.
        ZarcFitWindow.SldOutPef.setText("{:.2E}".format(Pef))
        ZarcFitWindow.zarc.Pef = Pef
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 

    def updateSldOutPei(ZarcFitWindow, value):
        Pei = value/1000.
        ZarcFitWindow.SldOutPei.setText("{:.2E}".format(Pei))
        ZarcFitWindow.zarc.Pei = Pei
        Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.updateFigs(Z) 
        

    def addmplCole(ZarcFitWindow):
        ZarcFitWindow.canvas = FigureCanvas(ZarcFitWindow.figCole)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        ZarcFitWindow.toolbar = NavigationToolbar(ZarcFitWindow.canvas, ZarcFitWindow, coordinates=True)
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        else:
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        ZarcFitWindow.addToolBar(ZarcFitWindow.toolbar)     

    def linearmap():
        re      
 
if __name__ == '__main__':
    Rinf = 1.E4
    Rh = 1.E5
    Fh = 1e6
    Ph = 0.8
    Rm = 1e-1
    Fm = 1e-1
    Pm = 1.        
    Rl = 5.E4
    Fl = 1e1
    Pl = 0.5    
    Re = 1.E10
    Qe = 1.E-4
    Pef = 0.5
    Pei = 0.05    

    path = "../data/HVC2014_10Grenon/"
    fnameobs = "BC13867-A 2014-10-23.z"
    pathobs = path+fnameobs
    temp = np.loadtxt(pathobs, skiprows=11, delimiter=",")
    obs = temp[:,4]+1j*temp[:,5]
    frequency = temp[:,0].copy()
    zarc = Zarcfit(obs, frequency)
    zarc.SetParametersSeries(0., Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei)     
    app = QtGui.QApplication(sys.argv)
    main = Main(zarc, obs, frequency)
    main.addmplCole()
    main.show()
    sys.exit(app.exec_())   