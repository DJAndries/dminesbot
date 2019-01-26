import random

class TileWithNeighbors:
    def __init__(self):
        self.center = None
        self.neighbors = dict()

class Action:
    def __init__(self, tile, is_flag, is_danger):
        self.tile = tile
        self.is_flag = is_flag
        self.is_danger = is_danger

    def __str__(self):
        return 'X: ' + str(self.tile.x) + ' Y: ' + str(self.tile.y) + \
            ' Flag: ' + str(self.is_flag)

def get_tile_info(gameparams, board, x, y):
    result = TileWithNeighbors()
    result.center = board[y][x]
    if x - 1 >= 0:
        result.neighbors['l'] = board[y][x - 1]
        if y - 1 >= 0:
            result.neighbors['ul'] = board[y - 1][x - 1]
            result.neighbors['u'] = board[y - 1][x]
        if y + 1 < gameparams.tiles_height:
            result.neighbors['dl'] = board[y + 1][x - 1]
            result.neighbors['d'] = board[y + 1][x]
    if x + 1 < gameparams.tiles_width:
        result.neighbors['r'] = board[y][x + 1]
        if y - 1 >= 0:
            result.neighbors['ur'] = board[y - 1][x + 1]
            result.neighbors['u'] = board[y - 1][x]
        if y + 1 < gameparams.tiles_height:
            result.neighbors['dr'] = board[y + 1][x + 1]
            result.neighbors['d'] = board[y + 1][x]

    return result

def equal_flag_scan(tile):
    covered_or_flagged = 0
    covered_tiles = set()

    for nval in tile.neighbors.values():
        if nval.val < 0:
            covered_or_flagged += 1
            if nval.val == -1:
                covered_tiles.add(Action(nval, True, False))

    if covered_or_flagged == tile.center.val:
        return covered_tiles
    return None

def already_flagged_scan(tile):
    flagged = 0
    covered_tiles = set()

    for nval in tile.neighbors.values():
        if nval.val == -2:
            flagged += 1
        if nval.val == -1:
            covered_tiles.add(Action(nval, False, False))

    if flagged == tile.center.val:
        return covered_tiles
    return None

def one_in_x_scan(tile, x):
    if tile.center.val == 1:
        return None

    flagged = 0
    candidates = set()

    for nval in tile.neighbors.values():
        if nval.val == -2:
            flagged += 1
        if nval.val == -1:
            candidates.add(Action(nval, False, True))

    if (tile.center.val - flagged) == 1 and len(candidates) == x:
        return set(random.sample(candidates, 1))
    return None

def scan_tile_action(gameparams, board, x, y):
    tile = get_tile_info(gameparams, board, x, y)

    if tile.center.val <= 0:
        return None

    actions = equal_flag_scan(tile)
    if actions:
        return (actions, 1, True)

    actions = already_flagged_scan(tile)
    if actions:
        return (actions, 2, True)

    actions = one_in_x_scan(tile, 3)
    if actions:
        return (actions, 3, False)

    actions = one_in_x_scan(tile, 2)
    if actions:
        return (actions, 4, False)

    return None


def scan(gameparams, board):
    current_action_priority = 256
    actions = set()
    for y in range(0, gameparams.tiles_height):
        for x in range(0, gameparams.tiles_width):
            tile_actions = scan_tile_action(gameparams, board, x, y)
            if tile_actions is None:
                continue
            if tile_actions[1] < current_action_priority:
                current_action_priority = tile_actions[1]
                actions = tile_actions[0]
            elif tile_actions[1] == current_action_priority:
                if tile_actions[2]:
                    actions.update(tile_actions[0])
                else:
                    actions = tile_actions[0]

    if current_action_priority > 2 and len(actions) > 0 and random.random() > 0.5:
        actions = {random_action(gameparams, board)}

    if len(actions) == 0:
        actions.add(random_action(gameparams, board))
    return actions

def print_actions(actions):
    for action in actions:
        print(str(action))

def random_action(gameparams, board):
    y = int(random.random() * gameparams.tiles_height)
    x = int(random.random() * gameparams.tiles_width)
    return Action(board[y][x], False, True)
