import socket
import network
import time
from machine import Pin, PWM, ADC


class Lab6():

    def __init__(self) -> None:
        self.IN1 = Pin(16,Pin.OUT)
        self.IN2 = Pin(17,Pin.OUT)
        self.IN3 = Pin(18,Pin.OUT)
        self.IN4 = Pin(19,Pin.OUT)
        self.pins = [self.IN1, self.IN2, self.IN3, self.IN4]
        self.steps = [
            [self.IN1],
            [self.IN1, self.IN2],
            [self.IN2],
            [self.IN2, self.IN3],
            [self.IN3],
            [self.IN3, self.IN4],
            [self.IN4],
            [self.IN4, self.IN1],
        ]
        self.current_step = 0
        self.menu()

    def set_pins_low(self, pins):
        [pin.low() for pin in pins]

    def set_pins_high(self, pins):
        [pin.high() for pin in pins]

    def menu(self):
        print(" 1: GUI")
        print(" 2: Gear Ratio")
        # Take input from user
        self.user_input = input()

        # Call function
        if self.user_input == "1":
            print("Stepper motor control with GUI")
            self.stepper()

        # Call function
        if self.user_input == "2":
            print("Gear ratio calculations")
            self.step5()

    def rotate(self, delay):
        sum_ = 0
        while True:
            high_pins = self.steps[self.current_step]
            self.set_pins_low(self.pins)
            self.set_pins_high(high_pins)
            self.current_step += 1
            if self.current_step == len(self.steps):
                self.current_step = 0
            sum_ += delay
            if sum_ > 1000:
                return        
            time.sleep(delay/1000)
    
    def step5(self):
        count = 0
        while True:
            high_pins = self.steps[self.current_step]
            self.set_pins_low(self.pins)
            self.set_pins_high(high_pins)
            self.current_step += 1
            if self.current_step == len(self.steps):
                self.current_step = 0
            count += 1
            print(count)
            if count > 4096:
                return        
            time.sleep(0.002)
            
    def stepper(self):
        #"""
        ssid = 'Galaxy A32AE20'          # WIFI ID
        password = 'qgfb9519'           # WIFI Password

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        ai = socket.getaddrinfo("192.168.8.141", 1236) # Address of Web Server
        addr = ai[0][-1]
        self.cl = socket.socket() # Open socket
        self.cl.connect(addr)
        #"""
        # Create a socket and make a HTTP request

        old_data = ""
        while True:
            self.cl.send(str.encode("2"))  # send message
            data = self.cl.recv(1024).decode()  # receive response
            data = data.split(",")

            if old_data != data[1] or int(data[2][:-1]):
                if int(data[2][:-1]):
                    self.rotate(int(data[0][1:]))
                    continue
                high_pins = self.steps[self.current_step]
                self.set_pins_low(self.pins)
                self.set_pins_high(high_pins)
                self.current_step += 1 
                old_data = data[1]
                if self.current_step == 8:
                    self.current_step = 0
                
Lab6()

