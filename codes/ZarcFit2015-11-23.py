import numpy as np
import sys, glob, os
from PyQt4 import QtGui, QtCore
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from Zarcfit import *
    
Ui_MainWindow, QMainWindow = loadUiType('ZarcFit2015-11-23.ui')  

class PathPicker(QtGui.QWidget):

    fnamestr = None

    def __init__(self, ZarcFitWindow, parent=None):
        # create GUI
        super(PathPicker, self).__init__()
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
        # Connect to ZarcFitWindow
        self.ZarcFitWindow = ZarcFitWindow

    def get_fname(self):
        """
        Handler called when 'choose path' is clicked
        """
        # When you call getOpenPathName, a path picker dialog is created
        # and if the user selects a path, it's path is returned, and if not
        # (ie, the user cancels the operation) None is returned
        fname = QtGui.QFileDialog.getExistingDirectory(self, "Select Path")
        self.fnamestr = str(fname)

        if fname:
            self.lbl.setText(fname)
            self.ZarcFitWindow.lineEditPath.setText(fname)
            self.ZarcFitWindow.getOBSFNAME()
        else:
            self.lbl.setText('No path selected')


class Main(QMainWindow, Ui_MainWindow):
    
    fwdtype = "series"
    axComplexReal = None
    axComplexImag = None
    OBSFNAME = None

    def __init__(ZarcFitWindow, zarc, obs, frequency):
        ZarcFitWindow.zarc = zarc
        ZarcFitWindow.obs = obs
        ZarcFitWindow.frequency = frequency
        hmlFreq = np.array([ZarcFitWindow.zarc.Fh,
                            ZarcFitWindow.zarc.Fm,
                            ZarcFitWindow.zarc.Fl,])


        figCole = Figure()
        gs = gridspec.GridSpec(7, 7)
        axCole = figCole.add_subplot(gs[:, :3])
        axBodeMagn = figCole.add_subplot( gs[:3,4:])
        axBodePhase = figCole.add_subplot(gs[4:,4:])

        if ZarcFitWindow.fwdtype == "series":        
            Z = ZarcFitWindow.zarc.Zseries(frequency)  
#            Zhml = ZarcFitWindow.zarc.Zseries(hmlFreq) 
#            Zhml = np.array([1.,2.,3.])*(1-1j)*1.E4
        elif ZarcFitWindow.fwdtype == "parallel":
            Z = ZarcFitWindow.zarc.Zparallel(frequency)  
#            Zhml = ZarcFitWindow.zarc.Zseries(hmlFreq)  
        else:
            Exception("Not implemented!! choose either series or parallel")

        mergedZreal = np.append(np.concatenate((Z.real, obs.real)), 0.)
        mergedZimag = np.append(np.concatenate((Z.imag, obs.imag)), 0.)

        # Cole-Cole Plot: Real vs Imag
        lineColeZeroImag,= axCole.plot([min(mergedZreal), max(mergedZreal)], [0., 0.], 
             color='salmon', linewidth=1)                                
        lineColeZeroReal,= axCole.plot([0., 0.], [min(mergedZimag), max(mergedZimag)], 
             color='salmon', linewidth=1)   
