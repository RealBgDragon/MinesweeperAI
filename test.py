import pyautogui
from PIL import Image


X_START = 313
Y_START = 252
WIDTH = 600
HEIGHT = 320

X_GRID_SIZE = 30
Y_GRID_SIZE = 16
BOX_SIZE = 20

CLICKED = (155, 155, 155)
NOT_CLICKED = (255, 255, 255)

ONE = (0, 0, 255)
TWO = (0, 255, 0)
THREE = (255, 0, 0)

SIX = (0, 123, 123)

# Rectangle: left-X, top-Y, width, height
box = (X_START, Y_START, WIDTH, HEIGHT)
img = pyautogui.screenshot(region=box)

for i in range(X_GRID_SIZE):
    for j in range(Y_GRID_SIZE):
        pixel = img.getpixel((i*BOX_SIZE + 1, j*BOX_SIZE + 1))
        # print("Pos: ", i*BOX_SIZE + 1, j*BOX_SIZE + 1)
        if pixel == NOT_CLICKED:
            print("Not clicked")
        elif pixel == CLICKED:
            number = img.getpixel((i*BOX_SIZE + 13, j*BOX_SIZE + 15))
            print("Pos: ", i*BOX_SIZE + 13, j*BOX_SIZE + 15)
            print("Clicked")
            if number == ONE:
                print("one")
            if number == TWO:
                print("two")
            if number == THREE:
                print("three")
                
                

img.show()                            # pops a window
