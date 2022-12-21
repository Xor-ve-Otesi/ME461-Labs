import sys
import lab5_ui
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from lab5_ui import Ui_MainWindow
import socket
from time import sleep

addr = socket.getaddrinfo("192.168.184.141", 1242)[0][-1]
ServerSideSocket = socket.socket()
ServerSideSocket.bind(addr)
ServerSideSocket.listen(5)
conn, address = ServerSideSocket.accept()  # accept new connection

# Step 1: Create a worker class
class Worker(QObject):
    progress = pyqtSignal(int)

    def run(self):

        while True:
            data = conn.recv(1024).decode()
            #sleep(0.2)
            self.progress.emit(0)


class Lab5():
    def __init__(self) -> None:

        """
        Format of the data:
        b'is_active, pwm'
        """

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.button_initiator()
        self.is_active = 0
        self.pwm = 0
        self.ui.PWMslider.setMaximum(180)
        self.runLongTask()

    def button_initiator(self):
        self.ui.rb_0.clicked.connect(lambda  a: self.PWM_signal(0))
        self.ui.rb_45.clicked.connect(lambda  a: self.PWM_signal(45))
        self.ui.rb_90.clicked.connect(lambda  a: self.PWM_signal(90))
        self.ui.rb_135.clicked.connect(lambda  a: self.PWM_signal(135))
        self.ui.rb_180.clicked.connect(lambda  a: self.PWM_signal(180))
        self.ui.Releasebutton.clicked.connect(self.release)
        self.ui.PWMslider.sliderReleased.connect(self.PWM_changed)

    def PWM_signal(self, num):
        self.pwm = num
        self.is_active = 1
        self.ui.PWMslider.setValue(num)

    def PWM_changed(self):
        self.PWM_signal(self.ui.PWMslider.value())
        self.ui.SignalText.setText(f"PWM signal changed to {self.ui.PWMslider.value()}")

    def release(self):
        self.is_active = 0
        self.ui.SignalText.setText(f"Button is released")

    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

    def reportProgress(self,num):
        conn.sendall(f"{self.is_active},{self.pwm}".encode())  # send data to the client
        self.ui.SignalText.setText(f"{self.is_active},{self.pwm}")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lab5 = Lab5()
    lab5.MainWindow.show()
    sys.exit(app.exec_())