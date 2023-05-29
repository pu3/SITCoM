
from PyQt5 import QtCore, QtGui, QtWidgets
import os,platform
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time,imageio 
import numpy as np
from astropy.visualization import ZScaleInterval

class Ui_SaveWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedWidth(470)
        MainWindow.setFixedHeight(197)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_save = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_save.setGeometry(QtCore.QRect(10, 10, 411, 101))
        self.groupBox_save.setGeometry(QtCore.QRect(10, 10, 451, 161))
        self.groupBox_save.setObjectName("groupBox_save")
        current_path=os.path.dirname(os.path.realpath(__file__))
        self.sitep=current_path
        self.frate = QtWidgets.QLabel(self.groupBox_save)
        self.frate.setGeometry(QtCore.QRect(30, 130, 91, 17))
        self.frate.setObjectName("frate")
        self.label_sav = QtWidgets.QLabel(self.groupBox_save)
        self.label_sav.setGeometry(QtCore.QRect(80, 30, 101, 20))
        self.label_sav.setObjectName("label_sav")
        self.File_le = QtWidgets.QLineEdit(self.groupBox_save)
        self.File_le.setGeometry(QtCore.QRect(260, 130, 113, 20))
        self.File_le.setObjectName("File_le")
        self.Save_ok = QtWidgets.QPushButton(self.groupBox_save)
        self.Save_ok.setGeometry(QtCore.QRect(290, 30, 41, 25))
        self.Save_ok.setObjectName("Save_ok")
        self.label_sav_done = QtWidgets.QLabel(self.groupBox_save)
        self.label_sav_done.setGeometry(QtCore.QRect(180, 70, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_sav_done.setFont(font)
        self.label_sav_done.setObjectName("label_sav_done")
        self.comboBox_save = QtWidgets.QComboBox(self.groupBox_save)
        self.comboBox_save.setGeometry(QtCore.QRect(190, 30, 86, 25))
        self.comboBox_save.setObjectName("comboBox_save")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.comboBox_save.addItem("")
        self.Filen = QtWidgets.QLabel(self.groupBox_save)
        self.Filen.setGeometry(QtCore.QRect(180, 130, 81, 16))
        self.Filen.setObjectName("Filen")
        self.spinBox_fr = QtWidgets.QSpinBox(self.groupBox_save)
        self.spinBox_fr.setGeometry(QtCore.QRect(120, 130, 41, 21))
        self.spinBox_fr.setObjectName("spinBox_fr")
        self.spinBox_fr.setMinimum(1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        cw=os.path.join(self.sitep,'data/save.png')
        MainWindow.setStyleSheet("QMainWindow{border-image: url("+cw+"); background-repeat:no-repeat; background-position: center;}")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Save Files"))
        self.frate.setText(_translate("MainWindow", "Frame Rate:"))
        self.label_sav.setText(_translate("MainWindow", "Save movie as :"))
        self.label_sav_done.setText(_translate("MainWindow", "Storing."))
        self.label_sav_done.hide()
        self.Save_ok.setText(_translate("MainWindow", "OK"))
        self.Save_ok.clicked.connect(self.Save)
        self.comboBox_save.setItemText(0, _translate("MainWindow", "mp4"))
        self.comboBox_save.setItemText(1, _translate("MainWindow", "gif"))
        self.comboBox_save.setItemText(2, _translate("MainWindow", "png"))
        self.comboBox_save.setItemText(3, _translate("MainWindow", "fits"))
        self.comboBox_save.setItemText(4, _translate("MainWindow", "sav"))
        self.Filen.setText(_translate("MainWindow", "File Name:"))

    def Save(self):
        fr=self.spinBox_fr.value()
        nm=self.File_le.text()
        fpath=os.path.expanduser('~')
        self.label_sav_done.show()
        time.sleep(0.01)
        self.label_sav_done.clear()
        self.label_sav_done.setText('Storing..')
        msg = QtWidgets.QMessageBox()
        msg.setStyleSheet("color:'black';")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Files will be saved in: "+os.path.join(fpath, self.date))
        msg.setWindowTitle("Files")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        interval = ZScaleInterval()
        vmin, vmax = interval.get_limits(self.ima1[10])
        if self.comboBox_save.currentText()=='mp4':
            fpath1=os.path.join(fpath,self.date)
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm+".mp4")
            #cn=os.path.join(fpath, self.date,nm)
            with imageio.get_writer(cnm,fps=fr,quality=10) as writer:
              for i in range(len(self.ima1)):
                writer.append_data(self.frames[i])
        elif self.comboBox_save.currentText()=='gif':
            fpath1=os.path.join(fpath,self.date)
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm+".gif")
            imageio.mimsave(cnm,self.frames[:len(self.ima1)],fps=fr)
        elif self.comboBox_save.currentText()=='png':
            self.spinBox_fr.setEnabled(False) 
            fpath1=os.path.join(fpath,self.date,"PNG")
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm)
            for i in range(len(self.ima1)):
                plt.imsave(cnm+"-"+'_'.join(self.date.split('-')[1:])+'T'+'_'.join(self.time[i].split(':'))+'.png',self.fram[i],cmap=self.colorm,vmin=vmin,vmax=vmax,format='png')
        elif self.comboBox_save.currentText()=='fits':
            self.spinBox_fr.setEnabled(False)
            fpath1=os.path.join(fpath,self.date,"FITS")
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm)
            img=[]
            for i in range(len(self.fram)):
             im = fits.PrimaryHDU(self.fram[i])
             hdu=fits.HDUList(im)
             sv='_'.join(self.date.split('-')[1:])+'T'+'_'.join(self.time[i].split(':'))
             hdu.writeto(cnm+f'-{sv}.fits')
             hdu.close()
            img=np.array(self.frames)
            fits.writeto(cnm+'_cube.fits',img)
        elif self.comboBox_save.currentText()=='sav':
            self.spinBox_fr.setEnabled(False)
            fpath1=os.path.join(fpath,self.date,"SAV")
            os.makedirs(fpath1,mode=0o777,exist_ok=True)
            cnm=os.path.join(fpath1,nm)
            for i in range(len(self.ima1)):
              np.save(cnm+'_'+str(i)+'.npy', self.fram[i])
              img_from_file = np.load(cnm+'_'+str(i)+'.npy')
              np.savetxt(cnm+'-'+'_'.join(self.date.split('-')[1:])+'T'+'_'.join(self.time[i].split(':'))+'.sav', img_from_file)
              os.remove(cnm+'_'+str(i)+'.npy')
        self.label_sav_done.clear()
        self.label_sav_done.setText('Done!')
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_SaveWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
