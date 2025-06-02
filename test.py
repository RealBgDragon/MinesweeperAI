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
            if pixel == NOT_CLICKED:
                # print("Not clicked")
                tiles[i][j] = 0
            elif pixel == CLICKED:
                number = img.getpixel((i*BOX_SIZE + 13, j*BOX_SIZE + 15))
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
    for i in range(len(tiles)):
        print(tiles[i])
        
    for i in range(X_GRID_SIZE):
        for j in range(Y_GRID_SIZE):
            empty_tiles = 0
            empty_tiles_coordinates = []
            # check if the tile is a 1
            if tiles[i][j] == 1:
                # run trough each element next to the current
                empty_tiles, empty_tiles_coordinates = AdjacentElements(i, j)
                                
                if empty_tiles == 1:
                    Click(empty_tiles_coordinates)
            
            # check if the tile is a 2
            if tiles[i][j] == 2:
                # run trough each element next to the current
                empty_tiles, empty_tiles_coordinates = AdjacentElements(i, j)
                                
                if empty_tiles == 2:
                    Click(empty_tiles_coordinates)
      
def AdjacentElements(i, j):
    empty_tiles = 0
    empty_tiles_coordinates = []

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

    return empty_tiles, empty_tiles_coordinates

def Click(empty_tiles_coordinates):
    current_coordinates = empty_tiles_coordinates[0]
    if (current_coordinates not in clicked_coordinates) and tiles[current_coordinates[0]][clicked_coordinates[1]] != 10:
        clicked_coordinates.append(current_coordinates)

        x = X_START + current_coordinates[0] * BOX_SIZE
        y = Y_START + current_coordinates[1] * BOX_SIZE

        print("Click:", x, y)
        pyautogui.moveTo(x, y)
        pyautogui.rightClick()

def __main__():
    TakeIamge()
    MakeMove()

__main__()