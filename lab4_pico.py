import socket
import network
import time
from machine import Pin, PWM, ADC

ssid = 'Galaxy A32AE20'          # WIFI ID
password = 'qgfb9519'           # WIFI Password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

class Lab4():

    def __init__(self) -> None:
        self.left_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.right_button = Pin(22, Pin.IN, Pin.PULL_UP)
        self.ena = PWM(Pin(2, Pin.OUT))
        self.ena.duty_u16(0)
        self.ena.freq(1000)
        self.in1 = Pin(4, Pin.OUT)
        self.in2 = Pin(5, Pin.OUT)
        self.debounce_time = 0
        self.left_button.irq(trigger=Pin.IRQ_FALLING, handler=self.left_lower)
        self.right_button.irq(trigger=Pin.IRQ_FALLING, handler=self.right_lower)
        self.rotation_flag = 0
        old_data = ""
        self.old_duty = 0
        self.old_frequency = 0
        #self.ena.init(freq=self.frequency, duty_ns=self.duty_cycle)

        #"""
        ai = socket.getaddrinfo("192.168.61.141", 1234) # Address of Web Server
        addr = ai[0][-1]

        # Create a socket and make a HTTP request
        self.cl = socket.socket() # Open socket
        self.cl.connect(addr)

        while True:
            time.sleep(0.2)
            self.cl.send(str.encode("2"))  # send message
            data = self.cl.recv(1024).decode()  # receive response
            if old_data != data:
                data = data.split(",")

                self.start_flag = int(data[0])
                self.motor_number = int(data[1])
                self.direction = int(data[2])
                self.duty_cycle = int(data[3])
                self.frequency = int(data[4])
                print(self.start_flag, self.motor_number, self.direction, self.duty_cycle, self.frequency)
                if not self.start_flag:
                    self.stop()
                    continue

                if self.direction == 0:
                    self.forward()

                elif self.direction == 1:
                    self.backward()
                
                elif self.direction == 2:
                    self.stop()

                if self.duty_cycle != self.old_duty:
                    self.ena.duty_u16(int(self.duty_cycle / 100 * 65536))
                    self.old_duty = self.duty_cycle

                if self.old_frequency != self.frequency:
                    self.ena.freq(self.frequency)
                    #self.ena.freq(self.frequency)
                    self.old_frequency = self.frequency

                old_data = data
    
        client_socket.close()  # close the connection
        #"""

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.ena.duty_u16(0)

    def start(self):
        pass
    
    def forward(self):
        self.in1.value(1)
        self.in2.value(0)

    def backward(self):
        self.in1.value(0)
        self.in2.value(1)

    def right_lower(self, pin):
        
        if (time.ticks_ms()- self.debounce_time) > 500:
            self.debounce_time = time.ticks_ms()
            self.forward()

    def left_lower(self, pin):
        
        if (time.ticks_ms()- self.debounce_time) > 500:
            self.debounce_time = time.ticks_ms()
            self.backward()



if __name__ == '__main__':
    Lab4()
