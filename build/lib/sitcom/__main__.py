

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.patches as pa
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
import glob,os,cv2,platform
import time,sys,site,shutil
import sitcom.sirgraf as sf

from astropy.io import fits
from astropy.visualization import ZScaleInterval

if platform.system()=='Windows':
    import moviepy.editor as mpe

mp.use('Qt5Agg')
mp.rcParams['font.family'] = 'monospace'

from sitcom.st1 import Ui_SecondWindow

conda_env=os.environ.get('CONDA_DEFAULT_ENV')
site_packages_path=None
if conda_env:
    cnpath=os.path.join(os.environ['CONDA_PREFIX'],'lib','python{}'.format(sys.version[:3]),'site-packages')
    if os.path.exists(cnpath):
        site_packages_path = cnpath
else:
    site_packages_path = site.getusersitepackages()
ft=os.path.join(site_packages_path,'cv2/qt/plugins')
if os.path.exists(ft):
    shutil.rmtree(ft)
    #gc.collect()
    if os.path.exists(ft):
        os.rmdir(ft)
else:
    pass


import warnings
warnings.filterwarnings("ignore")
class Load_Window(QtWidgets.QSplashScreen):
    def __init__(self, movie, parent=None):
        movie.jumpToFrame(0)
        pixmap = QtGui.QPixmap(movie.frameRect().size())

        QtWidgets.QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)
