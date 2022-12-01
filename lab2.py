# Import modules
from machine import Pin, ADC
import network, time, socket

ssid = 'AndroidAP3E19'          # WIFI ID
password = 'navq1475'           # WIFI Password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Global game variables
health1 = 1
health2 = 1
score1 = 0
score2 = 0
start_flag_xor = 0
start_flag_bcs = 0
turn = 1
pongspeed = 100

# Interrupt variables
interrupt_flagL = 0
interrupt_flagR = 0
debounce_time = 0
stopper = True




# 8 LEDs from 2 to 9
LED = []
for i in range(2,10):
    LED.append(Pin(i, Pin.OUT, value=0))
    
# Interrupt function for left button
def left_lower(pin):
    global interrupt_flagL, debounce_time
    if (time.ticks_ms()-debounce_time) > 500:
        interrupt_flagL = 1
        debounce_time = time.ticks_ms()

# Interrupt function for right button
def right_lower(pin):
    global interrupt_flagR, debounce_time, stopper
    if (time.ticks_ms()-debounce_time) > 500:
        interrupt_flagR = 1
        debounce_time = time.ticks_ms()

    elif 300 < (time.ticks_ms()-debounce_time) and (time.ticks_ms()-debounce_time) < 700:
        stopper = not stopper
        print("double clicked")
        debounce_time = time.ticks_ms()

# Registering the button Pins and its interrupt requests
left_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
right_button = Pin(22, Pin.IN, Pin.PULL_UP)
left_button.irq(trigger=Pin.IRQ_FALLING, handler=left_lower)
right_button.irq(trigger=Pin.IRQ_FALLING, handler=right_lower)

# Define every pin again
def reset():
    for i in range(2,10):
        Pin(i, Pin.OUT, value=0)

# Displays the given value in binary representation
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

# Counts from 0 to 255, counting speed can be changed by buttons
def Count():

    # Counter, speed and tick variables
    counter = 0
    countspeed = 1000
    varTick = 1
    # Interrupt flags
    global interrupt_flagL, interrupt_flagR

    while True:

        varTick = varTick + 1
        if varTick > 2**15:
            varTick = 1
        
        if stopper:
            if interrupt_flagL is 1:
                countspeed = int(countspeed * 2)
                interrupt_flagL = 0
                print("Slowed Down")
            elif interrupt_flagR is 1:
                if countspeed > 3:
                    countspeed = int(countspeed / 2)
                    print("Fastened")
                else:
                    print("Maximum speed is reached")
                interrupt_flagR = 0

            ByteDisplay(counter)

            if counter < 255:
                if (varTick%countspeed == 0):
                    counter = counter + 1
            else:
                counter = 0

