import pyautogui, sys
import time, random

__version__ = '0.1.0'

def move_cursor(every_n_seconds: int = 10):
    width, height = pyautogui.size()
    try:
        while True:
            x, y = pyautogui.position()
            a = random.randint(1, width-1)
            b = random.randint(1, height-1)
            pyautogui.moveTo(a, b, 2)
            time.sleep(every_n_seconds)
    except KeyboardInterrupt:
        return
