#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import curses
import subprocess

# Function to control MPD using MPC
def mpd_control(command):
    subprocess.call(["mpc", command])

# Function to get MPD status
def get_mpd_status():
    status = subprocess.check_output(["mpc"]).decode("utf-8")
    if "playing" in status:
        return "Playing"
    elif "paused" in status:
        return "Paused"
    else:
        return "Stopped"

# Function to display text on the screen
#def display_text(screen, mode, status, song_info):
#    screen.clear()
#    screen.addstr(0, 0, f"Mode {mode}: {'Play' if mode == MODE_PLAY else 'Volume'}")
#    screen.addstr(1, 0, f"Status: {status}")
#    screen.addstr(2, 0, f"Song Info: {song_info}")
#    screen.refresh()

def display_text(screen, mode, status, song_info, volume=None):
    screen.clear()
    screen.addstr(0, 0, f"Mode {mode}: {'Play' if mode == MODE_PLAY else 'Volume'}")
    screen.addstr(1, 0, f"Status: {status}")
    if volume is not None:
        screen.addstr(2, 0, f"Volume: {volume}")
    screen.addstr(4, 0, f"Song: \n{song_info}\n\n")
    if mode == MODE_PLAY:
      screen.addstr(25, 0, f"Mode   Play/Pause   Stop      Next")
    elif mode == MODE_VOLUME:
      screen.addstr(25, 0, f"Mode    Vol +5%    Vol -5%    Prev")      
    elif mode == MODE_SYSTEM:
      screen.addstr(25, 0, f"Mode                          Quit")      
    screen.refresh()

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Give the system a quick break
time.sleep(0.5)

# Set the initial counter value to zero
counter = 0

# Define the modes
MODE_PLAY = 1
MODE_VOLUME = 2
MODE_SYSTEM = 3

# Main program
def main(stdscr):
    global current_mode  # Declare current_mode as global

    current_mode = MODE_PLAY
    curses.curs_set(0)
    song_info = ""  # Variable to store song information
    mpd_status = ""  # Variable to store MPD status

    while True:
        if (GPIO.input(27) == False):
            current_mode = (current_mode + 1) % 3

            # Switch between MODE_PLAY and MODE_VOLUME
            current_mode = MODE_VOLUME if current_mode == MODE_PLAY else MODE_PLAY
            display_text(stdscr, current_mode, mpd_status, song_info)
            time.sleep(0.5)

        # Check button inputs based on the current mode
        if current_mode == MODE_PLAY:
            if (GPIO.input(23) == False):
                print("Play/Pause")
                mpd_control("toggle")
                time.sleep(0.5)

            if (GPIO.input(22) == False):
                print("Stop")
                mpd_control("stop")
                time.sleep(0.5)

            if (GPIO.input(17) == False):
                print("Next song")
                mpd_control("next")
                time.sleep(0.5)
        elif current_mode == MODE_VOLUME:
            if (GPIO.input(23) == False):
                command = ["mpc", "volume", "+5"]
                subprocess.run(command)
                time.sleep(0.5)

            if (GPIO.input(22) == False):
                command = ["mpc", "volume", "-5"]
                subprocess.run(command)
                time.sleep(0.5)

            if (GPIO.input(17) == False):
                print("Previous song")
                mpd_control("prev")
                time.sleep(0.5)
        elif current_mode == MODE_SYSTEM:
            if (GPIO.input(17) == False):
                print("Shutdown")
                os.system("sudo halt")  # Send shutdown command when GPIO 17 is pressed
                time.sleep(0.5)

        # Update song_info and mpd_status
        current_volume = subprocess.check_output(["mpc", "volume"]).decode("utf-8").strip()

        song_info = subprocess.check_output(["mpc", "current"]).decode("utf-8").strip()
        mpd_status = get_mpd_status()

        # Display the song_info and mpd_status
        #display_text(stdscr, current_mode, mpd_status, song_info)
        display_text(stdscr, current_mode, mpd_status, song_info, current_volume)

try:
    curses.wrapper(main)
finally:
    GPIO.cleanup()
