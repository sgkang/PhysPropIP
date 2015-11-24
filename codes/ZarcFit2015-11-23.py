import numpy as np
import sys, glob, os
from PyQt4 import QtGui, QtCore
from PyQt4.uic import loadUiType
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from Zarcfit import *
matplotlib.rcParams['axes.facecolor']="white"    
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
    plottype = "bode"
    axComplexReal = None
    axComplexImag = None
    obsfname = None

    def __init__(ZarcFitWindow, zarc, obs, frequency):
        
        ZarcFitWindow.zarc = zarc
        ZarcFitWindow.obs = obs
        ZarcFitWindow.frequency = frequency

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
        ZarcFitWindow.radioButtonBodePlots.clicked.connect(ZarcFitWindow.updateRadiOutBodePlots)
        ZarcFitWindow.radioButtonComplexPlots.clicked.connect(ZarcFitWindow.updateRadiOutComplexPlots)
        ZarcFitWindow.PathPickerWindow = PathPicker(ZarcFitWindow)
        
        ZarcFitWindow.spinBoxHighFreq.setValue(0)
        ZarcFitWindow.labelHighFreq.setText("{:,}".format(frequencyAll[0])+" Hz")
        ZarcFitWindow.spinBoxLowFreq.setValue(frequencyN-1)
        ZarcFitWindow.labelLowFreq.setText("{:,}".format(frequencyAll[frequencyN-1])+" Hz")
        ZarcFitWindow.initializeFigure()


    
                        
    #### Matplotlib window ####
    def initializeFigure(ZarcFitWindow):

        hmlFreq = np.array([ZarcFitWindow.zarc.Fh,
                            ZarcFitWindow.zarc.Fm,
                            ZarcFitWindow.zarc.Fl,])

        figCole = plt.figure(figsize=(30,30), facecolor="white")        
        gs = gridspec.GridSpec(7, 7)        

        axCole = figCole.add_subplot(gs[:, :3])                
        axColeRT = figCole.add_subplot( gs[:3,4:])
        axColeRB = figCole.add_subplot(gs[4:,4:])        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
#            Zhml = ZarcFitWindow.zarc.Zseries(hmlFreq) 
#            Zhml = np.array([1.,2.,3.])*(1-1j)*1.E4            
        elif ZarcFitWindow.radioButtonParallel.isChecked():
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
#            Zhml = ZarcFitWindow.zarc.Zseries(hmlFreq)              
        else:
            Exception("Not implemented!! choose either series or parallel")

        mergedZreal = np.append(np.concatenate((Z.real, obs.real)), 0.)
        mergedZimag = np.append(np.concatenate((-Z.imag, -obs.imag)), 0.)

        # Cole-Cole Plot: Real vs Imag
        lineColeZeroImag,= axCole.plot([min(mergedZreal), max(mergedZreal)], [0., 0.], 
             color='salmon', linewidth=1)                                
        lineColeZeroReal,= axCole.plot([0., 0.], [min(mergedZimag), max(mergedZimag)], 
             color='salmon', linewidth=1)   
