from machine import Pin, PWM, ADC
import time

# Maximum value given for the PWM // used in Snake
tVal = 2**16 - 2

# 8 LEDs from 2 to 9
LED = []
for i in range(2,10):
    LED.append(Pin(i, Pin.OUT, value=0))

# Registering the button Pins
left_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
right_button = Pin(22, Pin.IN, Pin.PULL_UP)

def reset():
    for i in range(2,10):
        Pin(i, Pin.OUT, value=0)

def ByteDisplay(val=0):
    
    # Setting off all the LEDs.
    reset()
    # Setting the limiting values to the 0 - 255 as we have 8 bits.
    if 0 <= val <= 255:
        # Converting the input to binary. 
        # In order to achieve the indexes of the byte, we then convert it to string.
        binary = str(bin(val))[2:]

        # 0 gives the index error in the for loop and since all LEDs are off when it is 0, we excluded it.
        if int(binary) > 0:
            # from the "binary" string, each LED value is set one by one. 
            for i in range(len(binary)):
                LED[i].value(int(binary[len(binary)-i - 1]))
    else:
        print("You entered a number that cannot be represented by unsigned 8 bits")

def Volta(N=1, speed=0.1):
    
    # Initializing the first LED
    LED[0].value(1)
    time.sleep(speed)
    LED[0].value(0)   
    
    # Looping through the LEDs.
    while(N):

        # LEDs are runnning forward
        for i in range(7):
            LED[i+1].value(1)
            time.sleep(speed)
            LED[i+1].value(0)
        
        # LEDs are running backward.
        for i in range(7):
            LED[6-i].value(1)
            time.sleep(speed)
            LED[6-i].value(0)
        
        # Tracking the loop count
        N = N - 1


def Snake(L=4, speed=0.3):
    LEDs = []
    if L < 5 and isinstance(L, int):
        for i in range(8):
            LEDs.append(PWM(LED[i]))
        LEDs[0].duty_u16(tVal)
        time.sleep(speed)
        for i in range(7+L):
            if (i+1) < 8:
                LEDs[i+1].duty_u16(tVal)
            for k in range(L):
                if (i-k) >= 0 and (i-k) < 8:
                    LEDs[i-k].duty_u16(int(tVal/(4*(k+1))))
            time.sleep(speed)
            for i in range(8):
                LEDs[i].duty_u16(0)
        for i in range(7+L):
            if 6-i > 0:
                LEDs[6-i].duty_u16(tVal)
            for k in range(L+1):
                if (6-i+k) >= 0 and (6-i+k) < 7:
                    LEDs[6-i+k].duty_u16(int(tVal/(4*(k+1))))
            time.sleep(speed)
            for i in range(8):
                LEDs[i].duty_u16(0)

        for i in range(8):
            LEDs[i].duty_u16(0)
        LEDs = []
    else:
        print("L can have a maximum value of 4")


def ButtonCounter():
    temp_left = True
    temp_right = True
    sec = str(int(time.time()))
    initial_val = int(int(sec[-3:]) / 999 * 255)
    ByteDisplay(initial_val)

    while True:
        if temp_left:
            if left_button.value() == 1:
                initial_val -= 1
                ByteDisplay(initial_val)
                temp_left = False
                print(str(initial_val) + " is displayed")
        else:
            if left_button.value() == 0:
                temp_left = True

        if temp_right:
            if right_button.value() == 0:
                initial_val += 1
                ByteDisplay(initial_val)    
                temp_right = False
                print(str(initial_val) + " is displayed")

        else:
            if right_button.value() == 1:
                temp_right = True
        
        time.sleep(0.02)


def Digital_UV_Meter():
    
    # create an ADC object acting on a pin
    adc = ADC(26)        
    while True:
        # Pot value is readed between 0-65535 and mapped into 0-255
        pot_value = int(adc.read_u16() / 65535 * 255)
        print(str(pot_value) + " is displayed")
        # Readed pot value is displated
        ByteDisplay(pot_value)
        time.sleep(0.1)


def Thermometer():
    sensor_temp = ADC(4)
    conversion_factor = 3.3 / (65535)

    while True:
        reading = sensor_temp.read_u16() * conversion_factor 
        temperature = 27 - (reading - 0.706)/0.001721
        print(temperature)
        ByteDisplay(int(Temperature))
        time.sleep(2)

def Menu():
    reset()
    print("Tasks are given below, please enter one of the numbers on the left.")
    print(" 2: Byte Display - Number you enter will be displayed on the LEDs")
    print(" 3: Walking Lights - ")
    print(" 4: Walking & Fading Lights - ")
    print(" 5: Button Counter - LEDs are changing according to button press")
    print(" 6: Digital VU meter - LEDs are changing according to potantiometer value")
    print(" 7: Thermometer - Temperature of the room is displayed on the LEDs")
    user_input = input()
    
    if user_input == "2":
        print("Please enter an integer")
        user_val = input()
        ByteDisplay(int(user_val))

    elif user_input == "3":
        print("Please enter an integer and a float seperated by space.")
        print("  1- For the loop count")
        print("  2- For the sleep time between two LEDs")
        user_val = input()
        arr = user_val.split(' ')
        Volta(int(arr[0]), float(arr[1]))

    elif user_input == "4":
        print("Please enter an integer and a float  seperated by space.")
        print("  1- For the loop count")
        print("  2- For the sleep time between two LEDs")
        user_val = input()
        arr = user_val.split(' ')
        Snake(int(arr[0]), float(arr[1]))

    elif user_input == "5":
        print("Please press the buttons")
        ButtonCounter()

    elif user_input == "6":
        print("Please turn the potantiometer")
        Digital_UV_Meter()

    elif user_input == "7":
        print("Thermomater is starting...")
        Thermometer()

    else:
        print("Invalid input")

Menu()
