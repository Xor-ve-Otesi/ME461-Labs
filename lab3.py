from machine import Pin, PWM, ADC
import time

class Lab3:

    def __init__(self) -> None:
        self.qrd1_r = Pin(28, Pin.IN)
        self.qrd2_r = Pin(27, Pin.IN)
        self.qrd1_f = Pin(12, Pin.IN)
        self.qrd2_f = Pin(13, Pin.IN)
        self.left_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.right_button = Pin(22, Pin.IN, Pin.PULL_UP)
        self.servo = PWM(Pin(18))
        self.servo.freq(50)
        self.x1 = 1
        self.x2 = 2
        self.x3 = 3
        self.count = 0
        self.interrupt_count = 0
        self.debounce_time = 0
        self.left_button.irq(trigger=Pin.IRQ_FALLING, handler=self.left_lower)
        self.right_button.irq(trigger=Pin.IRQ_FALLING, handler=self.right_lower)
        self.qrd1_f.irq(trigger=Pin.IRQ_FALLING, handler= self.qrd1_fall)
        self.qrd1_r.irq(trigger=Pin.IRQ_RISING, handler= self.qrd1_rise)
        self.qrd2_f.irq(trigger=Pin.IRQ_FALLING, handler= self.qrd2_fall)
        self.qrd2_r.irq(trigger=Pin.IRQ_RISING, handler= self.qrd2_rise)
        self.x4_array = [[1,1],[0,1],[0,0],[1,0]]
        self.current_state = []
        self.temp_state = []
        self.distance = [[3000, 0], [3300, 0.1], [3500, 0.2], [5000, 0.3], [24000, 0.4], [35000, 0.5], [39000, 0.6], [43000, 0.7], [46000, 0.8], [51000, 0.9], [55000, 1], [59000, 1.5], [60000, 2]]
        self.user_input = 0
        self.angle = 12 * 10**5
        self.menu()
        
    def step4(self):
        while True:
            if self.x3 == self.interrupt_count:
                i = self.x4_array.index(self.current_state)
                    
                if self.temp_state == self.x4_array[(i+1)%4]:
                    self.count += 1
                    print(f"Count: {self.count}")
                    self.current_state = self.temp_state

                elif self.temp_state == self.x4_array[(i-1)%4]:
                    self.count -= 1
                    print(f"Count: {self.count}")
                    self.current_state = self.temp_state

    # Interrupt function for left button
    def left_lower(self, pin):

    
        if (time.ticks_ms()- self.debounce_time) > 500:
            self.debounce_time = time.ticks_ms()

            if self.user_input == "1":

                self.interrupt_count += 1 
                if self.interrupt_count == 1:
                    print("Encoding method changed to X1")
                elif self.interrupt_count == 2:
                    print("Encoding method changed to X2")
                elif self.interrupt_count == 3:
                    print("Encoding method changed to X4")
                self.current_state = [self.qrd1_r.value(), self.qrd2_r.value()]
                if self.interrupt_count == 4:
                    print("Encoding method changed to X1")
                    self.interrupt_count = 1

            elif self.user_input == "2":
                self.angle = self.angle + 300000
                if self.angle > 2600000:
                    self.angle = 2600000

    def right_lower(self, pin):
        
        if (time.ticks_ms()- self.debounce_time) > 500:
            self.debounce_time = time.ticks_ms()
            if self.user_input == "1":
                self.count = 0
                print("Count reset to zero")
                print(f"Count: {self.count}")
            elif self.user_input == "2":
                self.angle = self.angle - 300000
                if self.angle < 300000:
                    self.angle = 300000
            
    # Interrupt function for QRD1 Rise
    def qrd1_rise(self, pin):
        if self.interrupt_count == 1 or self.interrupt_count == 2:
            self.count += 1
            print(f"Count: {self.count}")
        if self.interrupt_count == 3:
            self.temp_state = [self.qrd1_r.value(), self.qrd2_r.value()]

    # Interrupt function for QRD1 Fall
    def qrd1_fall(self, pin):
        if self.interrupt_count == 2:
            self.count += 1
            print(f"Count: {self.count}")

        elif self.interrupt_count == 3:
            self.temp_state = [self.qrd1_r.value(), self.qrd2_r.value()]

    # Interrupt function for QRD2 Rise
    def qrd2_rise(self, pin):
        if self.interrupt_count == 3:
            self.temp_state = [self.qrd1_r.value(), self.qrd2_r.value()]

    # Interrupt function for QRD2 Fall
    def qrd2_fall(self, pin):
        if self.interrupt_count == 3:
            self.temp_state = [self.qrd1_r.value(), self.qrd2_r.value()]

    def step5(self):
        self.qrd = ADC(28)

        while True:        
            temp3 = 100000
            index = 0
            self.servo.duty_ns(self.angle)
            temp = self.qrd.read_u16()
            for i in range(len(self.distance)):
                temp2 = abs(temp - self.distance[i][0])
                if temp2 < temp3:
                    temp3 = temp2
                    index = i
            if self.distance[index][1] == 2:
                print("2+ cm")
            else:
                print(str(self.distance[index][1]) + " cm")
            time.sleep(0.2)

    def menu(self):
        print(" 1: Quadrature encoder")
        print(" 2: An analog sensor")
        # Take input from user
        self.user_input = input()

        # Call Count function
        if self.user_input == "1":
            print("Quadrature encoder. Press left button to start.")
            self.step4()

        # Call Count function
        if self.user_input == "2":
            print("An analog sensor")
            self.step5()

try:
    Lab3()
except:
    print("Unexpected error")