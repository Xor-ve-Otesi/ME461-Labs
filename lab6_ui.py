# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab6.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ContinuousModeGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ContinuousModeGroupBox.setGeometry(QtCore.QRect(320, 190, 251, 311))
        self.ContinuousModeGroupBox.setObjectName("ContinuousModeGroupBox")
        self.RunButton = QtWidgets.QPushButton(self.ContinuousModeGroupBox)
        self.RunButton.setGeometry(QtCore.QRect(30, 40, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.RunButton.setFont(font)
        self.RunButton.setObjectName("RunButton")
        self.delayText = QtWidgets.QLabel(self.ContinuousModeGroupBox)
        self.delayText.setGeometry(QtCore.QRect(40, 100, 181, 51))
        self.delayText.setAlignment(QtCore.Qt.AlignCenter)
        self.delayText.setObjectName("delayText")
        self.DelayInputField = QtWidgets.QTextEdit(self.ContinuousModeGroupBox)
        self.DelayInputField.setGeometry(QtCore.QRect(20, 150, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.DelayInputField.setFont(font)
        self.DelayInputField.setLineWidth(-1)
        self.DelayInputField.setObjectName("DelayInputField")
        self.StopButton = QtWidgets.QPushButton(self.ContinuousModeGroupBox)
        self.StopButton.setGeometry(QtCore.QRect(30, 230, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StopButton.setFont(font)
        self.StopButton.setObjectName("StopButton")
        self.CoilInputField = QtWidgets.QTextEdit(self.centralwidget)
        self.CoilInputField.setGeometry(QtCore.QRect(30, 20, 251, 481))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.CoilInputField.setFont(font)
        self.CoilInputField.setObjectName("CoilInputField")
        self.CurrentSequenceText = QtWidgets.QLabel(self.centralwidget)
        self.CurrentSequenceText.setGeometry(QtCore.QRect(330, 30, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.CurrentSequenceText.setFont(font)
        self.CurrentSequenceText.setText("")
        self.CurrentSequenceText.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentSequenceText.setObjectName("CurrentSequenceText")
        self.SingleStepButton = QtWidgets.QPushButton(self.centralwidget)
        self.SingleStepButton.setGeometry(QtCore.QRect(360, 100, 181, 51))
        self.SingleStepButton.setObjectName("SingleStepButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ContinuousModeGroupBox.setTitle(_translate("MainWindow", "Continuous Mode"))
        self.RunButton.setText(_translate("MainWindow", "RUN"))
        self.delayText.setText(_translate("MainWindow", "Delay between steps (ms)"))
        self.DelayInputField.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:24pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">20</p></body></html>"))
        self.StopButton.setText(_translate("MainWindow", "STOP"))
        self.CoilInputField.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:24pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1000</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1100</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0100</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0110</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0010</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0011</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0001</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1001</p></body></html>"))
        self.SingleStepButton.setText(_translate("MainWindow", "Apply Single Step"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