# Single player pong game    
def LEDPong():
    
    # Game variables
    health = 10
    score = 0
    backward = 0
    shoot = 0
    temp_time = -1
    counter = 1
    varTick = 1
    pot_value5 = 1
    pot_value6 = 0
    time5 = 1
    time6 = 0
    pongspeed = 100
    global interrupt_flagL, interrupt_flagR
    start_time = time.time()
    end_time = 30
    adc = ADC(26)

    while True:
        
        # Check game ending conditions:
        # If time is greater than end game time -> Finish
        # If first player has no health -> Finish
        if (time.time() - start_time > end_time) or (health == 0):
            print("Game over")
            print("Your score is: " + str(score))
            for i in range(5):
                ByteDisplay(255)
                time.sleep(0.1)
                reset()
                time.sleep(0.1)
            reset()
            break
        
        # Count the remaining time
        # If there are more than 10 seconds print only multiples of 5
        # If there are less than 10 seconds print every seconds
        if (int(time.time() - start_time) < (end_time - 10)):
            if (int(time.time() - start_time)%5 == 0):
                current_time = int(time.time() - start_time)
                if not(current_time == temp_time):
                    print("Remaining Time: ", end="")
                    print(end_time - current_time)
                    temp_time = current_time
        else:
            current_time = int(time.time() - start_time)
            if not(current_time == temp_time):
                print("Remaining Time: ", end="")
                print(end_time - current_time)
                temp_time = current_time
        
        # Increase tick in every loop
        varTick = varTick + 1
        if varTick > 2**10:
            varTick = 1
        
        if not shoot:
            if counter == 2**5 and backward == 0:
                pot_value5 = int(adc.read_u16() / 65535 * 100000)
                time5 = time.ticks_ms()
            if (counter == 2**6 or counter == 2**7) and backward == 0:
                pot_value6 = int(adc.read_u16() / 65535 * 100000)
                time6 = time.ticks_ms()
                if abs(pot_value5 - pot_value6) > 1000:
                    pongspeed = int(20000/(int(abs(pot_value5 - pot_value6) / abs(time5 - time6))))
                    if pongspeed < 50:
                        pongspeed = 50
                    if pongspeed > 150:
                        pongspeed = 150
                    shoot = not shoot
                    score += 200 - pongspeed
                    print("Your score is: " + str(score))      

        ByteDisplay(counter)

        # If the ball is coming to you
        if backward == 0:
            if (varTick%pongspeed == 0):
                counter = counter * 2

            # If the ball is in the closest LED
            if counter == 2**7:
                backward = not backward

                # If you weren't able to shoot, you will lose health and score
                if not shoot:
                    health -= 1
                    score -= 200
                    counter = 1
                    backward = not backward
                    pongspeed = 100
                    reset()
                    print("Your score is: " + str(score))
                    print("Remaining health is: " + str(health))
                    print("Press any button to continue")
                    while True:
                        if interrupt_flagR or interrupt_flagL:
                            interrupt_flagL = 0
                            interrupt_flagR = 0
                            break
        # If the ball is going to the wall
        else:
            if (varTick%pongspeed == 0):
                counter = int(counter / 2)
            # If the ball is in the furthest LED
            if (counter == 1):
                backward = not backward
                shoot = 0

