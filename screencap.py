import mss

sct = mss.mss()

def grab(gameparams):
    sct_img = sct.grab((gameparams.x, gameparams.y,
        gameparams.x + gameparams.width, gameparams.y + gameparams.height))

    return sct_img
