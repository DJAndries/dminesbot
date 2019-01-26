import math, pyautogui, mss, mss.tools

COLOR_MAP = {
    (127, 215, 255): -1,
    (25, 190, 224): 1,
    (118, 153, 32): 2,
    (78, 94, 37): 2,
    (221, 38, 110): 3,
    (225, 49, 118): 3,
    (26, 87, 201): 4,
    (181, 25, 25): 5,
    (25, 121, 48): 6
}

GAME_OVER_SCREEN_BLACK_COUNT = 100000
PIXEL_COLOR_DISTANCE_TOLERANCE = 16
TILE_ID_RADIUS = 6

class Tile:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val

def dst(x, y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

def identify_tile(im, gameparams, x, y):
    tile_width = gameparams.width / gameparams.tiles_width
    tile_height = gameparams.height / gameparams.tiles_height
    mid_x = int(tile_width / 2)
    mid_y = int(tile_height / 2)

    start_x = int(tile_width * x) + mid_x
    start_y = int(tile_height * y) + mid_y

    for x in range(start_x - TILE_ID_RADIUS, start_x + TILE_ID_RADIUS):
        for y in range(start_y - TILE_ID_RADIUS, start_y + TILE_ID_RADIUS):
            pixel_value = im.pixels[y][x]
            for tile_pixel_key, tile_pixel_value in COLOR_MAP.items():
                if dst(tile_pixel_key, pixel_value) < PIXEL_COLOR_DISTANCE_TOLERANCE:
                    return tile_pixel_value
    return 0

def print_scan(scan):
    for row in scan:
        line = ''
        for cell in row:
            line += ('*' if cell.val < 0 else str(cell.val)) + ' '
        print(line)

def init_board(gameparams):
    result = []
    for y in range(0, gameparams.tiles_height):
        row = []
        for x in range(0, gameparams.tiles_width):
            row.append(Tile(x, y, -1))
        result.append(row)
    return result

def game_over_scan(gameparams, cap, danger_actions):
    tile_width = int(gameparams.width / gameparams.tiles_width)
    tile_height = int(gameparams.height / gameparams.tiles_height)

    for action in danger_actions:
        print(cap.pixels[action.tile.y * tile_height + 12][action.tile.x * tile_width + 12])
        if dst(cap.pixels[action.tile.y * tile_height + 12][action.tile.x * tile_width + 12], (241, 241, 241)) > 164:
            mss.tools.to_png(cap.rgb, cap.size, output='killer.png')
            return True
    return False

def scan(gameparams, board, cap):
    for y in range(0, gameparams.tiles_height):
        for x in range(0, gameparams.tiles_width):
             if board[y][x].val != -1:
                 continue
             board[y][x].val = identify_tile(cap, gameparams, x, y)
