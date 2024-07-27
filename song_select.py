from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os

from global_funcs import *
from game import play_tja

def song_select_onAppStart(app):
    #FPS counter vars
    app.current_ms = 0
    app.start_ms = 0
    app.last_ms = 0
    app.fps_display = 0
    
    app.stepsPerSecond = 60
    app.song_list = []
    app.song_metadata = []
    app.selected_song = 0
    for folder in os.listdir(app.tja_folder_path):
        app.song_list.append(folder)
        tja = tja_parser(f'Songs\\{folder}')
        app.song_metadata.append(tja.get_metadata())
        
    
def song_select_onStep(app):
    app.current_ms = get_current_ms() - app.start_ms
    app.fps_display = 1000 / (app.current_ms - app.last_ms)
    app.last_ms = app.current_ms
    
    if isinstance(app.bg_music, sa.PlayObject):
        if not app.bg_music.is_playing():
            app.bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
            return
    
def song_select_redrawAll(app):
    fps_counter(app)
    for i in range(len(app.song_list)):
        if i == app.selected_song:
            color = 'red'
        else:
            color = 'black'
        drawLabel(app.song_metadata[i][0], app.width/2, 40+(i*40), fill=color, font='DFPKanTeiRyu-XB')
    
def song_select_onKeyPress(app, key):
    if key == 'up':
        sa.WaveObject.from_wave_file('Sounds/inst_00_katsu.wav').play()
        if app.selected_song > 0:
            app.selected_song -= 1
        else:
            app.selected_song += len(app.song_list)-1
    elif key == 'down':
        sa.WaveObject.from_wave_file('Sounds/inst_00_katsu.wav').play()
        if app.selected_song < len(app.song_list)-1:
            app.selected_song += 1
        else:
            app.selected_song = 0
    elif key == 'enter':
        sa.WaveObject.from_wave_file('Sounds/inst_00_don.wav').play().wait_done()
        sa.stop_all()
        setActiveScreen('game')
        play_tja(app, f'{app.tja_folder_path}\\{app.song_list[app.selected_song]}')
        
    switchScreen(app, key)