class Ui_MainWindow(object):     
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedWidth(1000)
        MainWindow.setFixedHeight(550)
        conda_env=os.environ.get('CONDA_DEFAULT_ENV')
        site_packages_path=None
        if conda_env:
              cnpath=os.path.join(os.environ['CONDA_PREFIX'],'lib','python{}'.format(sys.version[:3]),'site-packages')
              if os.path.exists(cnpath):
                 site_packages_path = cnpath
        else:
              site_packages_path = site.getusersitepackages()
        self.sitep=site_packages_path
        icon = QtGui.QIcon()
        ci=os.path.join(self.sitep,'sitcom/icon/cme.png')
        icon.addPixmap(QtGui.QPixmap(ci), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(40, 30))
        QtGui.QFontDatabase.removeAllApplicationFonts()
        cf=os.path.join(self.sitep,'sitcom/font/lato/Lato-Semibold.ttf')
        QtGui.QFontDatabase.addApplicationFont(cf)
        font = QtGui.QFont('Lato-SemiBold', 10)
        
        font.setWeight(50)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #########################################################
        self.Browse = QtWidgets.QPushButton(self.centralwidget)
        self.Browse.setGeometry(QtCore.QRect(330, 10, 89, 31))
        self.Browse.setObjectName("Browse")
        self.Browse_le = QtWidgets.QLineEdit(self.centralwidget)
        self.Browse_le.setGeometry(QtCore.QRect(10, 10, 301, 31))
        self.Browse_le.setObjectName("Browse_le")
        ##########################################################
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(150, 80, 118, 21))
        self.progressBar.setObjectName("progressBar")
        self.Success = QtWidgets.QLabel(self.centralwidget)
        self.Success.setGeometry(QtCore.QRect(280, 80, 71, 21))
        self.Success.setObjectName("Success")
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        self.Start.setGeometry(QtCore.QRect(50, 80, 71, 21))
        self.Start.setObjectName("Start")
        self.Start.clicked.connect(self.fStart)
        ##########################################################
        self.intensity = QtWidgets.QLabel(self.centralwidget)
        self.intensity.setGeometry(QtCore.QRect(50, 230, 111, 21))
        self.intensity.setObjectName("intensity")
        self.comboBox_scale = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_scale.setGeometry(QtCore.QRect(170, 230, 121, 25))
        self.comboBox_scale.setObjectName("comboBox_scale")
        self.comboBox_scale.addItem("")
        self.comboBox_scale.addItem("")
        self.comboBox_scale.addItem("")
        self.comboBox_scale.addItem("")
        ##########################################################
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(426, 0, 20, 791))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        ##########################################################
        self.groupBox_image = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_image.setGeometry(QtCore.QRect(10, 100, 411, 131))
        self.groupBox_image.setObjectName("groupBox_image")
        self.Movie = QtWidgets.QPushButton(self.groupBox_image)
        self.Movie.setGeometry(QtCore.QRect(220, 100, 181, 21))
        self.Movie.setObjectName("Movie")
        self.Minimum = QtWidgets.QPushButton(self.groupBox_image)
        self.Minimum.setGeometry(QtCore.QRect(220, 40, 181, 21))
        self.Minimum.setObjectName("Minimum")
        self.Final = QtWidgets.QPushButton(self.groupBox_image)
        self.Final.setGeometry(QtCore.QRect(20, 100, 181, 21))
        self.Final.setObjectName("Final")
        self.Uniform = QtWidgets.QPushButton(self.groupBox_image)
        self.Uniform.setGeometry(QtCore.QRect(20, 40, 181, 21))
        self.Uniform.setObjectName("Uniform")
        self.Filtered = QtWidgets.QPushButton(self.groupBox_image)
        self.Filtered.setGeometry(QtCore.QRect(20, 70, 181, 21))
        self.Filtered.setObjectName("Filtered")
        self.Average = QtWidgets.QPushButton(self.groupBox_image)
        self.Average.setGeometry(QtCore.QRect(220, 70, 181, 21))
        self.Average.setObjectName("Average")
        self.groupBox_image.setStyleSheet("QGroupBox#groupBox_image {border:0;}")
        ##########################################################
        self.groupBox_scale = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_scale.setGeometry(QtCore.QRect(30, 240, 341, 111))
        self.groupBox_scale.setObjectName("groupBox_scale")
        self.label_max = QtWidgets.QLabel(self.groupBox_scale)
        self.label_max.setGeometry(QtCore.QRect(120, 90, 161, 17))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.label_max.setFont(font)
        self.label_max.setObjectName("label_max")
        self.Max = QtWidgets.QLabel(self.groupBox_scale)
        self.Max.setGeometry(QtCore.QRect(20, 70, 71, 20))
        self.Max.setObjectName("Max")
        self.MinSlider = QtWidgets.QSlider(self.groupBox_scale)
        self.MinSlider.setGeometry(QtCore.QRect(120, 30, 151, 20))
        self.MinSlider.setMaximum(4)
        self.MinSlider.setOrientation(QtCore.Qt.Horizontal)
        self.MinSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.MinSlider.setObjectName("MinSlider")
        self.Min = QtWidgets.QLabel(self.groupBox_scale)
        self.Min.setGeometry(QtCore.QRect(20, 30, 71, 20))
        self.Min.setObjectName("Min")
        self.MaxSlider = QtWidgets.QSlider(self.groupBox_scale)
        self.MaxSlider.setGeometry(QtCore.QRect(120, 70, 151, 20))
        self.MaxSlider.setMaximum(4)
        self.MaxSlider.setOrientation(QtCore.Qt.Horizontal)
        self.MaxSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.MaxSlider.setObjectName("MaxSlider")
        self.label_min = QtWidgets.QLabel(self.groupBox_scale)
        self.label_min.setGeometry(QtCore.QRect(120, 50, 161, 17))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.label_min.setFont(font)
        self.label_min.setObjectName("label_min")
        self.Ok1 = QtWidgets.QPushButton(self.groupBox_scale)
        self.Ok1.setGeometry(QtCore.QRect(290, 50, 41, 25))
        self.groupBox_scale.setStyleSheet("QGroupBox#groupBox_scale {border:0;}")
        self.groupBox_scale.hide()
        ##########################################################
        self.groupBox_scale_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_scale_2.setGeometry(QtCore.QRect(30, 240, 341, 111))
        self.groupBox_scale_2.setObjectName("groupBox_scale_2")
        self.GammaSlider = QtWidgets.QSlider(self.groupBox_scale_2)
        self.GammaSlider.setGeometry(QtCore.QRect(120, 50, 151, 20))
        self.GammaSlider.setMaximum(4)
        self.GammaSlider.setRange(0, 4)
        self.GammaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.GammaSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.GammaSlider.setObjectName("MinSlider_2")
        self.gamma = QtWidgets.QLabel(self.groupBox_scale_2)
        self.gamma.setGeometry(QtCore.QRect(20, 50, 71, 20))
        self.gamma.setObjectName("Min_2")
        self.label_gamma = QtWidgets.QLabel(self.groupBox_scale_2)
        self.label_gamma.setGeometry(QtCore.QRect(120, 70, 161, 17))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(12)
        self.label_gamma.setFont(font)
        self.label_gamma.setObjectName("label_min_2")
        self.Ok2 = QtWidgets.QPushButton(self.groupBox_scale_2)
        self.Ok2.setGeometry(QtCore.QRect(290, 50, 41, 25))
        self.groupBox_scale_2.setStyleSheet("QGroupBox#groupBox_scale_2 {border:0;}")
        self.groupBox_scale_2.hide()
        ##########################################################
        self.groupBox_save = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_save.setGeometry(QtCore.QRect(20, 350, 411, 101))
        self.groupBox_save.setObjectName("groupBox_save")
        self.frate = QtWidgets.QLabel(self.groupBox_save)
        self.frate.setGeometry(QtCore.QRect(0, 70, 91, 17))
        self.frate.setObjectName("frate")
        self.label_sav = QtWidgets.QLabel(self.groupBox_save)
        self.label_sav.setGeometry(QtCore.QRect(0, 30, 101, 20))
        self.label_sav.setObjectName("label_sav")
        self.File_le = QtWidgets.QLineEdit(self.groupBox_save)
        self.File_le.setGeometry(QtCore.QRect(230, 70, 113, 20))
        self.File_le.setObjectName("File_le")
        self.Save_ok = QtWidgets.QPushButton(self.groupBox_save)
        self.Save_ok.setGeometry(QtCore.QRect(210, 30, 41, 25))
        self.Save_ok.setObjectName("Save_ok")
        self.label_sav_done = QtWidgets.QLabel(self.groupBox_save)
        self.label_sav_done.setGeometry(QtCore.QRect(320, 30, 61, 21))
        self.label_sav_done.setObjectName("label_sav_done")
        self.comboBox_save = QtWidgets.QComboBox(self.groupBox_save)
        self.comboBox_save.setGeometry(QtCore.QRect(110, 30, 86, 25))
        self.comboBox_save.setObjectName("comboBox_save")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.Filen = QtWidgets.QLabel(self.groupBox_save)
        self.Filen.setGeometry(QtCore.QRect(150, 70, 81, 16))
        self.Filen.setObjectName("Filen")
        self.progressBar_save = QtWidgets.QProgressBar(self.groupBox_save)
        self.progressBar_save.setGeometry(QtCore.QRect(260, 30, 51, 23))
        #self.progressBar_save.setProperty("value", 24)
        self.progressBar_save.setObjectName("progressBar_save")
        self.spinBox_fr = QtWidgets.QSpinBox(self.groupBox_save)
        self.spinBox_fr.setGeometry(QtCore.QRect(90, 70, 41, 21))
        self.spinBox_fr.setObjectName("spinBox_fr")
        self.spinBox_fr.setMinimum(1)
        self.groupBox_save.setStyleSheet("QGroupBox#groupBox_save {border:0;}")
        self.groupBox_save.hide()
        ##########################################################
        self.s, self.t, self.frames = [], [], []
        self.fname = None
        self.frames = []
        self.min_image, self.uniform_image = None, None
        self.x, self.y = None, None
        self.avg, self.mask = None, None
        self.ima1, self.colorm = None, None
        self.date, self.time = None, None
        ##########################################################
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(440, 0, 541, 501))
        self.plot = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.plot.setObjectName(u"plot")
        self.plot.setContentsMargins(0, 0, 0, 0)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,MainWindow)
        self.toolbar.setStyleSheet("QWidget {background-color:grey;}")
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setStyleSheet("padding: 3px;")
        self.toolbar.addWidget(self.play_button)
        self.pause_button = QtWidgets.QPushButton()
        self.pause_button.setStyleSheet("padding: 3px;")
        self.toolbar.addWidget(self.pause_button)
        self.plot.addWidget(self.toolbar)
        self.plot.addWidget(self.canvas)
        ##########################################################
        self.Analysis = QtWidgets.QPushButton(self.centralwidget)
        self.Analysis.setGeometry(QtCore.QRect(150, 450, 121, 31))
        self.Analysis.clicked.connect(self.Win)
        ##########################################################
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 961, 22))
        self.menubar.setObjectName("menubar")
        self.menuTheme = QtWidgets.QMenu(self.menubar)
        self.menuTheme.setObjectName("menuTheme")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave_Image = QtWidgets.QMenu(self.menuFile)
        self.menuSave_Image.setObjectName("menuSave_Image")
        self.menuMinimum_Image = QtWidgets.QMenu(self.menuSave_Image)
        self.menuMinimum_Image.setObjectName("menuMinimum_Image")
        self.menuUniform_Image = QtWidgets.QMenu(self.menuSave_Image)
        self.menuUniform_Image.setObjectName("menuUniform_Image")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLight = QtWidgets.QAction(MainWindow)
        self.actionLight.setObjectName("actionLight")
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.actionAverage_Intensity_Plot = QtWidgets.QAction(MainWindow)
        self.actionAverage_Intensity_Plot.setObjectName("actionAverage_Intensity_Plot")
        self.actionPNG = QtWidgets.QAction(MainWindow)
        self.actionPNG.setObjectName("actionPNG")
        self.actionFITS = QtWidgets.QAction(MainWindow)
        self.actionFITS.setObjectName("actionFITS")
        self.actionPNG_2 = QtWidgets.QAction(MainWindow)
        self.actionPNG_2.setObjectName("actionPNG_2")
        self.actionFITS_2 = QtWidgets.QAction(MainWindow)
        self.actionFITS_2.setObjectName("actionFITS_2")
        self.menuTheme.addAction(self.actionLight)
        self.menuTheme.addAction(self.actionDark)
        self.menuMinimum_Image.addAction(self.actionPNG)
        self.menuMinimum_Image.addAction(self.actionFITS)
        self.menuUniform_Image.addAction(self.actionPNG_2)
        self.menuUniform_Image.addAction(self.actionFITS_2)
        self.menuSave_Image.addSeparator()
        self.menuSave_Image.addAction(self.menuMinimum_Image.menuAction())
        self.menuSave_Image.addAction(self.menuUniform_Image.menuAction())
        self.menuSave_Image.addAction(self.actionAverage_Intensity_Plot)
        self.menuFile.addAction(self.menuSave_Image.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTheme.menuAction())
        self.actionLight.triggered.connect(self.light)
        self.actionLight.trigger()
        self.actionDark.triggered.connect(self.dark)
        self.actionPNG.triggered.connect(self.pminimum)
        self.actionFITS.triggered.connect(self.fminimum)
        self.actionPNG_2.triggered.connect(self.puniform)
        self.actionFITS_2.triggered.connect(self.funiform)
        self.actionAverage_Intensity_Plot.triggered.connect(self.faverage)
        self.menuFile.setEnabled(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.Browse_le, self.Browse)
        MainWindow.setTabOrder(self.Browse, self.Start)
        MainWindow.setTabOrder(self.Start, self.Uniform)
        MainWindow.setTabOrder(self.Uniform, self.Minimum)
        MainWindow.setTabOrder(self.Minimum, self.Filtered)
        MainWindow.setTabOrder(self.Filtered, self.Average)
        MainWindow.setTabOrder(self.Average, self.Final)
        MainWindow.setTabOrder(self.Final, self.Movie)
        MainWindow.setTabOrder(self.Movie, self.comboBox_scale)
        MainWindow.setTabOrder(self.comboBox_scale, self.MinSlider)
        MainWindow.setTabOrder(self.MinSlider, self.MaxSlider)
        MainWindow.setTabOrder(self.MaxSlider, self.comboBox_save)
        MainWindow.setTabOrder(self.comboBox_save, self.Save_ok)
        MainWindow.setTabOrder(self.Save_ok, self.spinBox_fr)
        MainWindow.setTabOrder(self.spinBox_fr, self.File_le)
        MainWindow.setTabOrder(self.File_le, self.Analysis)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SITCoM: SiRGraF Integrated Tool for Coronal dynaMics"))
        self.Average.setText(_translate("MainWindow", "Average intensity Plot"))
        self.Average.clicked.connect(self.fAverage)
        self.Save_ok.setText(_translate("MainWindow", "OK"))
        self.Save_ok.clicked.connect(self.Save)
        self.Min.setText(_translate("MainWindow", "Min Scale :"))
        self.Movie.setText(_translate("MainWindow", "Movie"))
        self.Movie.clicked.connect(self.Mov)
        self.label_sav_done.setText(_translate("MainWindow", "Done!"))
        self.label_sav_done.hide()
        self.comboBox_scale.setItemText(0, _translate("MainWindow", "Linear"))
        self.comboBox_scale.setItemText(1, _translate("MainWindow", "Logarithmic"))
        self.comboBox_scale.setItemText(2, _translate("MainWindow", "MinMax"))
        self.comboBox_scale.setItemText(3, _translate("MainWindow", "Gamma"))
        self.comboBox_scale.currentTextChanged.connect(self.Scale)
        self.Final.setText(_translate("MainWindow", "Combined plots"))
        self.Final.clicked.connect(self.fFinal)
        self.Minimum.setText(_translate("MainWindow", "Minimum Intensity Image"))
        self.Minimum.clicked.connect(self.fMinimum)
        self.Filtered.setText(_translate("MainWindow", "Filtered Image"))
        self.Filtered.clicked.connect(self.fFiltered)
        self.Success.setText(_translate("MainWindow", "Success!"))
        self.Success.hide()
        self.Start.setText(_translate("MainWindow", "Start"))
        self.label_sav.setText(_translate("MainWindow", "Save movie as :"))
        self.Max.setText(_translate("MainWindow", "Max Scale:"))
        self.Uniform.setText(_translate("MainWindow", "Uniform Intensity Image"))
        self.Uniform.clicked.connect(self.fUniform)
        self.Browse.setText(_translate("MainWindow", "Browse"))
        self.Browse.clicked.connect(self.getfile)
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.play_button.clicked.connect(self.tplay)
        self.play_button.setEnabled(False)
        self.pause_button.setText(_translate("MainWindow", "Pause"))
        self.pause_button.clicked.connect(self.tpause)
        self.pause_button.setEnabled(False) 
        self.Ok1.setText(_translate("MainWindow", "OK"))
        self.Ok1.clicked.connect(self.Scale)
        self.Ok2.setText(_translate("MainWindow", "OK"))
        self.Ok2.clicked.connect(self.Scale)
        self.intensity.setText(_translate("MainWindow", "Intensity Scale:"))
        self.comboBox_save.setItemText(0, _translate("MainWindow", "mp4"))
        self.comboBox_save.setItemText(1, _translate("MainWindow", "gif"))
        self.comboBox_save.setItemText(2, _translate("MainWindow", "png"))
        self.comboBox_save.setItemText(3, _translate("MainWindow", "sav"))
        self.comboBox_save.setItemText(4, _translate("MainWindow", "fits"))
        self.frate.setText(_translate("MainWindow", "Frame Rate:"))
        self.Filen.setText(_translate("MainWindow", "File Name:"))
        self.label_min.setText(_translate("MainWindow", "0     0.25      0.5     0.75     1.0"))
        self.label_max.setText(_translate("MainWindow", "0     0.25      0.5     0.75     1.0"))
        self.label_gamma.setText(_translate("MainWindow", "0     0.25      0.5     0.75     1.0"))
        self.Analysis.setText(_translate("MainWindow", "Analysis"))
        self.menuTheme.setTitle(_translate("MainWindow", "Theme"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        #self.menuSave_Image.setTitle(_translate("MainWindow", "Save Image (PNG)"))
        self.menuSave_Image.setTitle(_translate("MainWindow", "Save Image"))
        self.menuMinimum_Image.setTitle(_translate("MainWindow", "Minimum Image"))
        self.menuUniform_Image.setTitle(_translate("MainWindow", "Uniform Image"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.actionAverage_Intensity_Plot.setText(_translate("MainWindow", "Average Intensity Plot"))
        self.actionPNG.setText(_translate("MainWindow", "PNG"))
        self.actionFITS.setText(_translate("MainWindow", "FITS"))
        self.actionPNG_2.setText(_translate("MainWindow", "PNG"))
        self.actionFITS_2.setText(_translate("MainWindow", "FITS"))
        self.gamma.setText(_translate("MainWindow", "Gamma :"))
        self.groupBox_image.setEnabled(False)
    def Win(self):
      if self.Browse_le.text()=='':
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Please enter the directory first")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
      elif any(File.endswith((".fts",".fits",".fit")) for File in os.listdir(self.fname)):
        self.window=QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.window)
        self.ui.fnamm.setText(self.Browse_le.text())
        self.window.show()
      else:
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Please enter a valid directory containing FITS files or press Start button")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
    def pminimum(self):
        fpath=os.path.expanduser('~')
        cnm=os.path.join(fpath,self.date)
        plt.imsave(cnm+'_min.png',self.min_image,cmap=self.colorm,format='png')
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("The image has been saved to "+cnm+'_min.png')
        msg.setWindowTitle("Saved!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
    def fminimum(self):
        fpath=os.path.expanduser('~')
        f1=fits.PrimaryHDU(self.min_image)
        cnm=os.path.join(fpath,self.date)
        f1.writeto(cnm+'_min.fits',overwrite=True)
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("The image has been saved to "+cnm+'_min.fits')
        msg.setWindowTitle("Saved!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval=msg.exec_()
    def faverage(self):
        fpath=os.path.expanduser('~')
        g=np.log10(self.avg)
        r=np.round(np.mean(g[np.where((np.isnan(g)==False) & (g!=np.inf))]))
        f1=fits.PrimaryHDU([self.y[np.where(self.y>=0)],self.avg/10**r])
        cnm=os.path.join(fpath,self.date)
        f1.writeto(cnm+'_avg.fits',overwrite=True)
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("The image has been saved to "+cnm+'_avg.fits')
        msg.setWindowTitle("Saved!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval=msg.exec_()

    def funiform(self):
        fpath=os.path.expanduser('~')
        f1=fits.PrimaryHDU(self.uniform_image)
        cnm=os.path.join(fpath,self.date)
        f1.writeto(cnm+'_uniform.fits',overwrite=True)
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("The image has been saved to "+cnm+'_uniform.fits')
        msg.setWindowTitle("Saved!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval=msg.exec_()
    def puniform(self):
        fpath=os.path.expanduser('~')
        cnm=os.path.join(fpath,self.date)
        plt.imsave(cnm+'_uniform.png',self.uniform_image,cmap=self.colorm,format='png')
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("The image has been saved to "+cnm+'_uniform.png')
        msg.setWindowTitle("Saved!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
    def Save(self):
        fr=self.spinBox_fr.value()
        nm=self.File_le.text()
        fpath=os.path.expanduser('~')
        self.progressBar_save.show()
        self.label_sav_done.show()
        self.label_sav_done.setText('Storing..')
        for i in range(51):
            time.sleep(0.1)
            self.progressBar_save.setValue(i)
        if self.comboBox_save.currentText()=='mp4':
          if platform.system()=='Linux':
            FFwriter = animation.FFMpegWriter(fps=fr)
            cnm=os.path.join(fpath, nm+".mp4")
            self.ani.save(cnm, writer = FFwriter,dpi=300)
          elif platform.system()=='Windows':
            Pwriter = animation.PillowWriter(fps=fr)
            cnm=os.path.join(fpath, nm+".gif")
            self.ani.save(cnm, writer = Pwriter,dpi=300)
            clip = mpe.VideoFileClip(cnm)
            clip.write_videofile(os.path.join(fpath,nm+".mp4"))
        if self.comboBox_save.currentText()=='gif':
            Pwriter = animation.PillowWriter(fps=fr)
            cnm=os.path.join(fpath, nm+".gif")
            self.ani.save(cnm, writer = Pwriter,dpi=300)
        if self.comboBox_save.currentText()=='png':
            interval = ZScaleInterval()
            vmin, vmax = interval.get_limits(self.ima1[0])
            fpath1=os.path.join(fpath+"/PNG")
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm)
            for i in range(len(self.frames)):
                plt.imsave(cnm+"-"+str(i)+'.png',self.frames[i],cmap=self.colorm,vmin=-0.1,vmax=0.1,format='png')
            self.ani.save(cnm, writer="imagemagick",fps=fr)
            animation.ImageMagickWriter.grab_frame(self.figure)
        if self.comboBox_save.currentText()=='fits':
            fpath1=os.path.join(fpath+"/FITS")
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm+".fits")
            self.ani.save(cnm, writer="imagemagick",fps=fr)
            filenames=sorted(glob.glob(fpath1+'/*.fits'))
            img=[]
            for i in range(len(filenames)):
              f1=fits.getdata(filenames[i])
              img.append(f1)
            img=np.array(img)
            fits.writeto(cnm,img)
        for i in range(51,101):
            time.sleep(0.01)
            self.progressBar_save.setValue(i)
        self.label_sav_done.setText('Done!')
    def fEdit(self):
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("The path seems to be changed! Start process again?")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        self.fname=self.Browse_le.textChanged
        self.groupBox_image.setEnabled(False)
        self.canvas.figure.clf()
        self.groupBox_save.hide()
        self.groupBox_scale.hide()
        self.canvas.draw_idle()
        #self.Browse_le.setText(self.)
        self.progressBar.reset()
        self.Success.hide()
    def Scale(self):
        if self.s==[]:
          pass
        elif self.s[-1]=="Minimum":
          self.Minimum.click()
        elif self.s[-1]=="Filtered":
          self.Filtered.click()
        elif self.s[-1]=="Uniform":
          self.Uniform.click()
        elif self.s[-1]=="Final":
          self.Final.click()
        elif self.s[-1]=="Average":
          self.Average.click()
        elif self.s[-1]=="Movie":
          self.Movie.click()
    def light(self):
        self.t.append('Light')
        #MainWindow=QtWidgets.QMainWindow()
        cw=os.path.join(self.sitep,'sitcom/data/white.png')
        MainWindow.setStyleSheet("QMainWindow{border-image: url("+cw+"); background-repeat:no-repeat; background-position: center;}")
        self.figure.set_facecolor('white')
        mp.rcParams.update({'text.color' : "black",'axes.labelcolor' : "black",'axes.edgecolor':"black",'axes.facecolor':"white",'xtick.color':"black",'ytick.color':"black"})
        #self.setupUi(MainWindow)
        if self.s==[]:
          pass
        elif self.s[-1]=="Minimum":
          self.Minimum.click()
        elif self.s[-1]=="Filtered":
          self.Filtered.click()
        elif self.s[-1]=="Uniform":
          self.Uniform.click()
        elif self.s[-1]=="Final":
          self.Final.click()
        elif self.s[-1]=="Average":
          self.Average.click()
        elif self.s[-1]=="Movie":
          self.Movie.click()   
    def dark(self):
        self.t.append('Dark')
        cw=os.path.join(self.sitep,'sitcom/data/black.png')
        MainWindow.setStyleSheet("QMainWindow{border-image: url("+cw+"); background-repeat:no-repeat; background-position: center;}QLabel{color:white;}")
        self.figure.patch.set_facecolor('black')
        mp.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white",'axes.edgecolor':"white",'axes.facecolor':"black",'xtick.color':"white",'ytick.color':"white"})
        if self.s==[]:
          pass
        elif self.s[-1]=="Minimum":
          self.Minimum.click()
        elif self.s[-1]=="Filtered":
          self.Filtered.click()
        elif self.s[-1]=="Uniform":
          self.Uniform.click()
        elif self.s[-1]=="Final":
          self.Final.click()
        elif self.s[-1]=="Average":
          self.Average.click()
        elif self.s[-1]=="Movie":
          self.Movie.click() 
    def fStart(self):
      if self.Browse_le.text()=='':
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Please enter the directory first")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
      else:
        self.fname=self.Browse_le.text()
        if any(File.endswith((".fts",".fits",".fit")) for File in os.listdir(self.fname)):
          self.Browse_le.setText(self.fname)
          self.min_image,self.uniform_image,self.ima1,self.mask,self.colorm,self.R_i,self.R_sun,self.x,self.y,self.avg,self.date,self.time=sf.sif(self.fname)
          for i in range(101):
            time.sleep(0.01)
            self.progressBar.setValue(i)
          self.Success.show()
          self.groupBox_image.setEnabled(True)
          self.menuFile.setEnabled(True)
          self.Browse_le.textChanged.connect(self.fEdit)
        else:
          msg = QtWidgets.QMessageBox()
          msg.setStyleSheet("color:'black';")
          msg.setIcon(QtWidgets.QMessageBox.Warning)
          msg.setText("Please enter a valid directory containing FITS files")
          msg.setWindowTitle("Warning!")
          msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
          retval = msg.exec_()
    def getfile(self):
      self.fname= QtWidgets.QFileDialog.getExistingDirectory(None, 'Open directory',QtCore.QDir.homePath())
      if any(File.endswith((".fts",".fits",".fit")) for File in os.listdir(self.fname)):
        self.Browse_le.setText(self.fname)
      else:
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Please enter a valid directory containing FITS files")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
    def fMinimum(self):
      self.s.append('Minimum')
      self.groupBox_scale.hide()
      self.groupBox_save.hide()
      self.groupBox_scale_2.hide()
      bg1=np.ones(self.min_image.shape)-np.log10(self.min_image)
      bg1[self.mask]=0
      self.figure.clear()
      self.ax=self.canvas.figure.add_subplot(111)
      circ2=pa.Circle((0,0),self.R_i,color='black')
      circ=pa.Circle((0,0),1,color='white',fill=False)
      i1=None
      if self.comboBox_scale.currentText()=='Linear':
        i1=self.ax.imshow(bg1,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      if self.comboBox_scale.currentText()=='Logarithmic':
        c = 255/(np.log(1 + np.max(bg1)))
        log_transformed = c * np.log(1 + bg1)
        log_transformed = np.array(log_transformed, dtype = np.uint8)
        i1=self.ax.imshow(log_transformed,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      if self.comboBox_scale.currentText()=='MinMax':
        self.groupBox_scale.show()
        vmin,vmax=self.MinSlider.value()/4,self.MaxSlider.value()/4
        i1=self.ax.imshow(bg1,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
      if self.comboBox_scale.currentText()=='Gamma':
        self.groupBox_scale_2.show()
        gamma=self.GammaSlider.value()/4
        i1=self.ax.imshow( np.float_power(bg1, gamma),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      cb=plt.colorbar(i1,ax=self.ax,shrink=0.85,pad=0.01,extend='both')
      self.ax.add_patch(circ2)
      self.ax.add_patch(circ)
      cb.set_label('Log(Intensity)')
      self.ax.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax.set_ylabel('Solar Y (R$_{\odot}$)')
      self.ax.set_title('Minimum Intensity Image')
      plt.tight_layout()
      self.canvas.draw()
    def fFiltered(self):
      self.s.append('Filtered')
      self.groupBox_scale.hide()
      self.groupBox_save.hide()
      self.groupBox_scale_2.hide()
      index=int(len(self.ima1)/2)
      interval=ZScaleInterval()
      vmin,vmax=interval.get_limits(self.ima1[index])
      #self.comboBox_scale.currentTextChanged.connect(self.fFiltered)
      self.figure.clear()
      self.ax=self.canvas.figure.add_subplot(111)
      circ2=pa.Circle((0,0),self.R_i,color='black')
      circ=pa.Circle((0,0),1,color='white',fill=False)
      i1=None
      if self.comboBox_scale.currentText()=='Linear':
        i1=self.ax.imshow(cv2.medianBlur(self.ima1[index],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
      if self.comboBox_scale.currentText()=='Logarithmic':
        c = 255/(np.log(1 + np.max(cv2.medianBlur(self.ima1[index],5))))
        log_transformed = c * np.log(1 + cv2.medianBlur(self.ima1[index],5))
        log_transformed = np.array(log_transformed, dtype = np.uint8)
        i1=self.ax.imshow(log_transformed,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      if self.comboBox_scale.currentText()=='MinMax':
        self.groupBox_scale.show()
        vmin1,vmax1=self.MinSlider.value()/4,self.MaxSlider.value()/4
        i1=self.ax.imshow(cv2.medianBlur(self.ima1[index],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin1,vmax=vmax1)
      if self.comboBox_scale.currentText()=='Gamma':
        self.groupBox_scale_2.show()
        gamma=self.GammaSlider.value()/4
        i1=self.ax.imshow( cv2.medianBlur((self.ima1[index])**gamma,5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      cb=self.figure.colorbar(i1,ax=self.ax,shrink=0.85,pad=0.01,extend='both')
      cb.ax.set_ylim(bottom=0)
      self.ax.set_facecolor("black")
      patch = pa.Circle((0,0), radius=np.max(self.y),transform=self.ax.transData)
      i1.set_clip_path(patch)
      self.ax.add_patch(circ2)
      self.ax.add_patch(circ)
      cb.set_label('Normalized Intensity')
      self.ax.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax.set_ylabel('Solar Y (R$_{\odot}$)')
      self.ax.set_title('Filtered Image')
      self.figure.tight_layout()
      self.canvas.draw()
    def fUniform(self):
      self.s.append('Uniform')
      self.groupBox_scale.hide()
      self.groupBox_save.hide()
      self.groupBox_scale_2.hide()
      bg1=np.ones(self.uniform_image.shape)-np.log10(self.uniform_image)
      bg1[self.mask]=0
      #self.comboBox_scale.currentTextChanged.connect(self.fUniform)
      self.figure.clear()
      self.ax=self.canvas.figure.add_subplot(111)
      circ2=pa.Circle((0,0),self.R_i,color='black')
      circ=pa.Circle((0,0),1,color='white',fill=False)
      i1=None
      if self.comboBox_scale.currentText()=='Linear':
        i1=self.ax.imshow(bg1,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      if self.comboBox_scale.currentText()=='Logarithmic':
        c = 255/(np.log(1 + np.max(bg1)))
        log_transformed = c * np.log(1 + bg1)
        log_transformed = np.array(log_transformed, dtype = np.uint8)
        i1=self.ax.imshow(log_transformed,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      if self.comboBox_scale.currentText()=='MinMax':
        self.groupBox_scale.show()
        vmin,vmax=self.MinSlider.value()/4,self.MaxSlider.value()/4
        i1=self.ax.imshow(bg1,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
      if self.comboBox_scale.currentText()=='Gamma':
        self.groupBox_scale_2.show()
        gamma=self.GammaSlider.value()/4
        i1=self.ax.imshow( np.float_power(bg1, gamma),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      cb=plt.colorbar(i1,ax=self.ax,shrink=0.85,pad=0.01,extend='both')
      self.ax.add_patch(circ2)
      self.ax.add_patch(circ)
      cb.set_label('Log(Intensity)')
      self.ax.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax.set_ylabel('Solar Y (R$_{\odot}$)')
      self.ax.set_title('Uniform Intensity Image')
      plt.tight_layout()
      self.canvas.draw()
    def fAverage(self):
      self.s.append('Average')
      self.groupBox_scale.hide()
      self.groupBox_save.hide()
      self.groupBox_scale_2.hide()
      g=np.log10(self.avg)
      r=np.round(np.mean(g[np.where((np.isnan(g)==False) & (g!=np.inf))]))
      self.figure.clear()
      self.ax=self.canvas.figure.add_subplot(111)
      self.ax.plot(self.y[np.where(self.y>=0)],self.avg/10**r,color='grey')
      self.ax.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax.set_ylabel('Average Intensity(10$^{'+str(int(r))+'}$)')
      self.ax.set_title('Average Intensity Plot')
      plt.tight_layout()
      self.canvas.draw()
    def fFinal(self):
      self.s.append('Final')
      self.groupBox_scale.hide()
      self.groupBox_save.hide()
      self.groupBox_scale_2.hide()
      g=np.log10(self.avg)
      r=np.round(np.mean(g[np.where((np.isnan(g)==False) & (g!=np.inf))]))
      index=int(len(self.ima1)/2)
      bg=np.ones(self.uniform_image.shape)-np.log10(self.uniform_image)
      bg[self.mask]=0
      bg1=np.ones(self.min_image.shape)-np.log10(self.min_image)
      bg1[self.mask]=0
      interval = ZScaleInterval()
      vmin, vmax = interval.get_limits(self.ima1[index])
      self.figure.clear()
      self.ax=self.canvas.figure.add_subplot(221)
      circ2=pa.Circle((0,0),self.R_i,color='black')
      circ=pa.Circle((0,0),1,color='white',fill=False)
      i1=self.ax.imshow(bg1,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      cb=plt.colorbar(i1,ax=self.ax,shrink=0.65,pad=0.05,extend='both')
      self.ax.add_patch(circ2)
      self.ax.add_patch(circ)
      cb.set_label('Log(Intensity)')
      self.ax.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax.set_ylabel('Solar Y (R$_{\odot}$)')
      self.ax.set_title('Minimum Intensity Image')
      self.ax1=self.canvas.figure.add_subplot(222)
      self.ax1.plot(self.y[np.where(self.y>=0)],self.avg/10**r,color='grey')
      self.ax1.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax1.set_ylabel('Average Intensity(10$^{'+str(int(r))+'}$)')
      self.ax1.set_title('Average Intensity Plot')
      self.ax2=self.canvas.figure.add_subplot(223)
      i2=self.ax2.imshow(bg,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      cb1=plt.colorbar(i2,ax=self.ax2,shrink=0.65,pad=0.05,extend='both')
      circ3=pa.Circle((0,0),self.R_i,color='black')
      circ1=pa.Circle((0,0),1,color='white',fill=False)
      self.ax2.add_patch(circ3)
      self.ax2.add_patch(circ1)
      cb1.set_label('Log(Intensity)')
      self.ax2.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax2.set_ylabel('Solar Y (R$_{\odot}$)')
      self.ax2.set_title('Uniform Intensity Image')
      self.ax3=self.canvas.figure.add_subplot(224)
      self.ax3.set_facecolor("black")
      i3=self.ax3.imshow(cv2.medianBlur(self.ima1[index],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
      patch = pa.Circle((0,0), radius=np.max(self.y),transform=self.ax3.transData)
      i3.set_clip_path(patch)
      circ4=pa.Circle((0,0),self.R_i,color='black')
      circ0=pa.Circle((0,0),1,color='white',fill=False)
      self.ax3.add_patch(circ4)
      self.ax3.add_patch(circ0)
      cb2 = self.figure.colorbar(i3, ax=self.ax3, shrink=0.65, pad=0.05, extend='both')
      cb2.ax.set_ylim(bottom=0)
      cb2.set_label('Normalized Intensity')
      self.ax3.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax3.set_ylabel('Solar Y (R$_{\odot}$)')
      self.ax3.set_title('Filtered Image')
      self.figure.tight_layout()
      self.canvas.draw()
    def Mov(self):
      self.s.append('Movie')
      self.play_button.setEnabled(True)
      self.pause_button.setEnabled(True)
      self.groupBox_scale.hide()
      self.groupBox_save.show()
      self.groupBox_scale_2.hide()
      self.figure.clear()
      self.frames = []
      fr = self.spinBox_fr.value()
      nm = self.File_le.text()
      fpath = os.path.expanduser('~')
      self.ima=np.copy(self.ima1)
      interval=ZScaleInterval()
      for i in range(len(self.ima1)):
          if self.comboBox_scale.currentText() == 'Linear':
              self.frames.append(cv2.medianBlur(self.ima1[i], 5))
          elif self.comboBox_scale.currentText() == 'Logarithmic':
              c = 255 / (np.log(1 + np.max(cv2.medianBlur(self.ima1[i], 5))))
              log_transformed = c * np.log(1 + cv2.medianBlur(self.ima1[i], 5))
              self.frames.append(np.array(log_transformed, dtype=np.uint8))
          elif self.comboBox_scale.currentText() == 'MinMax':
              self.frames.append(cv2.medianBlur(self.ima1[i], 5))
              vmin1, vmax1 = self.MinSlider.value() / 4, self.MaxSlider.value() / 4
          elif self.comboBox_scale.currentText() == 'Gamma':
              gamma = self.GammaSlider.value() / 4
              arr = np.float_power(cv2.medianBlur(self.ima1[i],5), gamma)
          self.ima[i][np.where(self.ima[i]<0)]=0
      ax=self.canvas.figure.add_subplot(111)
      div = make_axes_locatable(ax)
      cax = div.append_axes('right', '5%', '5%')
      circ2=pa.Circle((0,0),self.R_i,color='black')
      circ=pa.Circle((0,0),1,color='white',fill=False)
      #self.ima1[np.where(self.ima1<0)]=0
      #tx=self.ax.set_title('Date: '+self.date+' Time: '+self.time[0])
      i1=None
      if self.comboBox_scale.currentText()=='Linear':
        vmin,vmax=interval.get_limits(self.ima[0])
        i1=ax.imshow(cv2.medianBlur(self.ima[0],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
      if self.comboBox_scale.currentText()=='Logarithmic':
        c = 255/(np.log10(1 + np.max(cv2.medianBlur(self.ima1[0],5))))
        log_transformed = c * np.log10(1 + cv2.medianBlur(self.ima1[0],5))
        log_transformed = np.array(log_transformed, dtype = np.uint8)
        i1=ax.imshow(log_transformed,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      vmin1,vmax1=self.MinSlider.value()/4,self.MaxSlider.value()/4
      if self.comboBox_scale.currentText()=='MinMax':
        self.groupBox_scale.show()
        i1=ax.imshow(cv2.medianBlur(self.ima1[0],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin1,vmax=vmax1)
      if self.comboBox_scale.currentText()=='Gamma':
        self.groupBox_scale_2.show()
        gamma=self.GammaSlider.value()/4
        i1=ax.imshow(np.float_power(cv2.medianBlur(self.ima1[0],5),gamma),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      cb=self.figure.colorbar(i1,cax=cax,extend='both')
      cb.ax.set_ylim(bottom=0)
      patch = pa.Circle((0,0), radius=np.max(self.y),transform=ax.transData)
      i1.set_clip_path(patch)
      ax.add_patch(circ2)
      ax.add_patch(circ)
      ax.set_facecolor("black")
      cb.set_label('Normalized Intensity')
      ax.set_xlabel('Solar X (R$_{\odot}$)')
      ax.set_ylabel('Solar Y (R$_{\odot}$)')
      def animate(i):
        if self.comboBox_scale.currentText()=='Linear':
          vmin,vmax=interval.get_limits(self.ima1[i])
          i1=ax.imshow(cv2.medianBlur(self.ima[i],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
          #i1.set_data(arr)
          #i1.set_clim(vmin,vmax)
        elif self.comboBox_scale.currentText()=='Logarithmic':
          c = 255/(np.log(1 + np.max(cv2.medianBlur(self.ima1[i],5))))
          log_transformed = c * np.log(1 + cv2.medianBlur(self.ima1[i],5))
          i1=ax.imshow(np.array(log_transformed, dtype = np.uint8),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
          #i1.set_data(arr)
        elif self.comboBox_scale.currentText()=='MinMax':
          arr=cv2.medianBlur(self.ima1[i],5)
          #i1.set_data(arr)
          vmin1,vmax1=self.MinSlider.value()/4,self.MaxSlider.value()/4
          i1=ax.imshow(arr,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin1,vmax=vmax1)
          #i1.set_clim(vmin1,vmax1)
        elif self.comboBox_scale.currentText()=='Gamma':
          gamma=self.GammaSlider.value()/4
          arr=np.float_power(cv2.medianBlur(self.ima1[i],5),gamma)
          #i1.set_data(arr)
          i1=ax.imshow(arr,extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
        ax.set_title('Date: ' + self.date + ' Time: ' + self.time[i])
        ax.set_facecolor("black")
        patch = pa.Circle((0,0), radius=np.max(self.y),transform=ax.transData)
        i1.set_clip_path(patch)
        return ax

      self.ani = animation.FuncAnimation(self.figure, animate, frames=len(self.ima1))
      self.canvas.draw()
      self.canvas.figure.tight_layout()
      plt.tight_layout()
    def tpause(self):
      self.ani.event_source.stop()
    def tplay(self):
      self.ani.event_source.start()


 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    conda_env=os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
       cnpath=os.path.join(os.environ['CONDA_PREFIX'],'lib','python{}'.format(sys.version[:3]),'site-packages')
       if os.path.exists(cnpath):
           site_packages_path = cnpath
    else:
       site_packages_path = site.getusersitepackages()
    cl=os.path.join(site_packages_path,'sitcom/load/sitcom.gif')
    movie=QtGui.QMovie(cl)
    cf=os.path.join(site_packages_path,'sitcom/font/lato/Lato-Semibold.ttf')
    QtGui.QFontDatabase.addApplicationFont(cf)
    font = QtGui.QFont('Lato-SemiBold', 10)
    font.setWeight(50)
    splash = Load_Window(movie)
    splash.show()
    splash.movie.start()
    start = time.time()
    while movie.state() == QtGui.QMovie.Running and time.time() < start + 4:
        app.processEvents()
    MainWindow = QtWidgets.QMainWindow()
    splash.finish(MainWindow)
    splash.close()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
