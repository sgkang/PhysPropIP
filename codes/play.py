# -*- coding: utf-8 -*-
"""
Created on Tue Feb 04 16:48:12 2014

@author: Christoph
"""

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from matplotlib import rcParams

import numpy as np
import scipy.constants as const
import sys

rcParams['font.size'] = 9


class MatplotlibWidget(Canvas):
    """
    MatplotlibWidget inherits PyQt4.QtGui.QWidget
    and matplotlib.backend_bases.FigureCanvasBase

    Options: option_name (default_value)
    -------    
    parent (None): parent widget
    title (''): figure title
    xlabel (''): X-axis label
    ylabel (''): Y-axis label
    xlim (None): X-axis limits ([min, max])
    ylim (None): Y-axis limits ([min, max])
    xscale ('linear'): X-axis scale
    yscale ('linear'): Y-axis scale
    width (4): width in inches
    height (3): height in inches
    dpi (100): resolution in dpi
    hold (False): if False, figure will be cleared each time plot is called

    Widget attributes:
    -----------------
    figure: instance of matplotlib.figure.Figure
    axes: figure axes

    Example:
    -------
    self.widget = MatplotlibWidget(self, yscale='log', hold=True)
    from numpy import linspace
    x = linspace(-10, 10)
    self.widget.axes.plot(x, x**2)
    self.wdiget.axes.plot(x, x**3)
    """
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=4, height=3, dpi=100, hold=False):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        if xscale is not None:
            self.axes.set_xscale(xscale)
        if yscale is not None:
            self.axes.set_yscale(yscale)
        if xlim is not None:
            self.axes.set_xlim(*xlim)
        if ylim is not None:
            self.axes.set_ylim(*ylim)
        self.axes.hold(hold)

        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtGui.QSize(w, h)

    def minimumSizeHint(self):
        return QtGui.QSize(10, 10)

def Zarcfun(Rx, Qx, px, freq):
    out = np.zeros_like(freq, dtype=np.complex128)
    out = 1./(1./Rx + Qx*(np.pi*2*freq*1j)**px)
    return out
    
class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        # Graphics Window
        self.mpl = MatplotlibWidget(self, title='Graph',
                                          xlabel='x',
                                          ylabel='y',
                                          hold=True)
        self.mpl.setGeometry(0,0,1300,800)
        self.setGeometry(0, 30, 1680, 800)

        # Slider Resistance
        title1=QtGui.QLabel(self)
        title1.setText('R')
        title1.move(1400,10)

        self.value1=QtGui.QLabel(self)
        self.value1.setText('1')
        self.value1.move(1550,40)

        cb=QtGui.QSlider(QtCore.Qt.Horizontal, self)
        cb.setGeometry(1400,40,100,30)
        cb.setMinimum(1)
        cb.setMaximum(10000)
        cb.valueChanged.connect(self.Rout)


        self.plot(1, self.mpl.axes)


    def Rout(self, position):
        self.value1.setText('%i' %position)
        self.plot(position, self.mpl.axes)

    def plot(self, R, axes):
        x = np.linspace(0, 1, 10)
        axes.plot(x, R*np.random.randn(10), 'r')



if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())