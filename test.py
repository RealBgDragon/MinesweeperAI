import pyautogui
import keyboard
from PIL import Image
import time


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
TWO = (0, 123, 0)
THREE = (255, 0, 0)
MINE = (0, 0, 0)

SIX = (0, 123, 123)

moves = 0

tiles = [[0 for _ in range(Y_GRID_SIZE)] for _ in range(X_GRID_SIZE)]
clicked_coordinates = []
# coordinates = [[0 for _ in range(Y_GRID_SIZE)] for _ in range(X_GRID_SIZE)]

def TakeIamge():
    # Rectangle: left-X, top-Y, width, height
    box = (X_START, Y_START, WIDTH, HEIGHT)
    img = pyautogui.screenshot(region=box)



    for i in range(X_GRID_SIZE):
        for j in range(Y_GRID_SIZE):
            pixel = img.getpixel((i*BOX_SIZE + 1, j*BOX_SIZE + 1))
            # print("Pos: ", i*BOX_SIZE + 1, j*BOX_SIZE + 1)
            number = img.getpixel((i*BOX_SIZE + 13, j*BOX_SIZE + 15))
            if pixel == NOT_CLICKED:
                # print("Not clicked")
                if number == MINE:
                    tiles[i][j] = 11
                else: 
                    tiles[i][j] = 0
                    
            elif pixel == CLICKED:
                # print("Pos: ", i*BOX_SIZE + 13, j*BOX_SIZE + 15)
                # print("Clicked")
                if number == ONE:
                    tiles[i][j] = 1
                elif number == TWO:
                    tiles[i][j] = 2
                elif number == THREE:
                    tiles[i][j] = 3
                else:
                    tiles[i][j] = 10
                    
                                
def MakeMove():
    # for i in range(len(tiles)):
    #     print(tiles[i])
        
    for i in range(X_GRID_SIZE):
        for j in range(Y_GRID_SIZE):
            empty_tiles = 0
            empty_tiles_coordinates = []
            flags = 0
            # check if the tile is a 1
            if tiles[i][j] == 1:
                # run trough each element next to the current
                empty_tiles, empty_tiles_coordinates, flags = AdjacentElements(i, j)
                                
                if flags == 1:
                    Click(empty_tiles_coordinates, "left")
                
                if empty_tiles == 1:
                    Click(empty_tiles_coordinates, "right")
            
            # check if the tile is a 2
            if tiles[i][j] == 2:
                # run trough each element next to the current
                empty_tiles, empty_tiles_coordinates, flags = AdjacentElements(i, j)
                
                if flags == 2:
                    Click(empty_tiles_coordinates, "left")
                
                if empty_tiles == 2:
                    Click(empty_tiles_coordinates, "right")
                    print("Empty tiles: ", empty_tiles, "and flags: ", flags)
                elif empty_tiles == 1 and flags == 1:
                    print("Empty tiles: ", empty_tiles, "and flags: ", flags)
                    Click(empty_tiles_coordinates, "right")
      
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
        if (current_coordinates not in clicked_coordinates) and tiles[current_coordinates[0]][current_coordinates[1]] != 11:
            clicked_coordinates.append(current_coordinates)

            x = X_START + current_coordinates[0] * BOX_SIZE
            y = Y_START + current_coordinates[1] * BOX_SIZE

            print("Click:", x, y)
            pyautogui.moveTo(x, y)
            if click == "right":
                pyautogui.rightClick()
            elif click == "left":
                pyautogui.leftClick()


def __main__():
    TakeIamge()
    MakeMove()

isRunning = True
last_toggle_time = 0

while True:
    if isRunning:
        __main__()
    if keyboard.is_pressed("k") and time.time() - last_toggle_time > 0.5:
        isRunning = not isRunning
        last_toggle_time = time.time()
    