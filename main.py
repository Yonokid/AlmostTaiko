from cmu_graphics import *

from entry import *
from song_select import *
from game import *
from game_2p import *
from ai_battle import *
from result import *

#All images and sounds created by BANDAI NAMCO ENTERTAINMENT

def onAppStart(app):
    app.tja_folder_path = 'Songs'
    app.stepsPerSecond = 60

    #FPS counter variables
    app.current_ms = 0
    app.start_ms = 0
    app.last_ms = 0
    app.fps_display = 0

    app.sfx_don = sa.WaveObject.from_wave_file('Sounds/inst_00_don.wav')
    app.sfx_kat = sa.WaveObject.from_wave_file('Sounds/inst_00_katsu.wav')
    app.sfx_cancel = sa.WaveObject.from_wave_file('Sounds/Cancel.wav')

def main():
    runAppWithScreens(initialScreen='entry', width=1280,height=720)

main()
