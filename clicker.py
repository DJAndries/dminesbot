import pyautogui

pyautogui.PAUSE = 0.01

class ActionResult:
    def __init__(self, requires_scan, danger_actions):
        self.requires_scan = requires_scan
        self.danger_actions = danger_actions

def get_coords(gameparams, action):
    tile_width = int(gameparams.width / gameparams.tiles_width)
    tile_height = int(gameparams.height / gameparams.tiles_height)
    x = int(gameparams.x + (action.tile.x * tile_width) + (tile_width / 2))
    y = int(gameparams.y + (action.tile.y * tile_height) + (tile_height / 2))
    return (x, y)

def flag_tile(gameparams, action):
    coords = get_coords(gameparams, action)

    pyautogui.click(x=coords[0], y=coords[1], button='right')
    action.tile.val = -2

def click_tile(gameparams, action):
    coords = get_coords(gameparams, action)

    pyautogui.click(x=coords[0], y=coords[1], button='left')

def process_actions(gameparams, actions):
    result = ActionResult(False, False)

    for action in actions:
        if action.tile.val != -1:
            continue
        if action.is_danger:
            if not result.danger_actions:
                result.danger_actions = set()
            result.danger_actions.add(action)
        if action.is_flag:
            flag_tile(gameparams, action)
        else:
            click_tile(gameparams, action)
            result.requires_scan = True
    return result
