import socket
import network
import time
from machine import Pin, PWM, ADC


class Lab5():

    def __init__(self) -> None:
        self.servo = PWM(Pin(18))
        self.pot = ADC(26)
        self.servo.freq(50)
        self.angle = 0
        self.menu()

    def step3(self):
        while True:
            try:
                self.step3_input = int(input())
                duty_cycle = int((self.step3_input*(7803-1950)/180) / 180 * 194) + 1950
                self.servo.duty_u16(duty_cycle)
            except:
                print("Invalid input")
                break

    def step4(self):
        while True:        
            self.angle = self.pot.read_u16() / 65536 * 180
            duty_cycle = int((self.angle*(7803-1950)/180) / 180 * 194) + 1950
            self.servo.duty_u16(duty_cycle)
            time.sleep(0.2)

    def step5(self):
        #"""
        ssid = 'Galaxy A32AE20'          # WIFI ID
        password = 'qgfb9519'           # WIFI Password

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        ai = socket.getaddrinfo("192.168.184.141", 1242) # Address of Web Server
        addr = ai[0][-1]
        self.cl = socket.socket() # Open socket
        self.cl.connect(addr)
        #"""
        # Create a socket and make a HTTP request

        old_data = ""
        while True:
            time.sleep(0.2)
            self.cl.send(str.encode("2"))  # send message
            data = self.cl.recv(1024).decode()  # receive response
            print(data)

            if old_data != data:
                data = data.split(",")
                self.is_active = int(data[0])
                self.pwm_signal = int(data[1])
                if self.is_active:
                    self.pwm_signal = int((self.pwm_signal*(7803-1950)/180) / 180 * 194) + 1950
                    self.servo.duty_u16(int(self.pwm_signal))
                old_data = data

            if not self.is_active:
                self.servo.deinit()
                self.servo = PWM(Pin(18))
                self.servo.freq(50)
                
    def menu(self):
        print(" 1: Command Line Control")
        print(" 2: POT Control")
        print(" 3: GUI Control")
        # Take input from user
        self.user_input = input()

        # Call function
        if self.user_input == "1":
            print("Command Line Control - Please write an angle in degrees")
            self.step3()

        # Call function
        if self.user_input == "2":
            print("POT Control")
            self.step4()
        
        # Call function
        if self.user_input == "3":
            print("GUI Control")
            self.step5()

if __name__ == '__main__':
    try:
        Lab5()
    except:
        print("Unknown error :(")

