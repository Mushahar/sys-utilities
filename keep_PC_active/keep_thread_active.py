#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# This module provides functionality to keep a system state as active.
# Prevents Windows from turning the display off and setting the system state to idle
"""

# imports
from ctypes import windll
import time
import os

# constants with simple values
ES_CONTINUOUS = 0x80000000          # state being set should remain in effect until the next call with ES_CONTINUOUS
ES_DISPLAY_REQUIRED = 0x00000002    # Forces the display to be on by resetting the display idle timer
ES_SYSTEM_REQUIRED = 0x00000001     # Forces the system to be in the working state by resetting the system idle timer
TIME_TO_SLEEP = 45                  # Time (in sec) for main loop to sleep for


def keep_system_active():
    """ Keeps system state as active, but doesn't affect the display """
    if os.name == 'nt':
        windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)


def keep_display_active():
    """ Keeps the display ON """
    if os.name == 'nt':
        windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)


def keep_system_and_display_active():
    """ Keeps the system state as active and keeps the display ON """
    if os.name == 'nt':
        windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)


def bring_to_normal():
    """ Returns any previous settings for system state and display back to normal.
        System state may go to idle and display may turn off if no user activity
    """
    if os.name == 'nt':
        windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

def move_mouse():
	""" Generates a mouse event """
	windll.user32.mouse_event(0x0001, 0, 0, 0, None)


if __name__ == '__main__':

    try:
        while True:
            time.sleep(TIME_TO_SLEEP)      # Yield CPU resource
            keep_system_and_display_active()
            move_mouse()
    except KeyboardInterrupt:
        bring_to_normal()
        pass
