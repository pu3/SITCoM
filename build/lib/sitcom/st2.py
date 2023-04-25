
from PyQt5 import QtCore, QtGui, QtWidgets
import site, os, sys

class Ui_SWindow(object):
    def setupUi(self, SWindow):
        SWindow.setObjectName("SWindow")
        SWindow.setFixedWidth(596)
        SWindow.setFixedHeight(442)
        self.centralwidget = QtWidgets.QWidget(SWindow)
        self.centralwidget.setObjectName("centralwidget")
        site_packages_path=None
        conda_env=os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env:
              cnpath=os.path.join(os.environ['CONDA_PREFIX'],'lib','python{}'.format(sys.version[:3]),'site-packages')
              if os.path.exists(cnpath):
                 site_packages_path = cnpath
        else:
              site_packages_path = site.getusersitepackages()
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        self.horizontalFrame.setGeometry(QtCore.QRect(10, 10, 571, 331))
        cw=os.path.join(site_packages_path,'sitcom/data/Sine_curve.png')
        self.horizontalFrame.setStyleSheet("QFrame{border-image: url("+cw+"); background-repeat:no-repeat; background-position: center;}")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.diagram = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.diagram.setObjectName("diagram")
        
        self.p0SpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p0SpinBox.setGeometry(QtCore.QRect(40, 370, 61, 41))
        self.p0SpinBox.setRange(-100000,100000)
        self.p0SpinBox.setValue(8)
        self.p0SpinBox.setObjectName("p0SpinBox")
        self.p5 = QtWidgets.QLabel(self.centralwidget)
        self.p5.setGeometry(QtCore.QRect(440, 340, 31, 31))
        self.p5.setObjectName("p5")
        self.p0 = QtWidgets.QLabel(self.centralwidget)
        self.p0.setGeometry(QtCore.QRect(50, 340, 31, 31))
        self.p0.setObjectName("p0")
        self.p1 = QtWidgets.QLabel(self.centralwidget)
        self.p1.setGeometry(QtCore.QRect(140, 340, 31, 31))
        self.p1.setObjectName("p1")
        self.p2 = QtWidgets.QLabel(self.centralwidget)
        self.p2.setGeometry(QtCore.QRect(220, 340, 31, 31))
        self.p2.setObjectName("p2")
        self.p3 = QtWidgets.QLabel(self.centralwidget)
        self.p3.setGeometry(QtCore.QRect(290, 340, 31, 31))
        self.p3.setObjectName("p3")
        self.p4 = QtWidgets.QLabel(self.centralwidget)
        self.p4.setGeometry(QtCore.QRect(370, 340, 31, 31))
        self.p4.setObjectName("p4")
        self.p1SpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p1SpinBox.setGeometry(QtCore.QRect(120, 370, 61, 41))
        self.p1SpinBox.setObjectName("p1SpinBox")
        self.p1SpinBox.setRange(-100000,100000)
        self.p1SpinBox.setValue(20)
        self.p2SpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p2SpinBox.setGeometry(QtCore.QRect(200, 370, 61, 41))
        self.p2SpinBox.setObjectName("p2SpinBox")
        self.p2SpinBox.setRange(-100000,100000)
        self.p2SpinBox.setValue(40)
        self.p3SpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p3SpinBox.setGeometry(QtCore.QRect(280, 370, 61, 41))
        self.p3SpinBox.setObjectName("p3SpinBox")
        self.p3SpinBox.setRange(-100000,100000)
        self.p3SpinBox.setValue(1)
        self.p4SpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p4SpinBox.setGeometry(QtCore.QRect(360, 370, 61, 41))
        self.p4SpinBox.setObjectName("p4SpinBox")
        self.p4SpinBox.setRange(-100000,100000)
        self.p4SpinBox.setValue(10)
        self.p5SpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.p5SpinBox.setGeometry(QtCore.QRect(430, 370, 61, 41))
        self.p5SpinBox.setObjectName("p5SpinBox")
        self.p5SpinBox.setRange(-100000,100000)
        self.p5SpinBox.setValue(0.1)
        self.pok = QtWidgets.QPushButton(self.centralwidget)
        self.pok.setGeometry(QtCore.QRect(510, 370, 61, 41))
        self.pok.setObjectName("pok")
        SWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SWindow)
        self.statusbar.setObjectName("statusbar")
        SWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SWindow)
        QtCore.QMetaObject.connectSlotsByName(SWindow)

    def retranslateUi(self, SWindow):
        _translate = QtCore.QCoreApplication.translate
        SWindow.setWindowTitle(_translate("SWindow", "Sine_Curve_parameters"))
        self.p5.setText(_translate("SWindow", "p5 :"))
        self.p0.setText(_translate("SWindow", "p0 :"))
        self.p1.setText(_translate("SWindow", "p1 :"))
        self.p2.setText(_translate("SWindow", "p2 :"))
        self.p3.setText(_translate("SWindow", "p3 :"))
        self.p4.setText(_translate("SWindow", "p4 :"))
        self.pok.setText(_translate("SWindow", "Ok"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SWindow = QtWidgets.QMainWindow()
    ui = Ui_SWindow()
    ui.setupUi(SWindow)
    SWindow.show()
    sys.exit(app.exec_())