#        scatterColehml = axCole.scatter(Zhml.real, Zhml.imag, 
#            c=[2.,1.,0.], marker='+', linewidth=2, s=80)                                
        lineCole,= axCole.plot(Z.real, Z.imag, 
             color='cyan', marker='D', markersize=3, linewidth=2)                                
        lineColeobs,= axCole.plot(obs.real, obs.imag, 
             color='green', marker='s', markersize=2, linewidth=1) 
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
        
        ZarcFitWindow.actionSelect_Path.triggered.connect(ZarcFitWindow.PickPath)
        ZarcFitWindow.actionSelect_Parameter_File.triggered.connect(ZarcFitWindow.SelectParameterFile)
        ZarcFitWindow.actionObs_File_Type.triggered.connect(ZarcFitWindow.SelectObsFileType)
        ZarcFitWindow.actionNext_Obs_File.triggered.connect(ZarcFitWindow.NextObsFile)
        ZarcFitWindow.actionPrev_Obs_File.triggered.connect(ZarcFitWindow.PrevObsFile)
        ZarcFitWindow.actionF1_Fit_Spectrum_Cartesian_Cole.triggered.connect(ZarcFitWindow.FitCole)
        ZarcFitWindow.actionF2_Fit_Spectrum_Polar_Bode.triggered.connect(ZarcFitWindow.FitBode)
        ZarcFitWindow.actionF3_All_Freq_s.triggered.connect(ZarcFitWindow.AllFreqs)
        ZarcFitWindow.actionF7_Read_Parameters.triggered.connect(ZarcFitWindow.ReadParameters)
        ZarcFitWindow.actionF8_Default_Start_Model.triggered.connect(ZarcFitWindow.DefaultStartModel)
        ZarcFitWindow.actionWrite_Header.triggered.connect(ZarcFitWindow.WriteHeader)
        ZarcFitWindow.actionF4_Write_Fit.triggered.connect(ZarcFitWindow.WriteParam)
        ZarcFitWindow.actionZarcFit_Help.triggered.connect(ZarcFitWindow.ZarcFitHelp)
        ZarcFitWindow.actionAbout_ZarcFit.triggered.connect(ZarcFitWindow.AboutZarcFit)
        
        ZarcFitWindow.spinBoxObsFileNumber.valueChanged.connect(ZarcFitWindow.ReadObsFile)
        ZarcFitWindow.pushButtonFitCole.clicked.connect(ZarcFitWindow.FitCole)
        ZarcFitWindow.pushButtonFitBode.clicked.connect(ZarcFitWindow.FitBode)
        ZarcFitWindow.pushButtonWriteHeader.clicked.connect(ZarcFitWindow.WriteHeader)
        ZarcFitWindow.pushButtonWriteParam.clicked.connect(ZarcFitWindow.WriteParam)
        
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

        ZarcFitWindow.spinBoxHighFreq.valueChanged.connect(ZarcFitWindow.updateHighFreq)
        ZarcFitWindow.spinBoxLowFreq.valueChanged.connect(ZarcFitWindow.updateLowFreq)
        
        #Connect QRadiobutton
        ZarcFitWindow.radioButtonSerial.clicked.connect(ZarcFitWindow.updateRadiOutSerial)
        ZarcFitWindow.radioButtonParallel.clicked.connect(ZarcFitWindow.updateRadiOutParallel)        
        # ZarcFitWindow.radioButtonBodePlots.clicked.connect(ZarcFitWindow.updateRadiOutBodePlots)
        # ZarcFitWindow.radioButtonComplexPlots.clicked.connect(ZarcFitWindow.updateRadiOutComplexPlots)
        ZarcFitWindow.PathPickerWindow = PathPicker(ZarcFitWindow)
        
        ZarcFitWindow.spinBoxHighFreq.setValue(0)
        ZarcFitWindow.labelHighFreq.setText("{:,}".format(frequencyAll[0])+" Hz")
        ZarcFitWindow.spinBoxLowFreq.setValue(frequencyN-1)
        ZarcFitWindow.labelLowFreq.setText("{:,}".format(frequencyAll[frequencyN-1])+" Hz")


    
                        
    #### Matplotlib window ####
    def addmplCole(ZarcFitWindow):
        ZarcFitWindow.canvas = FigureCanvas(ZarcFitWindow.figCole)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        ZarcFitWindow.toolbar = NavigationToolbar(ZarcFitWindow.canvas, ZarcFitWindow, coordinates=True)
        ZarcFitWindow.addToolBar(ZarcFitWindow.toolbar)   
        
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
        

    #### Menus and Buttons ####
    # # # Files # # #
    def PickPath(ZarcFitWindow):
        ZarcFitWindow.PathPickerWindow.show()        
        # ZarcFitWindow.PathPickerWindow.exec_()        
    
    def getOBSFNAME(ZarcFitWindow):
        ZarcFitWindow.OBSFNAME = []
        if ZarcFitWindow.PathPickerWindow.fnamestr:                
            os.chdir(ZarcFitWindow.PathPickerWindow.fnamestr)                
            # Read *.z file in the path
            for file in glob.glob("*.z"):
                ZarcFitWindow.OBSFNAME.append(file) 
                print (file)
            ZarcFitWindow.OBSFNAMEdirsize = len(ZarcFitWindow.OBSFNAME)
            print(ZarcFitWindow.OBSFNAMEdirsize)
            ZarcFitWindow.horizontalSliderObsFileNumber.setMaximum(ZarcFitWindow.OBSFNAMEdirsize-1)

    def ReadObsFile(ZarcFitWindow, value):
        ZarcFitWindow.lineEditOBSFNAME.setText(ZarcFitWindow.OBSFNAME[value])
        print (value, ZarcFitWindow.OBSFNAME[value], ZarcFitWindow.lineEditPRMFNAME.text())

    def SelectParameterFile(ZarcFitWindow):
        print ("SelectParameterFile")

    def SelectObsFileType(ZarcFitWindow):
        print ("SelectObsFileType")

    def NextObsFile(ZarcFitWindow):
        print ("NextObsFile")

    def PrevObsFile(ZarcFitWindow):
        print ("PrevObsFile")

    # # # Fits # # #
    def updateHighFreq(ZarcFitWindow, value):
        ZarcFitWindow.spinBoxHighFreq.setValue(value)
        ZarcFitWindow.labelHighFreq.setText("{:,}".format(frequency[value])+" Hz")
        #choose frequencies and set limits for plots
        #ZarcFitWindow.updateFigs()

    def updateLowFreq(ZarcFitWindow, value):
        ZarcFitWindow.spinBoxLowFreq.setValue(value)
        ZarcFitWindow.labelLowFreq.setText("{:,}".format(frequency[value])+" Hz")
        #choose frequencies and set limits for plots
        #ZarcFitWindow.updateFigs()
       
    def AllFreqs(ZarcFitWindow):
        print ("AllFreqs")
        
    def ReadParameters(ZarcFitWindow):
        print ("ReadParameters")
        
    def DefaultStartModel(ZarcFitWindow):
        print ("DefaultStartModel")
        
    def FitCole(ZarcFitWindow):
        print ("Fit Cole")
        
    def FitBode(ZarcFitWindow):
        print ("Fit Bode")
        
    def WriteHeader(ZarcFitWindow):
        print ("Write Header")
        
    def WriteParam(ZarcFitWindow):
        print ("Write Param")
        
    def updateRadiOutSerial(ZarcFitWindow, value):
        ZarcFitWindow.fwdtype = "series"
        ZarcFitWindow.updateFigs()

    def updateRadiOutParallel(ZarcFitWindow, value):
        ZarcFitWindow.fwdtype = "parallel"
        ZarcFitWindow.updateFigs()        
    
    def updateRadiOutBodePlots(ZarcFitWindow, value):
        ZarcFitWindow.updateFigs()

    def updateRadiOutComplexPlots(ZarcFitWindow, value):
        ZarcFitWindow.updateFigs()
        

    # # # Help # # #
    def ZarcFitHelp(ZarcFitWindow):
        print ("ZarcFitHelp")
        
    def AboutZarcFit(ZarcFitWindow):
        print ("AboutZarcFit")
        
    #### Update Sliders ####
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
        

############################################################################### 
############################################################################### 
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
    frequencyAll = temp[:,0].copy()
    frequencyN = len (frequencyAll)
    print (frequencyN, frequencyAll[0],frequencyAll[frequencyN-1],)
    frequency = frequencyAll
    zarc = Zarcfit(obs, frequency)
    zarc.SetParametersSeries(0., Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei)     
    app = QtGui.QApplication(sys.argv)
    main = Main(zarc, obs, frequency)
    main.addmplCole()
    main.show()
    sys.exit(app.exec_())   