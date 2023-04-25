from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.patches as pa
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
from astropy.visualization import ZScaleInterval
from astropy.visualization import MinMaxInterval
import cv2,os,site,sys
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

import sitcom.sirgraf as sf
import sitcom.sfit as sn
from sitcom.st2 import Ui_SWindow

mp.use('Qt5Agg')
mp.rcParams['font.family'] = 'monospace'

class Ui_SecondWindow(object):
    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.setFixedWidth(803)
        SecondWindow.setFixedHeight(550)
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 541, 501))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        conda_env=os.environ.get('CONDA_DEFAULT_ENV')
        site_packages_path=None
        if conda_env:
            cnpath=os.path.join(os.environ['CONDA_PREFIX'],'lib','python{}'.format(sys.version[:3]),'site-packages')
            if os.path.exists(cnpath):
              site_packages_path = cnpath
        else:
            site_packages_path = site.getusersitepackages()
        self.sitep=site_packages_path
        self.plot = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.plot.setContentsMargins(0, 0, 0, 0)
        self.plot.setObjectName("plot")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,SecondWindow)
        self.toolbar.setStyleSheet("QWidget {background-color:grey;}")
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setStyleSheet("padding: 3px;")
        self.toolbar.addWidget(self.play_button)
        self.pause_button = QtWidgets.QPushButton()
        self.pause_button.setStyleSheet("padding: 3px;")
        self.toolbar.addWidget(self.pause_button)
        self.clear_button = QtWidgets.QPushButton()
        self.clear_button.setStyleSheet("padding: 3px;")
        self.toolbar.addWidget(self.clear_button)
        self.plot_button = QtWidgets.QPushButton()
        self.plot_button.setStyleSheet("padding: 3px;")
        self.toolbar.addWidget(self.plot_button)
        self.plot.addWidget(self.toolbar)
        self.plot.addWidget(self.canvas)
        self.pmovie = QtWidgets.QPushButton(self.centralwidget)
        self.pmovie.setGeometry(QtCore.QRect(620, 20, 81, 21))
        self.pmovie.setObjectName("pmovie")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(660, 130, 71, 31))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setMaximum(360)
        self.doubleSpinBox.hide()
        self.fit_point = QtWidgets.QPushButton(self.centralwidget)
        self.fit_point.setGeometry(QtCore.QRect(640, 440, 81, 25))
        self.fit_point.setObjectName("fit_point")
        self.fit_point.hide()
        self.label_theta = QtWidgets.QLabel(self.centralwidget)
        self.label_theta.setGeometry(QtCore.QRect(600, 140, 67, 17))
        self.label_theta.setObjectName("label_theta")
        self.kinematic = QtWidgets.QPushButton(self.centralwidget)
        self.kinematic.setGeometry(QtCore.QRect(600, 90, 141, 25))
        self.kinematic.setObjectName("kinematic")
        self.htp = QtWidgets.QPushButton(self.centralwidget)
        self.htp.setGeometry(QtCore.QRect(590, 170, 191, 25))
        self.htp.setObjectName("htp")
        self.oscillation = QtWidgets.QPushButton(self.centralwidget)
        self.oscillation.setGeometry(QtCore.QRect(600, 310, 141, 25))
        self.oscillation.setObjectName("oscillation")
        self.dtp = QtWidgets.QPushButton(self.centralwidget)
        self.dtp.setGeometry(QtCore.QRect(580, 360, 201, 25))
        self.dtp.setObjectName("dtp")
        self.label_fit1 = QtWidgets.QLabel(self.centralwidget)
        self.label_fit1.setGeometry(QtCore.QRect(590, 220, 31, 17))
        self.label_fit1.setObjectName("label_fit1")
        self.comboBox_htp = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_htp.setGeometry(QtCore.QRect(620, 220, 86, 20))
        self.comboBox_htp.setObjectName("comboBox_htp")
        self.comboBox_htp.addItem("")
        self.comboBox_htp.addItem("")
        self.htp_ok = QtWidgets.QPushButton(self.centralwidget)
        self.htp_ok.setGeometry(QtCore.QRect(710, 220, 41, 21))
        self.theta_ok = QtWidgets.QPushButton(self.centralwidget)
        self.theta_ok.setGeometry(QtCore.QRect(740, 130, 41, 31))
        self.comboBox_dtp = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dtp.setGeometry(QtCore.QRect(630, 410, 101, 20))
        self.comboBox_dtp.setObjectName("comboBox_dtp")
        self.comboBox_dtp.addItem("")
        self.comboBox_dtp.addItem("")
        self.dtp_ok = QtWidgets.QPushButton(self.centralwidget)
        self.dtp_ok.setGeometry(QtCore.QRect(740, 410, 41, 21))
        self.s=['blank']
        self.t=[]
        self.sx,self.sy=[],[]
        self.lx,self.ly=[],[]
        self.evx,self.evy=[],[]
        self.ini_guess,self.ini_m=[],[]
        self.ac,self.ar=[],[]
        self.tpoints=[]
        self.min_image,self.uniform_image=None,None
        self.x,self.y=None,None
        self.avg,self.mask=None,None
        self.ima1,self.colorm=None,None
        self.date,self.time=None,None
        self.label_fit2 = QtWidgets.QLabel(self.centralwidget)
        self.label_fit2.setGeometry(QtCore.QRect(600, 410, 31, 17))
        self.label_fit2.setObjectName("label_fit2")
        SecondWindow.setCentralWidget(self.centralwidget)
        self.fnamm=QtWidgets.QLineEdit(self.centralwidget)
        self.fnamm.setGeometry(QtCore.QRect(620, 50, 113, 25))
        self.fnamm.hide()
        self.menubar = QtWidgets.QMenuBar(SecondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 22))
        self.menubar.setObjectName("menubar")
        self.menuTheme = QtWidgets.QMenu(self.menubar)
        self.menuTheme.setObjectName("menuTheme")
        SecondWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SecondWindow)
        self.statusbar.setObjectName("statusbar")
        SecondWindow.setStatusBar(self.statusbar)
        self.actionLight = QtWidgets.QAction(SecondWindow)
        self.actionLight.setObjectName("actionLight")
        self.actionLight.triggered.connect(lambda:self.light(SecondWindow))
        self.actionLight.trigger()
        self.actionDark = QtWidgets.QAction(SecondWindow)
        self.actionDark.triggered.connect(lambda: self.dark(SecondWindow))
        self.menuTheme.addAction(self.actionLight)
        self.menuTheme.addAction(self.actionDark)
        self.menubar.addAction(self.menuTheme.menuAction())

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "Analysis"))
        self.pmovie.setText(_translate("SecondWindow", "Play Movie"))
        self.pmovie.clicked.connect(self.Mov)
        self.label_theta.setText(_translate("SecondWindow", "Theta :"))
        self.label_theta.hide()
        self.kinematic.setText(_translate("SecondWindow", "Kinematic Analysis"))
        self.kinematic.clicked.connect(self.kin)
        self.htp.setText(_translate("SecondWindow", "Generate height-time plot"))
        self.htp.clicked.connect(self.HTP)
        self.htp.hide()
        self.oscillation.setText(_translate("SecondWindow", "Oscillations"))
        self.oscillation.clicked.connect(self.osc)
        self.dtp.setText(_translate("SecondWindow", "Generate distance-time plot"))
        self.dtp.clicked.connect(self.DTP)
        self.dtp.hide()
        self.label_fit1.setText(_translate("SecondWindow", "Fit :"))
        self.label_fit1.hide()
        self.comboBox_htp.setItemText(0, _translate("SecondWindow", "Linear"))
        self.comboBox_htp.setItemText(1, _translate("SecondWindow", "Quadratic"))
        self.comboBox_htp.hide()
        self.comboBox_dtp.setItemText(0, _translate("SecondWindow", "Automatic"))
        self.comboBox_dtp.setItemText(1, _translate("SecondWindow", "Manual"))
        self.comboBox_dtp.hide()
        self.htp_ok.setText(_translate("SecondWindow", "OK"))
        self.htp_ok.clicked.connect(self.HTP)
        self.htp_ok.hide()
        self.dtp_ok.setText(_translate("SecondWindow", "OK"))
        self.dtp_ok.clicked.connect(self.DTP)
        self.dtp_ok.hide()
        self.theta_ok.setText(_translate("SecondWindow", "OK"))
        self.theta_ok.clicked.connect(self.Mov)
        self.theta_ok.setCheckable(False)
        self.theta_ok.toggle()
        self.theta_ok.hide()
        self.label_fit2.setText(_translate("SecondWindow", "Fit :"))
        self.label_fit2.hide()
        self.play_button.setText(_translate("SecondWindow", "Play"))
        self.fit_point.setText(_translate("SecondWindow", "Fit Points"))
        self.play_button.clicked.connect(self.tplay)
        self.play_button.setEnabled(False)
        self.pause_button.setText(_translate("SecondWindow", "Pause"))
        self.pause_button.clicked.connect(self.tpause)
        self.pause_button.setEnabled(False)
        self.clear_button.setText(_translate("SecondWindow", "Clear"))
        self.clear_button.setEnabled(False)
        self.plot_button.setText(_translate("SecondWindow", "Plot"))
        self.plot_button.setEnabled(False)
        self.menuTheme.setTitle(_translate("SecondWindow", "Theme"))
        self.actionLight.setText(_translate("SecondWindow", "Light"))
        self.actionDark.setText(_translate("SecondWindow", "Dark"))

    def light(self,SecondWindow):
        cw=os.path.join(self.sitep,'sitcom/data/white.png')
        SecondWindow.setStyleSheet("QMainWindow{border-image: url("+cw+"); background-repeat:no-repeat; background-position: center;}")
        self.figure.set_facecolor('white')
        mp.rcParams.update({'text.color' : "black",'axes.labelcolor' : "black",'axes.edgecolor':"black",'axes.facecolor':"white",'xtick.color':"black",'ytick.color':"black"})
        if self.t==[]:
          pass
        elif self.t[-1]=='Movie':
          self.pmovie.click()
        elif self.t[-1]=='HTP':
          self.htp.click()
    def dark(self,SecondWindow):
        cw=os.path.join(self.sitep,'sitcom/data/black.png')
        SecondWindow.setStyleSheet("QMainWindow{border-image: url("+cw+"); background-repeat:no-repeat; background-position: center;}QLabel{color:white;}")
        self.figure.patch.set_facecolor('black')
        mp.rcParams.update({'text.color' : "white",'axes.labelcolor' : "white",'axes.edgecolor':"white",'axes.facecolor':"black",'xtick.color':"white",'ytick.color':"white"})
        if self.t==[]:
          pass
        elif self.t[-1]=='Movie':
          self.pmovie.click()
        elif self.t[-1]=='HTP':
          self.htp.click()

    def Mov(self):
      self.t.append('Movie')
      self.theta_ok.setChecked(True)
      self.min_image,self.uniform_image,self.ima1,self.mask,self.colorm,self.R_i,self.R_sun,self.x,self.y,self.avg,self.date,self.time=sf.sif(self.fnamm.text())
      self.play_button.setEnabled(True)
      self.pause_button.setEnabled(True)
      self.figure.clear()
      interval=ZScaleInterval()
      self.ax1=self.canvas.figure.add_subplot(111)
      div = make_axes_locatable(self.ax1)
      cax = div.append_axes('right', '5%', '5%')
      circ2=pa.Circle((0,0),self.R_i,color='black')
      circ=pa.Circle((0,0),1,color='white',fill=False)
      self.ax1.set_title('Date: '+self.date+' Time: '+self.time[0])
      im=self.ax1.imshow(cv2.medianBlur(self.ima1[0],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm)
      if self.theta_ok.isChecked():
        theta=self.doubleSpinBox.value()
        self.ax1.plot([0,np.max(self.y)*np.cos(np.radians(theta+90))],[0,np.max(self.y)*np.sin(np.radians(theta+90))],color='turquoise',linestyle=':')
        self.theta_ok.setChecked(False)
      cb=self.figure.colorbar(im,cax=cax,extend='both')
      cb.ax.set_ylim(bottom=0)
      patch = pa.Circle((0,0), radius=np.max(self.y),transform=self.ax1.transData)
      im.set_clip_path(patch)
      self.ax1.add_patch(circ2)
      self.ax1.add_patch(circ)
      self.ax1.set_facecolor("black")
      cb.set_label('Normalized Intensity')
      self.ax1.set_xlabel('Solar X (R$_{\odot}$)')
      self.ax1.set_ylabel('Solar Y (R$_{\odot}$)')
      def animate(i):
        vmin,vmax=interval.get_limits(self.ima1[i])
        im=self.ax1.imshow(cv2.medianBlur(self.ima1[i],5),extent=[self.x[0],self.x[-1],self.y[0],self.y[-1]],cmap=self.colorm,vmin=vmin,vmax=vmax)
        patch = pa.Circle((0,0), radius=np.max(self.y),transform=self.ax1.transData)
        im.set_clip_path(patch)
        self.ax1.set_title('Date: ' + self.date + ' Time: ' + self.time[i])
        self.ax1.set_facecolor("black")
        return self.ax1
      self.ani = animation.FuncAnimation(self.figure, animate, frames=len(self.ima1),blit=False)
      plt.tight_layout()
      self.canvas.draw()
    def tpause(self):
      self.ani.event_source.stop()
    def tplay(self):
      self.ani.event_source.start()
    def kin(self):
      self.s.append('Kinematic')
      if self.t==[]:
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Please play the movie first")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        #self.doubleSpinBox.valueChanged.connect(self.Mov)
      elif self.t[-1]=='Movie':
        self.label_theta.show()
        self.theta_ok.show()
        self.doubleSpinBox.show()
        self.htp.show()
        self.htp_ok.show()
        self.comboBox_htp.show()
        self.theta_ok.setCheckable(True)
        self.theta_ok.setChecked(False)
        #self.theta_ok.toggle()
        self.comboBox_htp.setEnabled(True)
    def osc(self):
      self.s.append('Oscillation')
      if self.t==[]:
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Please play the movie first")
        msg.setWindowTitle("Warning!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
      elif self.t[-1]=='Movie':
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Please click 2 points for slit!")
        msg.setWindowTitle("Select Slit!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        self.dtp.show()
        self.dtp_ok.show()
        self.pause_button.click()
        self.comboBox_dtp.show()
        self.comboBox_dtp.setEnabled(True)
        def point_event(event):
          if event.inaxes==self.ax1:
            self.evx.append(event.xdata)
            self.evy.append(event.ydata)
            self.sx.append(np.where(self.x<=event.xdata)[0][-1])
            self.sy.append(len(self.y)-np.where(self.y<=event.ydata)[0][-1])
            if len(self.sx) == 2:
              self.ax1.plot(self.evx,self.evy,color='lime')
              self.play_button.click()
              msg = QtWidgets.QMessageBox()
              msg.setStyleSheet("color:'black';")
              msg.setIcon(QtWidgets.QMessageBox.Information)
              msg.setText("Confirm the slit?")
              msg.setWindowTitle("Confirm!")
              msg.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Retry)
              if msg.exec_() == QtWidgets.QMessageBox.Retry:
                self.pause_button.click()
                self.sx.clear()
                self.sy.clear()
                self.evx.clear()
                self.evy.clear()
                self.ax1.lines.clear()
              else:
                self.play_button.click()
                self.canvas.mpl_disconnect(sid)
            elif len(self.sx)>2:
              msg = QtWidgets.QMessageBox()
              msg.setStyleSheet("color:'black';")
              msg.setIcon(QtWidgets.QMessageBox.Warning)
              msg.setText("Please click only 2 points for slit!")
              msg.setWindowTitle("Warning!")
              msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
              retval = msg.exec_()
              self.canvas.mpl_disconnect(sid)
        sid=self.canvas.mpl_connect('button_press_event',point_event)
    def HTP(self):
        self.t.append('HTP')
        theta=self.doubleSpinBox.value()
        center_x=np.where(self.x<=0)[0][-1]
        center_y=np.where(self.y<=0)[0][-1]
        a,b=[center_x,center_y],[np.max(self.x)*self.R_sun*np.sin(np.radians(theta-180))+center_x,np.max(self.y)*self.R_sun*np.cos(np.radians(theta-180))+center_y]
        hgt1=b[0]-a[0]
        hgt2=b[1]-a[1]
        b2=[np.max(self.x)*self.R_sun*np.sin(np.radians(theta+0.2-180))+center_x,np.max(self.y)*self.R_sun*np.cos(np.radians(theta+0.2-180))+center_y]
        b3=[np.max(self.x)*self.R_sun*np.sin(np.radians(theta-0.1-180))+center_x,np.max(self.y)*self.R_sun*np.cos(np.radians(theta-0.1-180))+center_y]
        a2,a3=np.ceil(np.abs([b2[0]-hgt1,b2[1]-hgt2])),np.ceil(np.abs([b3[0]-hgt1,b3[1]-hgt2]))
        top_left=np.int0(np.ceil([b3[0],b3[1]]))
        top_right=np.int0(np.ceil([b2[0],b2[1]]))
        bottom_right=np.int0(np.ceil([a2[0],a2[1]]))
        bottom_left=np.int0(np.ceil([a3[0],a3[1]]))
        contr=np.array([top_left,top_right,bottom_right,bottom_left])
        rect=cv2.minAreaRect(contr)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        width=int(rect[1][0])
        height = int(rect[1][1])
        src_pts = box.astype("float32")
        dst_pts = np.array([[0, height],[0, 0],[width, 0],[width, height]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        if (0<=theta<=89) or (theta==360):
            angle=3
        elif 90<=theta<=179:
            angle=2
        elif (270<=theta<=359):
            angle=0
        else:
            angle=1
        s1=[]
        for j in range(len(self.ima1)):
            w=cv2.warpPerspective(self.ima1[j], M, (width, height))
            s1.append(np.rot90(w,angle))
        s2=cv2.hconcat(s1)
        dimg=cv2.bilateralFilter(s2,3, 50, 50)
        interval=ZScaleInterval()
        vmin,vmax=interval.get_limits(dimg)
        t,t_min=[],[]
        for i in range(len(self.time)):
          sp=self.time[i].split(':')
          sp_min=int(sp[0])*60+int(sp[1])
          t_min.append(sp_min+int(sp[2])/60)
          t.append(int(sp[2])+sp_min*60)
        self.figure.clear()
        self.ax=self.canvas.figure.add_subplot(111)
        t1=np.linspace(t[0],t[-1],dimg.shape[1])
        #cm=plt.cm.get_cmap('soholasco2')
        #rcm=cm.reversed()
        self.ax.imshow(dimg,extent=[t_min[0],t_min[-1],self.y[np.where(self.y>=0)][0],self.y[-1]],vmin=vmin,vmax=vmax,cmap=self.colorm,aspect='auto')
        yx=self.y[np.where(self.y>=1)]
        self.ax.set_ylim(yx[0],self.y[-1])
        self.ax.axhline(1,linestyle=':',color='black')
        self.ax.axhline(self.R_i,linestyle='-.',color='black')
        self.ax.set_ylabel('Height (R$_{\odot}$)')
        self.ax.set_xlabel('Time(min)')
        self.ax.set_title('Start Time ('+self.date+'T'+self.time[0]+')')
        self.figure.tight_layout()
        if self.comboBox_htp.currentText()=='Linear':
            msg = QtWidgets.QMessageBox()
            msg.setStyleSheet("color:'black';")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Please click 2 points in the image!")
            msg.setWindowTitle("Linear fit")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            retval = msg.exec_()
            ex,ey=[],[]
            def mouse_event(event):
              ex.append(event.xdata)
              ey.append(event.ydata)
              temp_point = self.ax.scatter(ex, ey, color='black')
              if len(ex) == 2:
                temp_points = self.ax.scatter(ex, ey, color='black')
                self.ax.plot(ex,ey,color='black',linestyle=':')
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("color:'black';")
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Confirm the fit?")
                msg.setWindowTitle("Confirm line!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Retry)
                if msg.exec_() == QtWidgets.QMessageBox.Retry:
                    ex.clear()
                    ey.clear()
                    self.ax.lines.clear()
                    temp_point.remove()
                    temp_points.remove()
                else:
                    self.figure.clear()
                    self.canvas.mpl_disconnect(cid)
                    self.ax=self.canvas.figure.add_subplot(111)
                    self.ax.plot(ex,ey,color='black')
                    self.ax.set_ylim(0,self.y[-1])
                    self.ax.set_xlim(0,t_min[-1])
                    self.ax.axhline(1,linestyle=':',color='red')
                    self.ax.axhline(self.R_i,linestyle='-.',color='red')
                    self.ax.set_ylabel('Height (R$_{\odot}$)')
                    self.ax.set_xlabel('Time(min)')
                    self.ax.set_title('Start Time ('+self.date+'T'+self.time[0]+')')
                    self.ax.grid()
                    velocity=np.ceil((ey[1]-ey[0])*695700/(ex[1]*60-ex[0]*60))
                    self.ax.text(0,np.mean([1,self.R_i]),'Velocity ='+str(velocity)+r' km s$^{-1}$')
                    self.figure.tight_layout()
              elif len(ex)>2:
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("color:'black';")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Please click only 2 points for Linear fit!")
                msg.setWindowTitle("Warning!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retval = msg.exec_()
                self.canvas.mpl_disconnect(cid)
            cid = self.canvas.mpl_connect('button_press_event', mouse_event)
        elif self.comboBox_htp.currentText()=='Quadratic':
          msg = QtWidgets.QMessageBox()
          msg.setStyleSheet("color:'black';")
          msg.setIcon(QtWidgets.QMessageBox.Information)
          msg.setText("Please drag an area to crop")
          msg.setWindowTitle("Curve fit")
          msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
          msg.button(QtWidgets.QMessageBox.Ok)
          retval = msg.exec_()
          #msg.done(1)
          ec,er=[],[]
          def line_select_callback(eclick, erelease):
            ec.append([eclick.xdata, eclick.ydata])
            er.append([erelease.xdata, erelease.ydata])
            if len(ec)==1:
                self.ax.set_xlim(ec[0][0], er[0][0])
                self.ax.set_ylim(ec[0][1], er[0][1])
                qx.clear()
                qy.clear()
                #rs.set_active(False)
            elif len(ec)>1:
                rs.set_active(False)
                ec.clear()
                er.clear()
          props=dict(facecolor='bisque',edgecolor='black', alpha=0.3)
          rs = mp.widgets.RectangleSelector(self.ax, line_select_callback,drawtype='box', useblit=False,props=props, button=[1],minspanx=5, minspany=5, spancoords='pixels',interactive=False)
          qx,qy=[],[]
          def qmouse_event(event1):
            if event1.inaxes ==self.ax:
              qx.append(event1.xdata)
              qy.append(event1.ydata)
              #temp_points1=self.ax.scatter(qx, qy, color='black',s=0.7)
              if len(qx) == 5:
                #temp_points1.remove()
                temp_points=self.ax.scatter(qx,qy,color='black',s=0.7)
                cubic_interpolation_model = interp1d(qx, qy,kind='quadratic')
                X_=np.linspace(np.min(qx), np.max(qx), 500)
                Y_=cubic_interpolation_model(X_)
                self.ax.plot(X_,Y_,color='black',linestyle=':')
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("color:'black';")
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Confirm the fit?")
                msg.setWindowTitle("Confirm line!")
                RetryBtn = msg.addButton('Retry', msg.ActionRole)
                RetryFitBtn = msg.addButton('Retry Fit', msg.ActionRole)
                OkBtn = msg.addButton('Ok', msg.ActionRole)
                msg.exec_()
                if msg.clickedButton() == RetryBtn:
                  self.htp.click()
                  qx.clear()
                  qy.clear()
                  self.ax.lines[-1].remove()
                  temp_points.remove()
                elif msg.clickedButton() == RetryFitBtn:
                  qx.clear()
                  qy.clear()
                  self.ax.lines[-1].remove()
                  temp_points.remove()
                elif msg.clickedButton() == OkBtn:
                  self.figure.clear()
                  self.canvas.mpl_disconnect(qcid)
                  self.ax=self.canvas.figure.add_subplot(111)
                  yprime=np.gradient(Y_,X_)
                  ypprime=np.gradient(yprime,X_)
                  acc = np.mean(ypprime)*695700*0.28
                  self.ax.plot(X_,Y_,color='black')
                  self.ax.text(0, np.mean([1, self.R_i]), 'Acceleration =' + str(np.ceil(acc)) + r' m s$^{-2}$')
                  self.ax.set_ylim(0.8,self.y[-1])
                  self.ax.set_xlim(t_min[0],t_min[-1])
                  self.ax.axhline(1,linestyle=':',color='red')
                  self.ax.axhline(self.R_i,linestyle='-.',color='red')
                  self.ax.set_ylabel('Height (R$_{\odot}$)')
                  self.ax.set_xlabel('Time(min)')
                  self.ax.set_title('Start Time ('+self.date+'T'+self.time[0]+')')
                  self.ax.grid()
                  self.figure.tight_layout()
              elif len(qx)>5:
                msg = QtWidgets.QMessageBox()
                msg.setStyleSheet("color:'black';")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("Please click only 5 points for Curve fit!")
                msg.setWindowTitle("Warning!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retval = msg.exec_()
                self.canvas.mpl_disconnect(qcid)
            else:
              pass
          qcid = self.canvas.mpl_connect('button_press_event', qmouse_event)
    def DTP(self):
      self.t.append('DTP')
      self.play_button.setEnabled(False)
      self.pause_button.setEnabled(False)
      self.play_button.hide()
      self.pause_button.hide()
      a1,b1=[self.sx[0],self.sy[0]],[self.sx[1],self.sy[1]]
      hgt1=b1[0]-a1[0]
      hgt2=b1[1]-a1[1]
      angle=np.rad2deg(np.arctan2(self.sy[1]-self.sy[0],self.sx[1]-self.sx[0]))
      a=0
      b2,b3=[],[]
      if (0<angle<90) or (-180<angle<-90) :
        b2=[self.sx[0]+1,self.sy[0]-1]
        b3=[self.sx[0]-1,self.sy[0]+1]
        a=3
      elif (90<angle<180) or (-90<angle<0):
        b2=[self.sx[0]+1,self.sy[0]+1]
        b3=[self.sx[0]-1,self.sy[0]-1]
        a=2
      a2,a3=np.ceil(np.abs([b2[0]+hgt1,b2[1]+hgt2])),np.ceil(np.abs([b3[0]+hgt1,b3[1]+hgt2]))
      top_left=np.int0(np.ceil([b3[0],b3[1]]))
      top_right=np.int0(np.ceil([b2[0],b2[1]]))
      bottom_right=np.int0(np.ceil([a2[0],a2[1]]))
      bottom_left=np.int0(np.ceil([a3[0],a3[1]]))
      contr=np.array([top_left,top_right,bottom_right,bottom_left])
      rect=cv2.minAreaRect(contr)
      box = cv2.boxPoints(rect)
      box = np.int0(box)
      width=int(rect[1][0])
      height = int(rect[1][1])
      src_pts = box.astype("float32")
      dst_pts = np.array([[0, height-1],[0, 0],[width-1, 0],[width-1, height-1]], dtype="float32")
      M = cv2.getPerspectiveTransform(src_pts, dst_pts)
      s1=[]
      for j in range(len(self.ima1)):
        w=cv2.warpPerspective(self.ima1[j], M, (width, height))
        s1.append(np.rot90(w,a))
      s3=cv2.hconcat(s1)
      xt=cv2.bilateralFilter(s3,3, 50, 50)
      #cmap = plt.get_cmap('soholasco2')
      self.figure.clear()
      self.ax=self.canvas.figure.add_subplot(111)
      interval=MinMaxInterval()
      vmin,vmax=interval.get_limits(xt)
      self.ax.imshow(xt,cmap=self.colorm,aspect='auto',vmin=vmin,vmax=vmax)
      self.ax.set_xlabel('Frame number')
      self.ax.set_ylabel('Slit Length (Pixels)')
      plt.tight_layout()
      self.canvas.draw()
      self.canvas.figure.tight_layout()
      if self.comboBox_dtp.currentText()=='Automatic':
          self.ax.set_title('Drag the area to crop !')
          self.canvas.figure.tight_layout()
          self.window = QtWidgets.QMainWindow()
          self.ui = Ui_SWindow()
          self.ui.setupUi(self.window)
          def line_select_callback(aclick, arelease):
            self.ac.append([aclick.xdata, aclick.ydata])
            self.ar.append([arelease.xdata, arelease.ydata])
            if len(self.ac)==1:
                self.window.show()
                self.ax.set_xlim(self.ac[0][0], self.ar[0][0])
                self.ax.set_ylim(self.ar[0][1], self.ac[0][1])
                #self.ui.p0SpinBox.valueChanged.connect(lambda: sine())
                def sine(ac,ar):
                    self.ini_guess = [self.ui.p0SpinBox.value(), self.ui.p1SpinBox.value(), self.ui.p2SpinBox.value(),
                                      self.ui.p3SpinBox.value(), self.ui.p4SpinBox.value(), self.ui.p5SpinBox.value()]
                    self.ax.lines.clear()
                    xt_tr=xt[int(ac[0][1]):int(ar[0][1]),int(ac[0][0]):int(ar[0][0])]
                    sz = np.shape(xt_tr)
                    xxx = np.arange(0,sz[1],dtype='int')
                    coeff,sgm = sn.xt_gauss_peaks(xt_tr)
                    self.ax.scatter(xxx+int(ac[0][0]),coeff[1,:]+int(ac[0][1]),s=10,label='Gaussian fitted points')
                    sinp, sind = curve_fit(sn.mysine_decay, xxx, coeff[1, :], p0=self.ini_guess)
                    self.ax.plot(xxx + int(ac[0][0]),sn.mysine_decay(xxx, sinp[0], sinp[1], sinp[2], sinp[3], sinp[4], sinp[5]) + int(ac[0][1]), c='navy',label='Best-fit curve')
                    #self.ax.legend(loc="upper right")
                    self.canvas.figure.tight_layout()
                self.ui.pok.clicked.connect(lambda: sine(self.ac,self.ar))
                xt_tr=xt[int(self.ac[0][1]):int(self.ar[0][1]),int(self.ac[0][0]):int(self.ar[0][0])]
                sz = np.shape(xt_tr)
                xxx = np.arange(0,sz[1],dtype='int')
                coeff,sgm = sn.xt_gauss_peaks(xt_tr)
                self.ax.scatter(xxx+int(self.ac[0][0]),coeff[1,:]+int(self.ac[0][1]),s=10,label='Gaussian fitted points')
                self.ini_guess=[self.ui.p0SpinBox.value(),self.ui.p1SpinBox.value(),self.ui.p2SpinBox.value(),self.ui.p3SpinBox.value(),self.ui.p4SpinBox.value(),self.ui.p5SpinBox.value()]
                sinp,sind = curve_fit(sn.mysine_decay,xxx,coeff[1,:],p0=self.ini_guess)
                self.ax.plot(xxx+int(self.ac[0][0]),sn.mysine_decay(xxx,sinp[0],sinp[1],sinp[2],sinp[3],sinp[4],sinp[5])+int(self.ac[0][1]),c='navy',label='Best-fit curve')
                self.ax.legend(loc='upper right')
                self.canvas.figure.tight_layout()
                def plot(ac,ar):
                  self.figure.clear()
                  self.ax=self.canvas.figure.add_subplot(111)
                  self.window.close()
                  xt_tr=xt[int(ac[0][1]):int(ar[0][1]),int(ac[0][0]):int(ar[0][0])]
                  sz = np.shape(xt_tr)
                  xxx = np.arange(0,sz[1],dtype='int')
                  coeff,sgm = sn.xt_gauss_peaks(xt_tr)
                  sinp,sind = curve_fit(sn.mysine_decay,xxx,coeff[1,:],p0=self.ini_guess)
                  self.ax.grid()
                  self.ax.set_ylim(ar[0][1],ac[0][1])
                  fpath=os.path.expanduser('~')
                  cnm=os.path.join(fpath,self.date)
                  np.savetxt(cnm+'_auto_param.csv',[self.ini_guess[:]],header='p0,p1,p2,p3,p4,p5',delimiter=',', fmt='%s')
                  self.ax.plot(xxx + int(ac[0][0]),sn.mysine_decay(xxx, sinp[0], sinp[1], sinp[2], sinp[3], sinp[4], sinp[5]) + int(ac[0][1]), c='navy')
                  self.ax.set_ylabel('Slit_length( Pixels)')
                  self.ax.set_xlabel('Frame Number')
                  msg = QtWidgets.QMessageBox()
                  msg.setStyleSheet("color:'black';")
                  msg.setIcon(QtWidgets.QMessageBox.Information)
                  msg.setText("The final parameters are saved in"+cnm+'_auto_param.csv')
                  msg.setWindowTitle("Saved!")
                  msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                  retval = msg.exec_()
                self.plot_button.setEnabled(True)
                self.plot_button.clicked.connect(lambda: plot(self.ac,self.ar))
                ra.set_active(False)
                self.ax.set_title('')

            elif len(self.ac)>1:
                ra.set_active(False)
          ra = mp.widgets.RectangleSelector(self.ax,line_select_callback,drawtype='box',  props = dict(facecolor='khaki',edgecolor='black', alpha=0.3),useblit=False, button=[1],minspanx=5, minspany=5, spancoords='pixels',interactive=False)
          self.canvas.figure.tight_layout()
      elif self.comboBox_dtp.currentText()=='Manual':
        self.clear_button.setEnabled(True)
        self.fit_point.show()
        def qmouse_event(event5):
          if self.toolbar.mode!= 'zoom rect':
            if event5.inaxes ==self.ax:
             self.clear_button.show()
             def clear():
                 self.lx.clear()
                 self.ly.clear()
                 tpoints.remove()
                 self.ax.lines.clear()
             self.clear_button.clicked.connect(clear)
             if event5.button==1:
                self.lx.append(event5.xdata)
                self.ly.append(event5.ydata)
                tpoints=self.ax.plot(self.lx,self.ly,'bo')
             if event5.button==3:
                self.lx.pop()
                self.ly.pop()
                self.ax.lines[-1].remove()
             self.window = QtWidgets.QMainWindow()
             self.ui = Ui_SWindow()
             self.ui.setupUi(self.window)
             def fit():
              self.window.show()
              lid = self.canvas.mpl_connect('button_press_event', qmouse_event)
              self.ini_m = [self.ui.p0SpinBox.value(), self.ui.p1SpinBox.value(), self.ui.p2SpinBox.value(),self.ui.p3SpinBox.value(), self.ui.p4SpinBox.value(), self.ui.p5SpinBox.value()]
              sinp,sind = curve_fit(sn.mysine_decay,np.int0(self.lx),self.ly,p0=self.ini_m)
              self.ax.plot(np.int0(self.lx),sn.mysine_decay(np.int0(self.lx),sinp[0],sinp[1],sinp[2],sinp[3],sinp[4],sinp[5]),c='navy',label='Best-fit curve')
              #self.ax.legend(loc='upper right')
             def sine():
               self.ini_m = [self.ui.p0SpinBox.value(), self.ui.p1SpinBox.value(), self.ui.p2SpinBox.value(),self.ui.p3SpinBox.value(), self.ui.p4SpinBox.value(), self.ui.p5SpinBox.value()]
               sinp,sind = curve_fit(sn.mysine_decay,np.int0(self.lx),self.ly,p0=self.ini_m)
               self.ax.lines.clear()
               self.ax.plot(np.int0(self.lx),sn.mysine_decay(np.int0(self.lx),sinp[0],sinp[1],sinp[2],sinp[3],sinp[4],sinp[5]))
             self.fit_point.clicked.connect(fit)
             self.ui.pok.clicked.connect(sine)
          self.figure.canvas.draw()
          self.canvas.figure.tight_layout()
        lid = self.canvas.mpl_connect('button_press_event', qmouse_event)


        def plot(lx,ly):
           self.figure.clear()
           self.ax=self.canvas.figure.add_subplot(111)
           self.window.close()
           sinp,sind = curve_fit(sn.mysine_decay,np.int0(self.lx),self.ly,p0=self.ini_m)
           self.ax.grid()
           self.ax.plot(np.int0(self.lx),sn.mysine_decay(np.int0(self.lx),sinp[0],sinp[1],sinp[2],sinp[3],sinp[4],sinp[5]),c='navy')
           col1=['p0','p1','p2','p3','p4','p5']
           fpath=os.path.expanduser('~')
           cnm=os.path.join(fpath,self.date)
           np.savetxt(cnm+'_manual_param.csv',[self.ini_m[:]],header='p0,p1,p2,p3,p4,p5',delimiter=',', fmt='%s')
           self.ax.set_ylabel('Slit_length( Pixels)')
           self.ax.set_xlabel('Frame Number')
           self.ax.set_ylim(self.ax.get_ylim()[::-1])
           msg = QtWidgets.QMessageBox()
           msg.setStyleSheet("color:'black';")
           msg.setIcon(QtWidgets.QMessageBox.Information)
           msg.setText("The final parameters are saved in"+cnm+'_manual_param.csv')
           msg.setWindowTitle("Saved!")
           msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
           retval = msg.exec_()
        self.plot_button.setEnabled(True)
        self.plot_button.clicked.connect(lambda: plot(self.lx,self.ly))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondWindow()
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())