# Multi player pong game
def KnowYourNeighbor():
    
    # Game variables
    backward = 0
    shoot = 0
    temp_time = -1
    end_time = 90
    start_time = time.time()
    counter = 1
    varTick = 1
    pot_value5 = 1
    pot_value6 = 0
    time5 = 1
    time6 = 0
    global pongspeed, interrupt_flagL, interrupt_flagR, health1, health2, score1, score2, turn
    adc = ADC(26)

    ai = socket.getaddrinfo("192.168.43.139", 1250) # Address of Web Server
    addr = ai[0][-1]

    # Create a socket and make a HTTP request
    cl = socket.socket() # Open socket
    cl.connect(addr)
    
    while True:
        
        
        gamedata = str(pongspeed) + "," + str(turn) + "," + str(score1) + "," + str(health1)
        response = gamedata # This is what we send in reply
        
        # cl.close()

        # Check game ending conditions:
        # If time is greater than end game time -> Finish
        # If first player has no health -> Finish
        # If second player has no health -> Finish
        if (time.time() - start_time > end_time) or (health1 == 0) or (health2 == 0):
            print("Game over")
            print("Your score is: " + str(score1))
            print("Opponent score is: " + str(score2))
            # Check who won the game
            if score1 > score2:
                print("You won !!!")
            elif score2 > score1:
                print("Opponent won :(")
            else:
                print("Draw")
            # Some cool light show
            for i in range(5):
                ByteDisplay(255)
                time.sleep(0.1)
                reset()
                time.sleep(0.1)
            # Reset and exit from the game
            reset()
            cl.close()
            break

        # Count the remaining time
        # If there are more than 10 seconds print only multiples of 5
        # If there are less than 10 seconds print every seconds
        if (int(time.time() - start_time) < (end_time - 10)):
            if (int(time.time() - start_time)%5 == 0):
                current_time = int(time.time() - start_time)
                if not(current_time == temp_time):
                    print("Remaining Time: ", end="")
                    print(end_time - current_time)
                    temp_time = current_time
        else:
            current_time = int(time.time() - start_time)
            if not(current_time == temp_time):
                print("Remaining Time: ", end="")
                print(end_time - current_time)
                temp_time = current_time
        
        # Increase tick in every loop
        varTick = varTick + 1
        if varTick > 2**16:
            varTick = 1
        
        # If it is your turn, you did not shoot and ball comes to you you can shoot
        if (turn == 1) and (shoot == 0) and (backward == 0):
            if counter == 2**5:
                pot_value5 = int(adc.read_u16() / 65535 * 100000)
                time5 = time.ticks_ms()
            if (counter == 2**6 or counter == 2**7):
                pot_value6 = int(adc.read_u16() / 65535 * 100000)
                time6 = time.ticks_ms()
                if abs(pot_value5 - pot_value6) > 1000:
                    pongspeed = int(20000/(int(abs(pot_value5 - pot_value6) / abs(time5 - time6))))
                    if pongspeed < 50:
                        pongspeed = 50
                    if pongspeed > 150:
                        pongspeed = 150
                    pongspeed = int(pongspeed / 2)
                    shoot = 1

        # If it is your turn LED representing the ball should be displayed 
        if turn == 1:
            ByteDisplay(counter)
            # If the ball is coming to you
            if backward == 0:
                if (varTick%pongspeed == 0):
                    counter = counter * 2
                # If the ball is in the closest LED
                if counter == 2**7:
                    # If you were able to shoot, ball will go to your opponent
                    if (shoot == 1):
                        backward = not backward
                    # If you weren't able to shoot, you will lose health and score
                    if (shoot == 0):
                        health1 -= 1
                        score1 -= 200
                        turn = 2
                        backward = not backward
                        pongspeed = 100
                        reset()
                        print("Your score is: " + str(score1))
                        print("Remaining health is: " + str(health1))
                        print("Opponent score is: " + str(score2))
                        print("Opponent's remaining health is: " + str(health2))

                        while True:
                            gamedata = str(pongspeed) + "," + str(turn) + "," + str(health1) + "," + "-1" + "," + str(score1) + "," + "-1"
                            response = gamedata # This is what we send in reply
                            reset()
                            request = cl.recv(1024)
                            print(request)
                            cl.send(response)
                            print("Sent:" + gamedata)
                            if (turn == 1):
                                break
            # If the ball is going to your opponent
            else:
                if (varTick%pongspeed == 0):
                    counter = int(counter / 2)
                # If the ball is in the furthest LED, your opponent takes turn
                if (counter == 1):
                    ByteDisplay(counter)
                    backward = not backward
                    turn = 2
                    shoot = 0
                    # Send your opponent the ball and its speed
                    gamedata = str(pongspeed) + "," + str(turn) + "," + str(health1) + "," + "-1" + "," + str(score1) + "," + "-1"
                    response = gamedata # This is what we send in reply
                    reset()
                    cl.send(response)
                    print("Sent:" + gamedata)

        else:
            cl.send("-1,-1,-1,-1,-1,-1")
            request = str(cl.recv(1024))
            print(request)
            data = request.split(",")
            pongspeed = int(int(data[0][2:]) / 3)
            turn = int(data[1])
            try:
                score2 = int(data[5][:-1])
            except:
                score2 = int(data[5][:-2])
            health2 = int(data[3])
            print(pongspeed)

# Orchestrate
def Menu():

    # Global variables
    global interrupt_flagL, interrupt_flagR, start_flag_xor, start_flag_bcs
    # Call Menu with reseting PINs
    reset()
    # Menu instructions
    print("Tasks are given below, please enter one of the numbers on the left.")
    print(" 1: Count - Starts to count numbers from 0 to 255")
    print(" 2: LED Pong - Single player pong game")
    print(" 3: LED Pong - Multi player pong game")
    # Take input from user
    user_input = input()
    
    # Call Count function
    if user_input == "1":
        print("Press left button to count faster and right button to count slower")
        print("If right button is double clicked, counting will stop")
        Count()
    
    # Call Single Player LED Pong Game
    elif user_input == "2":
        print("Press any button to start game")
        while True:
            if interrupt_flagL or interrupt_flagR:
                interrupt_flagL = 0
                interrupt_flagR = 0
                LEDPong()
                break

    # Call Multi Player LED Pong Game
    if user_input == "3":
        KnowYourNeighbor()

    else:
        print("Invalid input")

# Initialize program with calling menu
Menu()