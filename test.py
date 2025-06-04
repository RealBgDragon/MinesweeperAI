import pyautogui
import keyboard
from PIL import Image
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

X_START = int(os.getenv("X_START"))
Y_START = int(os.getenv("Y_START"))
WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))

X_GRID_SIZE = int(os.getenv("X_GRID_SIZE"))
Y_GRID_SIZE = int(os.getenv("Y_GRID_SIZE"))
BOX_SIZE = int(os.getenv("BOX_SIZE"))
NUMBER_WIDTH = int(os.getenv("NUMBER_WIDTH"))
NUMBER_HEIGHT = int(os.getenv("NUMBER_HEIGHT"))

def get_color(name):
    return tuple(map(int, os.getenv(name).split(',')))

CLICKED = get_color("CLICKED")
NOT_CLICKED = get_color("NOT_CLICKED")

ONE = get_color("ONE")
TWO = get_color("TWO")
THREE = get_color("THREE")
FOUR = get_color("FOUR")
FIVE = get_color("FIVE")
SIX = get_color("SIX")

MINE = get_color("MINE")
moves = 0

tiles = [[0 for _ in range(Y_GRID_SIZE)] for _ in range(X_GRID_SIZE)]
clicked_coordinates = []
# coordinates = [[0 for _ in range(Y_GRID_SIZE)] for _ in range(X_GRID_SIZE)]

def TakeImage():
    # Rectangle: left-X, top-Y, width, height
    box = (X_START, Y_START, WIDTH, HEIGHT)
    img = pyautogui.screenshot(region=box)

    for i in range(X_GRID_SIZE):
        for j in range(Y_GRID_SIZE):
            pixel = img.getpixel((i*BOX_SIZE + 1, j*BOX_SIZE + 1))
            # print("Pos: ", i*BOX_SIZE + 1, j*BOX_SIZE + 1)
            number = img.getpixel((i*BOX_SIZE + NUMBER_WIDTH, j*BOX_SIZE + NUMBER_HEIGHT))
            if pixel == NOT_CLICKED:
                # print("Not clicked")
                if number == MINE:
                    tiles[i][j] = 11
                else: 
                    tiles[i][j] = 0
                    
            elif pixel == CLICKED:
                # print("Pos: ", i*BOX_SIZE + NUMBER_WIDTH, j*BOX_SIZE + NUMBER_HEIGHT)
                # print(number)
                if number == ONE:
                    tiles[i][j] = 1
                elif number == TWO:
                    tiles[i][j] = 2
                elif number == THREE:
                    tiles[i][j] = 3
                elif number == FOUR:
                    tiles[i][j] = 4
                else:
                    tiles[i][j] = 10
                                
def MakeMove():
    # for i in range(len(tiles)):
    #     print(tiles[i])
    
    for i in range(X_GRID_SIZE):
        for j in range(Y_GRID_SIZE):
            number = tiles[i][j]
            if number != 0 and number != 10 and number != 11:
                ProcessTile(i, j, tiles[i][j])
      
def AdjacentElements(i, j):
    empty_tiles = 0
    empty_tiles_coordinates = []
    flags = 0

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            ni = i + dx
            nj = j + dy

            if 0 <= ni < X_GRID_SIZE and 0 <= nj < Y_GRID_SIZE:
                neighbor = tiles[ni][nj]
                if neighbor == 0:
                    empty_tiles += 1
                    empty_tiles_coordinates.append([ni, nj])  # Store as list, not tuple for consistency
                if neighbor == 11:
                    flags += 1       
                
    return empty_tiles, empty_tiles_coordinates, flags

def Click(empty_tiles_coordinates, click):
    for current_coordinates in empty_tiles_coordinates:
        if (current_coordinates not in clicked_coordinates) and tiles[current_coordinates[0]][current_coordinates[1]] != 11 and tiles[current_coordinates[0]][current_coordinates[1]] != 10:
            clicked_coordinates.append(current_coordinates)

            x = X_START + current_coordinates[0] * BOX_SIZE
            y = Y_START + current_coordinates[1] * BOX_SIZE

            print("Click:", x, y)
            pyautogui.moveTo(x, y)
            if click == "right":
                pyautogui.rightClick()
                tiles[current_coordinates[0]][current_coordinates[1]] = 11
            elif click == "left":
                pyautogui.leftClick()
                tiles[current_coordinates[0]][current_coordinates[1]] = 10

def ProcessTile(i, j, number):
    empty_tiles, empty_tiles_coordinates, flags = AdjacentElements(i, j)

    if flags == number:
        Click(empty_tiles_coordinates, "left")

    if empty_tiles == number and flags == 0:
        Click(empty_tiles_coordinates, "right")
    elif empty_tiles + flags == number:
        Click(empty_tiles_coordinates, "right")

def __main__():
    TakeImage()
    MakeMove()

isRunning = True
last_toggle_time = 0

while True:
    if isRunning:
        __main__()
    if keyboard.is_pressed("k") and time.time() - last_toggle_time > 0.5:
        isRunning = not isRunning
        last_toggle_time = time.time()
    