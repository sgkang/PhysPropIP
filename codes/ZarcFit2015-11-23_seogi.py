import numpy as np
import sys, glob, os, time
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
from ZarcfitCalculations import *
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
        # Create a push button labelled 'Return' and add it to our layout
        btn1 = QtGui.QPushButton('Return to main window', self)
        self.vbox.addWidget(btn1)        
        # Connect the clicked signal to the get_fname handler
        self.connect(btn1, QtCore.SIGNAL('clicked()'), self.close)
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
            self.ZarcFitWindow.getObsFName()
            with open(scriptPath+mysys.filesep+"ZarcFit.ini", "w") as ini_file:
                print(fname, file=ini_file)
        else:
            self.lbl.setText('No path selected')



class Main(QMainWindow, Ui_MainWindow):
    
    fwdtype = "series"
    plottype = "bode"
    axComplexReal = None
    axComplexImag = None
    ObsFName = None
    nfreq = None
    freqindlow = None
    freqindhigh = None
    frequencyorig = None
    obsorig = None
    t0 = None
    forcePlot = False

    def __init__(ZarcFitWindow, zarc, obs, frequency):
        
        ZarcFitWindow.zarc = zarc
        ZarcFitWindow.obs = obs
        ZarcFitWindow.obsorig = obs.copy()
        ZarcFitWindow.frequency = frequency
        ZarcFitWindow.frequencyorig = frequency.copy()
        ZarcFitWindow.nfreq = ZarcFitWindow.frequency.size
        ZarcFitWindow.freqindlow = 0
        ZarcFitWindow.freqindhigh = ZarcFitWindow.nfreq

        super(Main, ZarcFitWindow).__init__()

            
        ZarcFitWindow.setupUi(ZarcFitWindow)    
        ZarcFitWindow.t0 = time.time()     
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
        
        #Connect parameter sliders
        ZarcFitWindow.SliderLinf.valueChanged.connect(ZarcFitWindow.updateSldOutLinf)
        ZarcFitWindow.SldOutLinf.textChanged.connect(ZarcFitWindow.updateSliderLinf)
        ZarcFitWindow.SliderRinf.valueChanged.connect(ZarcFitWindow.updateSldOutRinf)
        ZarcFitWindow.SldOutRinf.textChanged.connect(ZarcFitWindow.updateSliderRinf)
        ZarcFitWindow.SliderRh.valueChanged.connect(ZarcFitWindow.updateSldOutRh)
        ZarcFitWindow.SldOutRh.textChanged.connect(ZarcFitWindow.updateSliderRh)
        ZarcFitWindow.SliderFh.valueChanged.connect(ZarcFitWindow.updateSldOutFh)
        ZarcFitWindow.SldOutFh.textChanged.connect(ZarcFitWindow.updateSliderFh)
        ZarcFitWindow.SliderPh.valueChanged.connect(ZarcFitWindow.updateSldOutPh)
        ZarcFitWindow.SldOutPh.textChanged.connect(ZarcFitWindow.updateSliderPh)
        ZarcFitWindow.SliderRm.valueChanged.connect(ZarcFitWindow.updateSldOutRm)
        ZarcFitWindow.SldOutRm.textChanged.connect(ZarcFitWindow.updateSliderRm)
        ZarcFitWindow.SliderFm.valueChanged.connect(ZarcFitWindow.updateSldOutFm)
        ZarcFitWindow.SldOutFm.textChanged.connect(ZarcFitWindow.updateSliderFm)
        ZarcFitWindow.SliderPm.valueChanged.connect(ZarcFitWindow.updateSldOutPm)
        ZarcFitWindow.SldOutPm.textChanged.connect(ZarcFitWindow.updateSliderPm)
        ZarcFitWindow.SliderRl.valueChanged.connect(ZarcFitWindow.updateSldOutRl)
        ZarcFitWindow.SldOutRl.textChanged.connect(ZarcFitWindow.updateSliderRl)
        ZarcFitWindow.SliderFl.valueChanged.connect(ZarcFitWindow.updateSldOutFl)
        ZarcFitWindow.SldOutFl.textChanged.connect(ZarcFitWindow.updateSliderFl)
        ZarcFitWindow.SliderPl.valueChanged.connect(ZarcFitWindow.updateSldOutPl)
        ZarcFitWindow.SldOutPl.textChanged.connect(ZarcFitWindow.updateSliderPl)
        ZarcFitWindow.SliderRe.valueChanged.connect(ZarcFitWindow.updateSldOutRe)
        ZarcFitWindow.SldOutRe.textChanged.connect(ZarcFitWindow.updateSliderRe)
        ZarcFitWindow.SliderQe.valueChanged.connect(ZarcFitWindow.updateSldOutQe)
        ZarcFitWindow.SldOutQe.textChanged.connect(ZarcFitWindow.updateSliderQe)
        ZarcFitWindow.SliderPef.valueChanged.connect(ZarcFitWindow.updateSldOutPef)
        ZarcFitWindow.SldOutPef.textChanged.connect(ZarcFitWindow.updateSliderPef)
        ZarcFitWindow.SliderPei.valueChanged.connect(ZarcFitWindow.updateSldOutPei)
        ZarcFitWindow.SldOutPei.textChanged.connect(ZarcFitWindow.updateSliderPei)                

        ZarcFitWindow.spinBoxHighFreq.valueChanged.connect(ZarcFitWindow.updateHighFreq)
        ZarcFitWindow.spinBoxLowFreq.valueChanged.connect(ZarcFitWindow.updateLowFreq)
        
        #Connect QRadiobutton
        ZarcFitWindow.radioButtonSerial.clicked.connect(ZarcFitWindow.updateRadiOutSerial)
        ZarcFitWindow.radioButtonParallel.clicked.connect(ZarcFitWindow.updateRadiOutParallel)        
        ZarcFitWindow.radioButtonBodePlots.clicked.connect(ZarcFitWindow.updateRadiOutBodePlots)
        ZarcFitWindow.radioButtonComplexPlots.clicked.connect(ZarcFitWindow.updateRadiOutComplexPlots)
        ZarcFitWindow.PathPickerWindow = PathPicker(ZarcFitWindow)
        
        ZarcFitWindow.spinBoxHighFreq.setValue(0)
        ZarcFitWindow.labelHighFreq.setText("{:,}".format(ZarcFitWindow.frequencyorig[0])+" Hz")
        ZarcFitWindow.spinBoxLowFreq.setValue(frequencyN-1)
        ZarcFitWindow.labelLowFreq.setText("{:,}".format(ZarcFitWindow.frequencyorig[-1])+" Hz")
        ZarcFitWindow.initializeFigure()
                        
    #### Matplotlib window ####
    def initializeFigure(ZarcFitWindow):
                
        hmlFreq = np.array([ZarcFitWindow.zarc.Fh,
                            ZarcFitWindow.zarc.Fm,
                            ZarcFitWindow.zarc.Fl,])

        figCole = plt.figure(figsize=(30,30), facecolor="white")        
        gs = gridspec.GridSpec(7, 7)        

        axCole = figCole.add_subplot(gs[:, :3])     #Left                
        axColeRT = figCole.add_subplot( gs[:3,4:])  #Right-Top
        axColeRB = figCole.add_subplot(gs[4:,4:])   #Right-Bottom        
        if ZarcFitWindow.radioButtonSerial.isChecked():
            Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
            Zhml = ZarcFitWindow.zarc.Zseries(hmlFreq) 
        elif ZarcFitWindow.radioButtonParallel.isChecked():
            Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
            Zhml = ZarcFitWindow.zarc.Zparallel(hmlFreq)              
        else:
            Exception("Not implemented!! choose either series or parallel")

        mergedZreal = np.append(np.concatenate((Z.real, obs.real)), 0.)
        mergedZimag = np.append(np.concatenate((-Z.imag, -obs.imag)), 0.)

        # Cole-Cole Plot: Real vs Imag
        lineColeZeroImag,= axCole.plot([min(mergedZreal), max(mergedZreal)], [0., 0.], 
             color='salmon', linewidth=1)                                
        lineColeZeroReal,= axCole.plot([0., 0.], [min(mergedZimag), max(mergedZimag)], 
             color='salmon', linewidth=1)   
        lineColeFh, =axCole.plot(Zhml[0].real, -Zhml[0].imag,
            color='red', marker='+', markersize=20, markeredgewidth=2)                                       
        lineColeFm, =axCole.plot(Zhml[1].real, -Zhml[1].imag,
            color='green', marker='+', markersize=20, markeredgewidth=2)                                       
        lineColeFl, =axCole.plot(Zhml[2].real, -Zhml[2].imag,
            color='blue', marker='+', markersize=20, markeredgewidth=2)                                              

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

            lineColeRTFh, =axColeRT.plot(ZarcFitWindow.zarc.Fh, abs(Zhml[0]),
                color='red', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRTFm, =axColeRT.plot(ZarcFitWindow.zarc.Fm, abs(Zhml[1]),
                color='green', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRTFl, =axColeRT.plot(ZarcFitWindow.zarc.Fl, abs(Zhml[2]),
                color='blue', marker='+', markersize=20, markeredgewidth=2)                                              
            lineColeRTobs, = axColeRT.loglog(frequency, abs(obs),
                color='green', marker='s', markersize=2, linewidth=1)
            lineColeRTpred, = axColeRT.loglog(frequency, abs(Z),
                color='cyan', marker='D', markersize=3, linewidth=2)    
                
            lineColeRBFh, =axColeRB.plot(ZarcFitWindow.zarc.Fh, abs(np.angle(Zhml[0], deg=True)),
                color='red', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRBFm, =axColeRB.plot(ZarcFitWindow.zarc.Fm, abs(np.angle(Zhml[1], deg=True)),
                color='green', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRBFl, =axColeRB.plot(ZarcFitWindow.zarc.Fl, abs(np.angle(Zhml[2], deg=True)),
                color='blue', marker='+', markersize=20, markeredgewidth=2)                                                             
            lineColeRBobs,= axColeRB.loglog(frequency, abs(np.angle(obs, deg=True)),
                color='green', marker='s', markersize=2, linewidth=1)    
            lineColeRBpred,= axColeRB.loglog(frequency, abs(np.angle(Z, deg=True)),
                color='cyan', marker='D', markersize=3, linewidth=2)    
            axColeRT.set_ylabel("Total Impedance [Ohm]")
            axColeRB.set_ylabel("abs(Phase) [deg]")

        elif ZarcFitWindow.radioButtonComplexPlots.isChecked():

            lineColeRTFh, =axColeRT.plot(ZarcFitWindow.zarc.Fh, Zhml[0].real,
                color='red', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRTFm, =axColeRT.plot(ZarcFitWindow.zarc.Fm, Zhml[1].real,
                color='green', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRTFl, =axColeRT.plot(ZarcFitWindow.zarc.Fl, Zhml[2].real,
                color='blue', marker='+', markersize=20, markeredgewidth=2)                                              
            lineColeRTobs, = axColeRT.loglog(frequency, obs.real,
                color='green', marker='s', markersize=2, linewidth=1)
            lineColeRTpred, = axColeRT.loglog(frequency, Z.real,
                color='cyan', marker='D', markersize=3, linewidth=2) 

                
            lineColeRBFh, =axColeRB.plot(ZarcFitWindow.zarc.Fh, abs(Zhml[0].imag),
                color='red', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRBFm, =axColeRB.plot(ZarcFitWindow.zarc.Fm, abs(Zhml[1].imag),
                color='green', marker='+', markersize=20, markeredgewidth=2)                                       
            lineColeRBFl, =axColeRB.plot(ZarcFitWindow.zarc.Fl, abs(Zhml[2].imag),
                color='blue', marker='+', markersize=20, markeredgewidth=2)                                                             
            lineColeRBobs,= axColeRB.loglog(frequency, abs(obs.imag),
                color='green', marker='s', markersize=2, linewidth=1)    
            lineColeRBpred,= axColeRB.loglog(frequency, abs(Z.imag),
                color='cyan', marker='D', markersize=3, linewidth=2)    
            axColeRT.set_ylabel("Real [Ohm]")
            axColeRB.set_ylabel("abs(Imag) [Ohm]")

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
 
        ZarcFitWindow.lineColeFh = lineColeFh 
        ZarcFitWindow.lineColeFm = lineColeFm 
        ZarcFitWindow.lineColeFl = lineColeFl             

        ZarcFitWindow.lineColeRTFh = lineColeRTFh 
        ZarcFitWindow.lineColeRTFm = lineColeRTFm 
        ZarcFitWindow.lineColeRTFl = lineColeRTFl 
        
        ZarcFitWindow.lineColeRBFh = lineColeRBFh 
        ZarcFitWindow.lineColeRBFm = lineColeRBFm 
        ZarcFitWindow.lineColeRBFl = lineColeRBFl         
       
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
        ZarcFitWindow.t1 = time.time()
        elapsedTime = ZarcFitWindow.t1-ZarcFitWindow.t0
        if elapsedTime > 0.1 or ZarcFitWindow.forcePlot:
            ZarcFitWindow.t0 = ZarcFitWindow.t1
            ZarcFitWindow.forcePlot = False
        
            hmlFreq = np.array([ZarcFitWindow.zarc.Fh,
                                ZarcFitWindow.zarc.Fm,
                                ZarcFitWindow.zarc.Fl,])

            ZarcFitWindow.figCole.canvas.restore_region(ZarcFitWindow.figColebackground)         
            if ZarcFitWindow.radioButtonSerial.isChecked():
                Z = ZarcFitWindow.zarc.Zseries(ZarcFitWindow.frequency)  
                Zhml = ZarcFitWindow.zarc.Zseries(hmlFreq) 
            elif ZarcFitWindow.radioButtonParallel.isChecked():
                Z = ZarcFitWindow.zarc.Zparallel(ZarcFitWindow.frequency)  
                Zhml = ZarcFitWindow.zarc.Zparallel(hmlFreq) 
            else:
                Exception("Not implemented!! choose either series or parallel")
            vminR, vmaxR = (np.r_[Z.real, ZarcFitWindow.obs.real]).min(), (np.r_[Z.real, ZarcFitWindow.obs.real]).max()
            vminI, vmaxI = (np.r_[-Z.imag, -ZarcFitWindow.obs.imag]).min(),(np.r_[-Z.imag, -ZarcFitWindow.obs.imag]).max() 
            
            ZarcFitWindow.lineCole.set_data(Z.real, -Z.imag)
            ZarcFitWindow.lineCole.axes.set_xlim(0., vmaxR*1.2)
            ZarcFitWindow.lineCole.axes.set_ylim(vminI, vmaxI*1.2)

            ZarcFitWindow.lineColeFh.set_data(Zhml[0].real, -Zhml[0].imag)
            ZarcFitWindow.lineColeFm.set_data(Zhml[1].real, -Zhml[1].imag)
            ZarcFitWindow.lineColeFl.set_data(Zhml[2].real, -Zhml[2].imag)

            ZarcFitWindow.lineColeobs.set_data(ZarcFitWindow.obs.real, -ZarcFitWindow.obs.imag)
            ZarcFitWindow.figCole.draw_artist(ZarcFitWindow.figCole.patch)                
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.patch)        
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.get_yaxis())
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.get_xaxis())
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineColeFh)
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineColeFm)
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineColeFl)
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineCole)
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.lineColeobs)

            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.spines['left'])
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.spines['right'])
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.spines['bottom'])
            ZarcFitWindow.axCole.draw_artist(ZarcFitWindow.axCole.spines['top'])


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
                ZarcFitWindow.lineColeRBpred.axes.set_ylabel("abs(Phase) [deg]")     

                ZarcFitWindow.lineColeRTFh.set_data(ZarcFitWindow.zarc.Fh, abs(Zhml[0]))
                ZarcFitWindow.lineColeRTFm.set_data(ZarcFitWindow.zarc.Fm, abs(Zhml[1]))
                ZarcFitWindow.lineColeRTFl.set_data(ZarcFitWindow.zarc.Fl, abs(Zhml[2]))
                ZarcFitWindow.lineColeRBFh.set_data(ZarcFitWindow.zarc.Fh, abs(np.angle(Zhml[0], deg=True) ))
                ZarcFitWindow.lineColeRBFm.set_data(ZarcFitWindow.zarc.Fm, abs(np.angle(Zhml[1], deg=True) ))
                ZarcFitWindow.lineColeRBFl.set_data(ZarcFitWindow.zarc.Fl, abs(np.angle(Zhml[2], deg=True) ))            

            elif ZarcFitWindow.radioButtonComplexPlots.isChecked():

                zpredreal = Z.real
                zobsreal = ZarcFitWindow.obs.real
                ZarcFitWindow.lineColeRTpred.set_data(ZarcFitWindow.frequency, zpredreal)
                ZarcFitWindow.lineColeRTobs.set_data(ZarcFitWindow.frequency, zobsreal)
                zpredimag = -Z.imag
                zobsimag = -ZarcFitWindow.obs.imag
                ZarcFitWindow.lineColeRBpred.set_data(ZarcFitWindow.frequency, zpredimag)
                ZarcFitWindow.lineColeRBobs.set_data(ZarcFitWindow.frequency, zobsimag)            
                ZarcFitWindow.lineColeRTpred.axes.set_ylim(vminR*0.8, vmaxR*1.2)
                ZarcFitWindow.lineColeRBpred.axes.set_ylim(vminI*0.8, vmaxI*11.2)   
                ZarcFitWindow.lineColeRTpred.axes.set_ylabel("Real [Ohm]")
                ZarcFitWindow.lineColeRBpred.axes.set_ylabel("abs(Imag) [Ohm]")    

                ZarcFitWindow.lineColeRTFh.set_data(ZarcFitWindow.zarc.Fh, Zhml[0].real)
                ZarcFitWindow.lineColeRTFm.set_data(ZarcFitWindow.zarc.Fm, Zhml[1].real)
                ZarcFitWindow.lineColeRTFl.set_data(ZarcFitWindow.zarc.Fl, Zhml[2].real)
                ZarcFitWindow.lineColeRBFh.set_data(ZarcFitWindow.zarc.Fh, abs(Zhml[0].imag))
                ZarcFitWindow.lineColeRBFm.set_data(ZarcFitWindow.zarc.Fm, abs(Zhml[1].imag))
                ZarcFitWindow.lineColeRBFl.set_data(ZarcFitWindow.zarc.Fl, abs(Zhml[2].imag))

            else:
                Exception("Not implemented!! choose either bode or complex")               


            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.patch)
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.get_yaxis())
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.get_xaxis())
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.spines['left'])
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.spines['right'])
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.spines['bottom'])
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.axColeRT.spines['top'])
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTFh)
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTFm)       
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTFl)
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTpred)
            ZarcFitWindow.axColeRT.draw_artist(ZarcFitWindow.lineColeRTobs)        
           
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.patch)
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.get_yaxis())
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.get_xaxis())
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.spines['left'])
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.spines['right'])
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.spines['bottom'])
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.axColeRB.spines['top'])        
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBFh)
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBFm)
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBFl)
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBpred)        
            ZarcFitWindow.axColeRB.draw_artist(ZarcFitWindow.lineColeRBobs)   

            ZarcFitWindow.figCole.canvas.update()
        

    #### Menus and Buttons ####
    # # # Files # # #
    def PickPath(ZarcFitWindow):
        ZarcFitWindow.PathPickerWindow.show()        
        # ZarcFitWindow.PathPickerWindow.exec_()        
    
    def getObsFName(ZarcFitWindow):

        ZarcFitWindow.ObsFName = []
        ZarcFitWindow.obsdata = []
        if ZarcFitWindow.PathPickerWindow.fnamestr:                
            os.chdir(ZarcFitWindow.PathPickerWindow.fnamestr)                
            # Read *.z file in the path
            for file in glob.glob("*.z"):
                ZarcFitWindow.ObsFName.append(file) 
                tempobs = np.loadtxt(file, skiprows=11, delimiter=',')
                ZarcFitWindow.obsdata.append(tempobs)                
                # print (ZarcFitWindow.PathPickerWindow.fnamestr+ZarcFitWindow.filesep+ZarcFitWindow.filesep+file)

            ZarcFitWindow.ObsFNamedirsize = len(ZarcFitWindow.ObsFName)
            # Set maximum filenumber in ui 
            ZarcFitWindow.horizontalSliderObsFileNumber.setMaximum(ZarcFitWindow.ObsFNamedirsize-1)
            ZarcFitWindow.spinBoxObsFileNumber.setMaximum(ZarcFitWindow.ObsFNamedirsize-1)
            ZarcFitWindow.label_LastFile.setText(str(ZarcFitWindow.ObsFNamedirsize-1))


    def ReadObsFile(ZarcFitWindow, value):
        ZarcFitWindow.obs = ZarcFitWindow.obsdata[value][:,4]+ZarcFitWindow.obsdata[value][:,5]*1j
        ZarcFitWindow.obsorig = ZarcFitWindow.obsorig.copy()
        ZarcFitWindow.frequency = ZarcFitWindow.obsdata[value][:,0]
        ZarcFitWindow.frequencyorig = ZarcFitWindow.frequency.copy()
        ZarcFitWindow.nfreq = ZarcFitWindow.frequency.size
        ZarcFitWindow.freqindlow = 0
        ZarcFitWindow.freqindhigh = ZarcFitWindow.nfreq                
        # ZarcFitWindow.zarc.frequency = ZarcFitWindow.frequency
        ZarcFitWindow.updateFigs()               
        ZarcFitWindow.lineEditObsFName.setText(ZarcFitWindow.ObsFName[value])         
        # print (value, ZarcFitWindow.ObsFName[value], ZarcFitWindow.lineEditPRMFNAME.text())

    def SelectParameterFile(ZarcFitWindow):
        print ("SelectParameterFile")

    def SelectObsFileType(ZarcFitWindow):
        print ("SelectObsFileType")

    def NextObsFile(ZarcFitWindow):
        ZarcFitWindow.spinBoxObsFileNumber.setValue(ZarcFitWindow.spinBoxObsFileNumber.value() + 1)

    def PrevObsFile(ZarcFitWindow):
        ZarcFitWindow.spinBoxObsFileNumber.setValue(ZarcFitWindow.spinBoxObsFileNumber.value() - 1)

    # # # Fits # # #
    def updateHighFreq(ZarcFitWindow, value):
        ZarcFitWindow.spinBoxHighFreq.setValue(value)
        ZarcFitWindow.labelHighFreq.setText("{:,}".format(ZarcFitWindow.frequencyorig[value])+" Hz")        
        ZarcFitWindow.freqindlow = value
        ZarcFitWindow.frequency = ZarcFitWindow.frequencyorig[ZarcFitWindow.freqindlow:ZarcFitWindow.freqindhigh]
        ZarcFitWindow.obs = ZarcFitWindow.obsorig[ZarcFitWindow.freqindlow:ZarcFitWindow.freqindhigh]
        #choose frequencies and set limits for plots
        ZarcFitWindow.updateFigs()

    def updateLowFreq(ZarcFitWindow, value):
        ZarcFitWindow.spinBoxLowFreq.setValue(value)
        ZarcFitWindow.labelLowFreq.setText("{:,}".format(ZarcFitWindow.frequencyorig[value])+" Hz")        
        ZarcFitWindow.freqindhigh = value+1        
        ZarcFitWindow.frequency = ZarcFitWindow.frequencyorig[ZarcFitWindow.freqindlow:ZarcFitWindow.freqindhigh]        
        ZarcFitWindow.obs = ZarcFitWindow.obsorig[ZarcFitWindow.freqindlow:ZarcFitWindow.freqindhigh]
        
        #choose frequencies and set limits for plots
        ZarcFitWindow.updateFigs()
       
    def AllFreqs(ZarcFitWindow):
        print ("AllFreqs")
        
    def ReadParameters(ZarcFitWindow):
        print ("ReadParameters")
        
    def DefaultStartModel(ZarcFitWindow):
        ZarcFitWindow.zarc.Linf, ZarcFitWindow.zarc.Rinf, ZarcFitWindow.zarc.Rh, ZarcFitWindow.zarc.Fh, \
            ZarcFitWindow.zarc.Ph, ZarcFitWindow.zarc.Rl, ZarcFitWindow.zarc.Fl, ZarcFitWindow.zarc.Pl, \
            ZarcFitWindow.zarc.Rm, ZarcFitWindow.zarc.Fm, ZarcFitWindow.zarc.Pm, ZarcFitWindow.zarc.Re, \
            ZarcFitWindow.zarc.Qe, ZarcFitWindow.zarc.Pef, ZarcFitWindow.zarc.Pei = SetDefaultParameters()
        ZarcFitWindow.SldOutLinf.setText("{:.2E}".format(ZarcFitWindow.zarc.Linf))
        ZarcFitWindow.SldOutRinf.setText("{:.2E}".format(ZarcFitWindow.zarc.Rinf))
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(ZarcFitWindow.zarc.Rh))
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(ZarcFitWindow.zarc.Fh))
        ZarcFitWindow.SldOutPh.setText("{:.3f}".format(ZarcFitWindow.zarc.Ph))
        ZarcFitWindow.SldOutRm.setText("{:.2E}".format(ZarcFitWindow.zarc.Rm))
        ZarcFitWindow.SldOutFm.setText("{:.2E}".format(ZarcFitWindow.zarc.Fm))
        ZarcFitWindow.SldOutPm.setText("{:.3f}".format(ZarcFitWindow.zarc.Pm))
        ZarcFitWindow.SldOutRl.setText("{:.2E}".format(ZarcFitWindow.zarc.Rl))
        ZarcFitWindow.SldOutFl.setText("{:.2E}".format(ZarcFitWindow.zarc.Fl))
        ZarcFitWindow.SldOutPl.setText("{:.3f}".format(ZarcFitWindow.zarc.Pl))
        ZarcFitWindow.SldOutRe.setText("{:.2E}".format(ZarcFitWindow.zarc.Re))
        ZarcFitWindow.SldOutQe.setText("{:.2E}".format(ZarcFitWindow.zarc.Qe))
        ZarcFitWindow.SldOutPef.setText("{:.3f}".format(ZarcFitWindow.zarc.Pef))
        ZarcFitWindow.SldOutPei.setText("{:.3f}".format(ZarcFitWindow.zarc.Pei))
        ZarcFitWindow.forcePlot = True
        ZarcFitWindow.updateFigs()        
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
        # ZarcFitWindow.updateFigs() 
        
    def updateSliderLinf(ZarcFitWindow, value):
        Linf = float(value)
        ZarcFitWindow.SliderLinf.setValue(int(np.log10(Linf)*1000.))
        ZarcFitWindow.zarc.Linf = Linf
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutRinf(ZarcFitWindow, value):
        Rinf = 10**(value/1000.)
        ZarcFitWindow.SldOutRinf.setText("{:.2E}".format(Rinf))
        ZarcFitWindow.zarc.Rinf = Rinf
        # ZarcFitWindow.updateFigs() 

    def updateSliderRinf(ZarcFitWindow, value):
        Rinf = float(value)
        ZarcFitWindow.SliderRinf.setValue(int(np.log10(Rinf)*1000.))
        ZarcFitWindow.zarc.Rinf = Rinf
        ZarcFitWindow.updateFigs() 
    
    def updateSldOutRh(ZarcFitWindow, value):
        Rh = 10**(value/1000.)
        ZarcFitWindow.SldOutRh.setText("{:.2E}".format(Rh))
        ZarcFitWindow.zarc.Rh = Rh
        # ZarcFitWindow.updateFigs()                 


    def updateSliderRh(ZarcFitWindow, value):
        Rh = float(value)
        ZarcFitWindow.SliderRh.setValue(int(np.log10(Rh)*1000.))
        ZarcFitWindow.zarc.Rh = Rh
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutFh(ZarcFitWindow, value):
        Fh = 10**(value/1000.)
        ZarcFitWindow.SldOutFh.setText("{:.2E}".format(Fh))
        ZarcFitWindow.zarc.Fh = Fh
        # ZarcFitWindow.updateFigs() 

    def updateSliderFh(ZarcFitWindow, value):
        Fh = float(value)
        ZarcFitWindow.SliderFh.setValue(int(np.log10(Fh)*1000.))
        ZarcFitWindow.zarc.Fh = Fh
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutPh(ZarcFitWindow, value):
        Ph = value/1000.
        ZarcFitWindow.SldOutPh.setText("{:.3f}".format(Ph))
        ZarcFitWindow.zarc.Ph = Ph
        # ZarcFitWindow.updateFigs() 
        
    def updateSliderPh(ZarcFitWindow, value):
        Ph = float(value)
        ZarcFitWindow.SliderPh.setValue(Ph*1000)
        ZarcFitWindow.zarc.Ph = Ph
        ZarcFitWindow.updateFigs() 

    def updateSldOutRm(ZarcFitWindow, value):
        Rm = 10**(value/1000.)
        ZarcFitWindow.SldOutRm.setText("{:.2E}".format(Rm))
        ZarcFitWindow.zarc.Rm = Rm
        # ZarcFitWindow.updateFigs() 

    def updateSliderRm(ZarcFitWindow, value):
        Rm = float(value)
        ZarcFitWindow.SliderRm.setValue(int(np.log10(Rm)*1000.))
        ZarcFitWindow.zarc.Rm = Rm
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutFm(ZarcFitWindow, value):
        Fm = 10**(value/1000.)
        ZarcFitWindow.SldOutFm.setText("{:.2E}".format(Fm))
        ZarcFitWindow.zarc.Fm = Fm
        # ZarcFitWindow.updateFigs() 

    def updateSliderFm(ZarcFitWindow, value):
        Fm = float(value)
        ZarcFitWindow.SliderFm.setValue(int(np.log10(Fm)*1000.))
        ZarcFitWindow.zarc.Fm = Fm
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutPm(ZarcFitWindow, value):
        Pm = value/1000.
        ZarcFitWindow.SldOutPm.setText("{:.3f}".format(Pm))
        ZarcFitWindow.zarc.Pm = Pm
        # ZarcFitWindow.updateFigs() 
        
    def updateSliderPm(ZarcFitWindow, value):
        Pm = float(value)
        ZarcFitWindow.SliderPm.setValue(Pm*1000)
        ZarcFitWindow.zarc.Pm = Pm
        ZarcFitWindow.updateFigs() 

    def updateSldOutRl(ZarcFitWindow, value):
        Rl = 10**(value/1000.)
        ZarcFitWindow.SldOutRl.setText("{:.2E}".format(Rl))
        ZarcFitWindow.zarc.Rl = Rl
        # ZarcFitWindow.updateFigs() 

    def updateSliderRl(ZarcFitWindow, value):
        Rl = float(value)
        ZarcFitWindow.SliderRl.setValue(int(np.log10(Rl)*1000.))
        ZarcFitWindow.zarc.Rl = Rl
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutFl(ZarcFitWindow, value):
        Fl = 10**(value/1000.)
        ZarcFitWindow.SldOutFl.setText("{:.2E}".format(Fl))
        ZarcFitWindow.zarc.Fl = Fl
        # ZarcFitWindow.updateFigs() 
        
    def updateSliderFl(ZarcFitWindow, value):
        Fl = float(value)
        ZarcFitWindow.SliderFl.setValue(int(np.log10(Fl)*1000.))
        ZarcFitWindow.zarc.Fl = Fl
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutPl(ZarcFitWindow, value):
        Pl = value/1000.
        ZarcFitWindow.SldOutPl.setText("{:.3f}".format(Pl))
        ZarcFitWindow.zarc.Pl = Pl
        # ZarcFitWindow.updateFigs() 

    def updateSliderPl(ZarcFitWindow, value):
        Pl = float(value)
        ZarcFitWindow.SliderPl.setValue(Pl*1000)
        ZarcFitWindow.zarc.Pl = Pl
        ZarcFitWindow.updateFigs() 

    def updateSldOutRe(ZarcFitWindow, value):
        Re = 10**(value/1000.)
        ZarcFitWindow.SldOutRe.setText("{:.2E}".format(Re))
        ZarcFitWindow.zarc.Re = Re
        # ZarcFitWindow.updateFigs() 

    def updateSliderRe(ZarcFitWindow, value):
        Re = float(value)
        ZarcFitWindow.SliderRe.setValue(int(np.log10(Re)*1000.))
        ZarcFitWindow.zarc.Re = Re
        # ZarcFitWindow.updateFigs() 
        
    def updateSldOutQe(ZarcFitWindow, value):
        Qe = 10**(value/1000.)
        ZarcFitWindow.SldOutQe.setText("{:.2E}".format(Qe))
        ZarcFitWindow.zarc.Qe = Qe
        # ZarcFitWindow.updateFigs() 

    def updateSliderQe(ZarcFitWindow, value):
        Qe = float(value)
        ZarcFitWindow.SliderQe.setValue(int(np.log10(Qe)*1000.))
        ZarcFitWindow.zarc.Qe = Qe
        ZarcFitWindow.updateFigs() 
        
    def updateSldOutPef(ZarcFitWindow, value):
        Pef = value/1000.
        ZarcFitWindow.SldOutPef.setText("{:.3f}".format(Pef))
        ZarcFitWindow.zarc.Pef = Pef
        # ZarcFitWindow.updateFigs() 

    def updateSliderPef(ZarcFitWindow, value):
        Pef = float(value)
        ZarcFitWindow.SliderPef.setValue(Pef*1000)
        ZarcFitWindow.zarc.Pef = Pef
        ZarcFitWindow.updateFigs() 

    def updateSldOutPei(ZarcFitWindow, value):
        Pei = value/1000.
        ZarcFitWindow.SldOutPei.setText("{:.3f}".format(Pei))
        ZarcFitWindow.zarc.Pei = Pei
        # ZarcFitWindow.updateFigs() 

    def updateSliderPei(ZarcFitWindow, value):
        Pei = float(value)
        ZarcFitWindow.SliderPei.setValue(Pei*1000)
        ZarcFitWindow.zarc.Pei = Pei
        ZarcFitWindow.updateFigs() 
       
        

