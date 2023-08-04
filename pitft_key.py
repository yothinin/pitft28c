#!/usr/bin/python  

import RPi.GPIO as GPIO  
import time    
import os  

#Set GPIO mode  
GPIO.setmode(GPIO.BCM)  

#Setup GPIO  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

#Give the system a quick break  
time.sleep(0.5)  

#Set the intitial counter value to zero  
counter = 0 

#var for the 'while' statement to keep it running  
var = 1 

#Main program  
while var == 1:
  if (GPIO.input(27) == False):
    print ("Previous song")
    time.sleep(0.5)  

  if (GPIO.input(23) == False):  
    print("Play/Pause")  
    time.sleep(0.5)  

  if (GPIO.input(22) == False):  
    print("Stop")  
    time.sleep(0.5)  

  if (GPIO.input(17) == False):
    print ("Next song")
    time.sleep (0.5)

  if GPIO.input(17) == False and GPIO.input(27) == False:
    print("Buttons 23 and 27 pressed together. Shutdown!")
    os.system("sudo halt")

GPIO.cleanup() 
