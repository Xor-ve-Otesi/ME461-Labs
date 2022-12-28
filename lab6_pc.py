import sys
import lab6_ui
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from ui import Ui_MainWindow
import socket
from time import sleep

#"""
addr = socket.getaddrinfo("192.168.8.141", 1236)[0][-1]
ServerSideSocket = socket.socket()
ServerSideSocket.bind(addr)
ServerSideSocket.listen(5)
conn, address = ServerSideSocket.accept()  # accept new connection
#"""

# Step 1: Create a worker class
class Worker2(QObject):
    progress = pyqtSignal(int)

    def __init__(self, delay= 20, parent = None) -> None:
        super().__init__(parent)
        self.delay = delay
        self.stopper = False

    def run(self):

        while True:
            if not self.stopper:
                #self.progress.emit(0)
                sleep(self.delay / 1000)


# Step 1: Create a worker class
class Worker(QObject):
    progress = pyqtSignal(int)

    def run(self):

        while True:
            data = conn.recv(1024).decode()
            #sleep(0.0001)
            self.progress.emit(0)


class Lab6():
    def __init__(self) -> None:

        """
        Format of the data:
        b'data1,data2,data3,data4'
        """

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.button_initiator()
        self.sequence = ["..."]
        self.current_step = []
        self.current_delay = 20
        self.initialize = True
        self.sequence = self.ui.CoilInputField.toPlainText().split("\n")
        self.current_step = self.sequence[0]
        self.index = 0
        self.continuous_run = 0
        self.single()

    def button_initiator(self):
        self.ui.RunButton.clicked.connect(self.continuous)
        self.ui.SingleStepButton.clicked.connect(self.single_run)
        self.ui.StopButton.clicked.connect(self.stop)
        self.ui.DelayInputField.textChanged.connect(self.delay_change)

    def single_run(self, num = 2):
        self.current_step = self.sequence[self.index]
        print(self.current_step)
        self.index += 1
        self.ui.CurrentSequenceText.setText(self.current_step)
        if self.index == 8:
            self.index = 0

    def delay_change(self):
        try:
            self.current_delay = int(self.ui.DelayInputField.toPlainText())
        except:
            self.current_delay = 20

    def single(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.reportProgress_single)
        self.thread.start()

    def continuous(self):
        if self.initialize:
            self.thread2 = QThread()
            self.worker2 = Worker2(self.current_delay)
            self.worker2.moveToThread(self.thread2)
            self.thread2.started.connect(self.worker2.run)
            self.worker2.progress.connect(self.single_run)
            self.thread2.start()
            self.initialize = False
        
        self.worker2.stopper = False
        self.continuous_run = 1
        self.worker2.delay = self.current_delay

    def reportProgress_single(self,num):
        conn.sendall(f"{self.current_delay, self.index, self.continuous_run}".encode())  # send data to the client
        print(f"{self.current_delay, self.index, self.continuous_run}".encode())
        self.ui.CurrentSequenceText.setText(f"{self.current_step}")

    def stop(self):
        self.worker2.stopper = True
        self.continuous_run = 0

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lab6 = Lab6()
    lab6.MainWindow.show()
    sys.exit(app.exec_())
