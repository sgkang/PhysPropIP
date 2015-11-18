import numpy as np
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from Zarcfit import *
    
Ui_MainWindow, QMainWindow = loadUiType('ZarcFit2015-11-13.ui')  

class PathPicker(QtGui.QWidget):
    def __init__(self):
        print("PathPicker Called")
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('path picker')
        # Set the window dimensions
        self.resize(300,75)       
        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)
        # Create a label which displays the path to our chosen path
        self.lbl = QtGui.QLabel('No path selected')
        self.vbox.addWidget(self.lbl)
        # Create a push button labelled 'choose' and add it to our layout
        btn = QtGui.QPushButton('Choose path', self)
        self.vbox.addWidget(btn)        
        # Connect the clicked signal to the get_fname handler
        self.connect(btn, QtCore.SIGNAL('clicked()'), self.get_fname)

    def get_fname(self):
        """
        Handler called when 'choose path' is clicked
        """
        # When you call getOpenPathName, a path picker dialog is created
        # and if the user selects a path, it's path is returned, and if not
        # (ie, the user cancels the operation) None is returned
        fname = QtGui.QFileDialog.getExistingDirectory(self, "Select Path")
        if fname:
            self.lbl.setText(fname)
        else:
            self.lbl.setText('No path selected')


class Main(QMainWindow, Ui_MainWindow):
    
    fwdtype = "series"
    axComplexReal = None
    axComplexImag = None

    def __init__(ZarcFitWindow, zarc, obs, frequency):
        ZarcFitWindow.zarc = zarc
        ZarcFitWindow.obs = obs
        ZarcFitWindow.frequency = frequency

        figCole = Figure()
        gs = gridspec.GridSpec(7, 7)
        axCole = figCole.add_subplot(gs[:, :3])
        axBodeMagn = figCole.add_subplot( gs[:3,4:])
        axBodePhase = figCole.add_subplot(gs[4:,4:])

        # Only for the initialization default is "series"
        if ZarcFitWindow.fwdtype == "series":        
            Z = ZarcFitWindow.zarc.Zseries(frequency)  
        elif ZarcFitWindow.fwdtype == "parallel":
            Z = ZarcFitWindow.zarc.Zparallel(frequency)  
        else:
            Exception("Not implemented!! choose either series or parallel")

        lineColeobs,= axCole.plot(obs.real, obs.imag, 'kx-', lw=3)
        lineCole,= axCole.plot(Z.real, Z.imag, 'ro')    
        axCole.invert_yaxis()
        axCole.set_xlabel("Real [Ohm]")
        axCole.set_ylabel("Imag [Ohm]")
        axCole.hold (False)
        
                
        lineBodeMagnobs, = axBodeMagn.loglog(frequency, abs(obs), 'kx-', lw=3)
        lineBodeMagn, = axBodeMagn.loglog(frequency, abs(Z), 'ro')    
        axBodeMagn.invert_xaxis()
        axBodeMagn.set_xlabel("Frequency [Hz]")
        axBodeMagn.set_ylabel("Total Impedance [Ohm]")
        axBodeMagn.legend(("Obs","Pred"), bbox_to_anchor=(1.25, 1.), fontsize = 10)
        axBodeMagn.hold (False)    
                    
        lineBodePhaseobs,= axBodePhase.loglog(frequency, abs(np.angle(obs, deg=True)), 'kx-', lw=3)    
        lineBodePhase,= axBodePhase.loglog(frequency, abs(np.angle(Z, deg=True)), 'ro')        
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
        ZarcFitWindow.actionSelect_Path.triggered.connect(PathPicker.show)
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
        
        #Connect QRadiobutton
        ZarcFitWindow.radioButtonSerial.clicked.connect(ZarcFitWindow.updateRadiOutSerial)
        ZarcFitWindow.radioButtonParallel.clicked.connect(ZarcFitWindow.updateRadiOutParallel)        
        # ZarcFitWindow.radioButtonBodePlots.clicked.connect(ZarcFitWindow.updateRadiOutBodePlots)
        # ZarcFitWindow.radioButtonComplexPlots.clicked.connect(ZarcFitWindow.updateRadiOutComplexPlots)

    def updateRadiOutSerial(ZarcFitWindow, value):
        ZarcFitWindow.updateFigs()

    def updateRadiOutParallel(ZarcFitWindow, value):
        ZarcFitWindow.updateFigs()        
    
    def updateRadiOutBodePlots(ZarcFitWindow, value):
        ZarcFitWindow.updateFigs()

    def updateRadiOutComplexPlots(ZarcFitWindow, value):
        ZarcFitWindow.updateFigs()
                        
    def updateFigs(ZarcFitWindow):

        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        elif ZarcFitWindow.radioButtonParallel.isChecked():
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        else:
            Exception("Not implemented!! choose either series or parallel")

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
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutRinf(ZarcFitWindow, value):
        Rinf = 10**(value/1000.)
        ZarcFitWindow.SldOutRinf.setText("{:.2E}".format(Rinf))
        ZarcFitWindow.zarc.Rinf = Rinf
        ZarcFitWindow.updateFigs() 

    def updateSldOutRh(ZarcFitWindow, value):
        Rh = 10**(value/1000.)
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(Rh))
        ZarcFitWindow.zarc.Rh = Rh
        ZarcFitWindow.updateFigs()                 

    def updateSldOutFh(ZarcFitWindow, value):
        Fh = 10**(value/1000.)
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(Fh))
        ZarcFitWindow.zarc.Fh = Fh
        ZarcFitWindow.updateFigs() 

    def updateSldOutPh(ZarcFitWindow, value):
        Ph = value/1000.
        ZarcFitWindow.SldOutPh.setText("{:.2E}".format(Ph))
        ZarcFitWindow.zarc.Ph = Ph
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutRm(ZarcFitWindow, value):
        Rm = 10**(value/1000.)
        ZarcFitWindow.SldOutRm.setText("{:.2E}".format(Rm))
        ZarcFitWindow.zarc.Rm = Rm
        ZarcFitWindow.updateFigs() 

    def updateSldOutFm(ZarcFitWindow, value):
        Fm = 10**(value/1000.)
        ZarcFitWindow.SldOutFm.setText("{:.2E}".format(Fm))
        ZarcFitWindow.zarc.Fm = Fm
        ZarcFitWindow.updateFigs() 

    def updateSldOutPm(ZarcFitWindow, value):
        Pm = value/1000.
        ZarcFitWindow.SldOutPm.setText("{:.2E}".format(Pm))
        ZarcFitWindow.zarc.Pm = Pm
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutRl(ZarcFitWindow, value):
        Rl = 10**(value/1000.)
        ZarcFitWindow.SldOutRl.setText("{:.2E}".format(Rl))
        ZarcFitWindow.zarc.Rl = Rl
        ZarcFitWindow.updateFigs() 

    def updateSldOutFl(ZarcFitWindow, value):
        Fl = 10**(value/1000.)
        ZarcFitWindow.SldOutFl.setText("{:.2E}".format(Fl))
        ZarcFitWindow.zarc.Fl = Fl
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutPl(ZarcFitWindow, value):
        Pl = value/1000.
        ZarcFitWindow.SldOutPl.setText("{:.2E}".format(Pl))
        ZarcFitWindow.zarc.Pl = Pl
        ZarcFitWindow.updateFigs() 

    def updateSldOutRe(ZarcFitWindow, value):
        Re = 10**(value/1000.)
        ZarcFitWindow.SldOutRe.setText("{:.2E}".format(Re))
        ZarcFitWindow.zarc.Re = Re
        ZarcFitWindow.updateFigs() 

    def updateSldOutQe(ZarcFitWindow, value):
        Qe = 10**(value/1000.)
        ZarcFitWindow.SldOutQe.setText("{:.2E}".format(Qe))
        ZarcFitWindow.zarc.Qe = Qe
        ZarcFitWindow.updateFigs() 

    def updateSldOutPef(ZarcFitWindow, value):
        Pef = value/1000.
        ZarcFitWindow.SldOutPef.setText("{:.2E}".format(Pef))
        ZarcFitWindow.zarc.Pef = Pef
        ZarcFitWindow.updateFigs() 

    def updateSldOutPei(ZarcFitWindow, value):
        Pei = value/1000.
        ZarcFitWindow.SldOutPei.setText("{:.2E}".format(Pei))
        ZarcFitWindow.zarc.Pei = Pei
        ZarcFitWindow.updateFigs() 
        

    def addmplCole(ZarcFitWindow):
        ZarcFitWindow.canvas = FigureCanvas(ZarcFitWindow.figCole)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        ZarcFitWindow.toolbar = NavigationToolbar(ZarcFitWindow.canvas, ZarcFitWindow, coordinates=True)
        ZarcFitWindow.addToolBar(ZarcFitWindow.toolbar)     
 
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