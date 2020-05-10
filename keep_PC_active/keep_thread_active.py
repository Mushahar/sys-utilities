#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides functionality to keep a system state as active.

Prevents Windows from turning the display off and setting the system state to idle
"""

# imports
from ctypes import windll
import time
import os

# variables with simple values
ES_CONTINUOUS = 0x80000000          # state being set should remain in effect until the next call with ES_CONTINUOUS
ES_DISPLAY_REQUIRED = 0x00000002    # Forces the display to be on by resetting the display idle timer
ES_SYSTEM_REQUIRED = 0x00000001     # Forces the system to be in the working state by resetting the system idle timer
sleep_time = 45                   # Time (in sec) for main loop to sleep for


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


if __name__ == '__main__':

    keep_system_and_display_active()

    while True:
        try:
            time.sleep(sleep_time)      # Yield CPU resource
        except Exception:
            # Bring back to normal state i.e. thread not keeping system or display active
            bring_to_normal()
            break
