import win32api
import random
import time
#import pyautogui
import pydirectinput
from datetime import datetime

opciones = ["up", "down", "left", "right", "space", "tab", "esc", "home", "end", "pageup", "pagedown"];

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

cont = 0
while 1 == 1:
    cont += 1
    x = random.randrange(1, 1000)
    y = random.randrange(1, 1000)
    win32api.SetCursorPos((x, y))
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    if cont == 10:
        #pydirectinput.click(button='right')
        #pydirectinput.press('esc')	
        opcion = random.choice(opciones)
        pydirectinput.press(opcion)
        #print(cont, " ", opcion)
        cont = 0
    time.sleep(random.randrange(1, 10))
