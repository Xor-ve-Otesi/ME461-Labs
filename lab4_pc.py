import sys
import lab4_ui
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from lab4_ui import Ui_MainWindow
import socket
from time import sleep

addr = socket.getaddrinfo("192.168.61.141", 1235)[0][-1]
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


class Lab4():
    def __init__(self) -> None:

        """
        Format of the data to be sent to motors:
        b'start, motor_number, direction, duty_cycle, frequency'
        
        start:
            - 0: Stop
            - 1: Start

        motor number:
            - 0: motor A
            - 1: motor B

        directon:
            - 0: CW
            - 1: CCW
            - 2: STOP
        
        duty_cycle:
            - dynamic value (int)

        frequency:
            - dynamic value (int)
        """

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.button_initiator()

        self.start = 0
        self.duty = 0
        self.freq = 1000
        self.motor = 0 # Indicates A
        self.direction = 0
        self.ui.DutyCycleSlider.setMaximum(100)
        self.ui.FrequencySlider.setMaximum(1000)
        self.ui.FrequencySlider.setMinimum(100)
        self.ui.FrequencySlider.setValue(1000)
        self.runLongTask()

    def button_initiator(self):
        self.ui.dc_0_rb.clicked.connect(lambda  a: self.duty_cycle(0))
        self.ui.dc_25_rb.clicked.connect(lambda  a: self.duty_cycle(25))
        self.ui.dc_50_rb.clicked.connect(lambda  a: self.duty_cycle(50))
        self.ui.dc_75_rb.clicked.connect(lambda  a: self.duty_cycle(75))
        self.ui.dc_100_rb.clicked.connect(lambda  a: self.duty_cycle(100))
        self.ui.CWrb.clicked.connect(lambda  a: self.direction_control(0))
        self.ui.CCWrb.clicked.connect(lambda  a: self.direction_control(1))
        self.ui.motorArb.clicked.connect(lambda  a: self.motor_select(0))
        self.ui.motorBrb.clicked.connect(lambda  a: self.motor_select(1))
        self.ui.StopButton.clicked.connect(self.stopping)
        self.ui.StartButton.clicked.connect(self.starting)
        self.ui.DutyCycleSlider.sliderReleased.connect(self.duty_changed)
        self.ui.FrequencySlider.sliderReleased.connect(self.frequency_changed)

    def motor_select(self, which_motor):
        self.ui.TextFieldPC.setText("Motor is changed.")
        self.motor = which_motor
            #self.Client.send(str.encode(f"0,{self.duty},{self},{}"))

    def direction_control(self, dir):
        self.ui.TextFieldPC.setText("Direction is changed.")
        self.direction = dir
    
    def duty_cycle(self, duty_val):
        self.ui.TextFieldPC.setText(f"Duty cycle is changed to {duty_val}.")
        self.ui.DutyCycleSlider.setValue(duty_val)
        self.duty = duty_val

    def frequency(self, freq_val):
        self.ui.TextFieldPC.setText(f"Frequency is changed to {freq_val}.")
        self.ui.FrequencySlider.setValue(freq_val)
        self.freq = freq_val

    def stopping(self):
        self.direction = 2
        self.start = 0
        self.duty_cycle(0)
        self.frequency(100)
        self.ui.TextFieldPC.setText("Motor is stopped.")

    def starting(self):
        self.ui.TextFieldPC.setText("Motor is started.")
        self.start = 1
        self.direction = 0

    def duty_changed(self):
        self.duty_cycle(self.ui.DutyCycleSlider.value())

    def frequency_changed(self):
        self.frequency(self.ui.FrequencySlider.value())

    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

    def reportProgress(self,num):
        conn.sendall(f"{self.start},{self.motor},{self.direction},{self.duty},{self.freq}".encode())  # send data to the client
        self.ui.TextFieldPico.setText(f"Start: {self.start} \t\t\tMotor: {self.motor} \t\tDirection: {self.direction}\nDuty Cycle: {self.duty}\t\tFrequency: {self.freq}")
        print(f"{self.start},{self.motor},{self.direction},{self.duty},{self.freq}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lab4 = Lab4()
    lab4.MainWindow.show()
    sys.exit(app.exec_())