import keyboard, win32gui, time
import json, os

GAMEPARAMS_SAVE_FILE = 'last_gameparams.json'

class GameParams:
    pass

def save_gameparams():
    f = open(GAMEPARAMS_SAVE_FILE, 'w')
    json.dump(gameparams.__dict__, f)
    f.close()

def load_gameparams():
    global gameparams
    if not os.path.isfile(GAMEPARAMS_SAVE_FILE):
        return False
    f = open(GAMEPARAMS_SAVE_FILE, 'r')
    parsed_params = json.load(f)
    f.close()

    gameparams.__dict__.update(parsed_params)

    return True

def gselect(args):
    global root, gameparams
    gameparams = GameParams()

    if (len(args) < 2 or args[1] != 'grab') and load_gameparams():
        return gameparams

    print('Place mouse over top left corner of game grid, and press o.')
    while not keyboard.is_pressed('o'):
        pass
    x, y = win32gui.GetCursorPos()
    gameparams.x = x
    gameparams.y = y

    time.sleep(1)

    print('Place mouse over bottom right corner of game grid, and press o.')
    while not keyboard.is_pressed('o'):
        pass
    x, y = win32gui.GetCursorPos()
    gameparams.width = x - gameparams.x
    gameparams.height = y - gameparams.y

    gameparams.tiles_width = int(input('Enter the number of tiles for the width: '))
    gameparams.tiles_height = int(input('Enter the number of tiles for the height: '))

    save_gameparams()

    return gameparams