def SetDefaultParameters():
    
    Linf = 1.E-4
    Rinf = 1.E4
    Rh = 1.E5
    Fh = 1e5
    Ph = 0.8
    Rm = 1e-1
    Fm = 1e-1
    Pm = 0.5        
    Rl = 1.E4
    Fl = 1.e1
    Pl = 0.5    
    Re = 1.E10
    Qe = 1.E-4
    Pef = 0.5
    Pei = 0.05    

    return  Linf, Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei

############################################################################### 
############################################################################### 
from whichsystem import whichsystem
if __name__ == '__main__':

    mysys = whichsystem()
    mysys.run()
    scriptPath = os.getcwd()    
    with open(scriptPath+mysys.filesep+"ZarcFit.ini", "r") as ini_file:        
        path = ini_file.read()
    print(path)    
    # ZarcFitWindow.PathPickerWindow.fnamestr = path
    # ZarcFitWindow.lineEditPath.setText(path)
    # ZarcFitWindow.getObsFName()       
    path = "../data/HVC2014_10Grenon/"
    fnameobs = "BC13867-A 2014-10-23.z"
    pathobs = path+fnameobs
    temp = np.loadtxt(pathobs, skiprows=11, delimiter=",")
    obs = temp[:,4]+1j*temp[:,5]
    frequencyAll = temp[:,0].copy()
    frequencyN = len (frequencyAll)
    print (frequencyN, frequencyAll[0],frequencyAll[frequencyN-1],)
    frequency = frequencyAll
    zarc = ZarcfitCalculations(obs, frequency)
    Linf, Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei = SetDefaultParameters()
    zarc.SetParametersSeries(Linf, Rinf, Rh, Fh, Ph, Rl, Fl, Pl, Rm, Fm, Pm, Re, Qe, Pef, Pei)     
    app = QtGui.QApplication(sys.argv)
    main = Main(zarc, obs, frequency)
    main.addmplCole()
    main.show()
    sys.exit(app.exec_())   