#        scatterColehml = axCole.scatter(Zhml.real, Zhml.imag, 
#            c=[2.,1.,0.], marker='+', linewidth=2, s=80)                                
        lineCole,= axCole.plot(Z.real, -Z.imag, 
             color='cyan', marker='D', markersize=3, linewidth=2)                                
        lineColeobs,= axCole.plot(obs.real, -obs.imag, 
             color='green', marker='s', markersize=2, linewidth=1) 
        # axCole.invert_yaxis()
        axCole.set_xlabel("Real [kOhm]")
        axCole.set_ylabel("-Imag [kOhm]")
        axColexlim = axCole.set_xlim(0., mergedZreal.max())
        axColeylim = axCole.set_ylim(0., mergedZimag.max())        
        axCole.hold (False)
        
        if ZarcFitWindow.radioButtonBodePlots.isChecked():

            lineColeRTobs, = axColeRT.loglog(frequency, abs(obs),
                color='green', marker='s', markersize=2, linewidth=1)
            lineColeRTpred, = axColeRT.loglog(frequency, abs(Z),
                color='cyan', marker='D', markersize=3, linewidth=2)    
            lineColeRBobs,= axColeRB.loglog(frequency, abs(np.angle(obs, deg=True)),
                color='green', marker='s', markersize=2, linewidth=1)    
            lineColeRBpred,= axColeRB.loglog(frequency, abs(np.angle(Z, deg=True)),
                color='cyan', marker='D', markersize=3, linewidth=2)    
            axColeRT.set_ylabel("Total Impedance [Ohm]")
            axColeRB.set_ylabel("Phase [deg]")

        elif ZarcFitWindow.radioButtonComplexPlots.isChecked():

            lineColeRTobs, = axColeRT.loglog(frequency, obs.real,
                color='green', marker='s', markersize=2, linewidth=1)
            lineColeRTpred, = axColeRT.loglog(frequency, Z.real,
                color='cyan', marker='D', markersize=3, linewidth=2)    
            lineColeRBobs,= axColeRB.loglog(frequency, -obs.imag,
                color='green', marker='s', markersize=2, linewidth=1)    
            lineColeRBpred,= axColeRB.loglog(frequency, -Z.imag,
                color='cyan', marker='D', markersize=3, linewidth=2)    
            axColeRT.set_ylabel("Real [Ohm]")
            axColeRB.set_ylabel("-Imag [Ohm]")

        else:
            Exception("Not implemented!! choose either bode or complex")       


        axColeRT.invert_xaxis()
        axColeRT.set_xlabel("Frequency [Hz]")
        axColeRT.xaxis.set_ticks_position('none') 
        axColeRT.yaxis.set_ticks_position('none') 
        # axColeRT.legend(("Obs","Pred"), bbox_to_anchor=(1.25, 1.), fontsize = 10)
        axColeRT.hold (False)    
        ZarcFitWindow.radioButtonBodePlots.clicked.connect(ZarcFitWindow.updateRadiOutBodePlots)
        ZarcFitWindow.radioButtonComplexPlots.clicked.connect(ZarcFitWindow.updateRadiOutComplexPlots)


        axColeRB.invert_xaxis()                
        axColeRB.set_xlabel("Frequency [Hz]")
        axColeRB.xaxis.set_ticks_position('none') 
        axColeRB.yaxis.set_ticks_position('none')         

        axColeRB.hold (False)   


        figColebackground = figCole.canvas.copy_from_bbox(figCole.bbox)      
        

        ZarcFitWindow.figCole = figCole
        ZarcFitWindow.figColebackground = figColebackground
        ZarcFitWindow.axCole = axCole
        ZarcFitWindow.axColeRT = axColeRT
        ZarcFitWindow.axColeRB = axColeRB
        
        ZarcFitWindow.lineCole = lineCole
        ZarcFitWindow.lineColeRTpred = lineColeRTpred
        ZarcFitWindow.lineColeRBpred = lineColeRBpred        

        ZarcFitWindow.lineColeobs = lineColeobs
        ZarcFitWindow.lineColeRTobs = lineColeRTobs
        ZarcFitWindow.lineColeRBobs = lineColeRBobs  
              
    def addmplCole(ZarcFitWindow):
        ZarcFitWindow.canvas = FigureCanvas(ZarcFitWindow.figCole)
        ZarcFitWindow.mplCole.addWidget(ZarcFitWindow.canvas)
        ZarcFitWindow.canvas.draw()  
        ZarcFitWindow.toolbar = NavigationToolbar(ZarcFitWindow.canvas, ZarcFitWindow, coordinates=True)
        ZarcFitWindow.addToolBar(ZarcFitWindow.toolbar)   
        
    def updateFigs(ZarcFitWindow):   

        ZarcFitWindow.figCole.canvas.restore_region(ZarcFitWindow.figColebackground)         
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
        elif ZarcFitWindow.radioButtonParallel.isChecked():
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
        else:
            Exception("Not implemented!! choose either series or parallel")
        vminR, vmaxR = (np.r_[Z.real, ZarcFitWindow.obs.real]).min(), (np.r_[Z.real, ZarcFitWindow.obs.real]).max()
        vminI, vmaxI = (np.r_[-Z.imag, -ZarcFitWindow.obs.imag]).min(),(np.r_[-Z.imag, -ZarcFitWindow.obs.imag]).max() 
        
        ZarcFitWindow.lineCole.set_data(Z.real, -Z.imag)
        ZarcFitWindow.lineCole.axes.set_xlim(0., vmaxR*1.2)
        ZarcFitWindow.lineCole.axes.set_ylim(vminI, vmaxI*1.2)

        ZarcFitWindow.lineColeobs.set_data(ZarcFitWindow.obs.real, -ZarcFitWindow.obs.imag)
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.patch)        
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineCole)
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineColeobs)
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.get_yaxis())
        ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.get_xaxis())

        if ZarcFitWindow.radioButtonBodePlots.isChecked():

            zpredabs = abs(Z)
            zobsabs = abs(ZarcFitWindow.obs)
            ZarcFitWindow.lineColeRTpred.set_data(ZarcFitWindow.frequency, zpredabs)
            ZarcFitWindow.lineColeRTobs.set_data(ZarcFitWindow.frequency,zobsabs)
            zpredphase = abs(np.angle(Z, deg=True))
            zobsphase = abs(np.angle(ZarcFitWindow.obs, deg=True))
            ZarcFitWindow.lineColeRBpred.set_data(ZarcFitWindow.frequency, zpredphase)
            ZarcFitWindow.lineColeRBobs.set_data(ZarcFitWindow.frequency, zobsphase)            
            vminAbs, vmaxAbs = (np.r_[zpredabs, zobsabs]).min(), (np.r_[zpredabs, zobsabs]).max()
            vminPhase, vmaxPhase = (np.r_[zpredphase, zobsphase]).min(), (np.r_[zpredphase, zobsphase]).max()
            ZarcFitWindow.lineColeRTpred.axes.set_ylim(vminAbs*0.8, vmaxAbs*1.2)
            ZarcFitWindow.lineColeRBpred.axes.set_ylim(vminPhase*0.8, vmaxPhase*1.2)        
            ZarcFitWindow.lineColeRTpred.axes.set_ylabel("Total Impedance [Ohm]")
            ZarcFitWindow.lineColeRBpred.axes.set_ylabel("Phase [deg]")     

        elif ZarcFitWindow.radioButtonComplexPlots.isChecked():

            zpredreal = Z.real
            zobsreal = ZarcFitWindow.obs.real
            ZarcFitWindow.lineColeRTpred.set_data(ZarcFitWindow.frequency, zpredreal)
            ZarcFitWindow.lineColeRTobs.set_data(ZarcFitWindow.frequency,zobsreal)
            zpredimag = -Z.imag
            zobsimag = -ZarcFitWindow.obs.imag
            ZarcFitWindow.lineColeRBpred.set_data(ZarcFitWindow.frequency, zpredimag)
            ZarcFitWindow.lineColeRBobs.set_data(ZarcFitWindow.frequency, zobsimag)            
            ZarcFitWindow.lineColeRTpred.axes.set_ylim(vminR*0.8, vmaxR*1.2)
            ZarcFitWindow.lineColeRBpred.axes.set_ylim(vminI*0.8, vmaxI*11.2)   
            ZarcFitWindow.lineColeRTpred.axes.set_ylabel("Real [Ohm]")
            ZarcFitWindow.lineColeRBpred.axes.set_ylabel("-Imag [Ohm]")     
        else:
            Exception("Not implemented!! choose either bode or complex")               

        ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.patch)
        ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTpred)
        ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTobs)        
        ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.get_yaxis())
        ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.get_xaxis())
        
        
        ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.patch)
        ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBpred)        
        ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBobs)   
        ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.get_yaxis())
        ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.get_xaxis())
        
        ZarcFitWindow.figCole.canvas.update()
        

    #### Menus and Buttons ####
    # # # Files # # #
    def PickPath(ZarcFitWindow):
        ZarcFitWindow.PathPickerWindow.show()        
        # ZarcFitWindow.PathPickerWindow.exec_()        
    
    def getOBSFNAME(ZarcFitWindow):

        ZarcFitWindow.obsfname = []
        ZarcFitWindow.obsdata = []
        if ZarcFitWindow.PathPickerWindow.fnamestr:                
            os.chdir(ZarcFitWindow.PathPickerWindow.fnamestr)                
            # Read *.z file in the path
            for file in glob.glob("*.z"):
                ZarcFitWindow.obsfname.append(file) 
                tempobs = np.loadtxt(file, skiprows=11, delimiter=',')
                ZarcFitWindow.obsdata.append(tempobs)                
                # print (ZarcFitWindow.PathPickerWindow.fnamestr+ZarcFitWindow.filesep+ZarcFitWindow.filesep+file)

            ZarcFitWindow.obsfnamedirsize = len(ZarcFitWindow.obsfname)
            # Set maximum filenumber in ui 
            ZarcFitWindow.horizontalSliderObsFileNumber.setMaximum(ZarcFitWindow.obsfnamedirsize-1)


    def ReadObsFile(ZarcFitWindow, value):
        ZarcFitWindow.obs = ZarcFitWindow.obsdata[value][:,4]+ZarcFitWindow.obsdata[value][:,5]*1j
        ZarcFitWindow.frequency = ZarcFitWindow.obsdata[value][:,0]
        ZarcFitWindow.zarc.frequency = ZarcFitWindow.frequency
        ZarcFitWindow.updateFigs()               
        ZarcFitWindow.lineEditOBSFNAME.setText(ZarcFitWindow.obsfname[value]) 
        print (value, ZarcFitWindow.obsfname[value], ZarcFitWindow.lineEditPRMFNAME.text())

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