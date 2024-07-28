from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os

from global_funcs import *
from game import play_tja 

def onScreenSwitch_song_select(app):
    app.sfx_don.play().wait_done()
    sa.stop_all()
    app.song_select_bg_music_start = sa.WaveObject.from_wave_file('Sounds/SongSelect_start.wav').play().wait_done()
    app.song_select_bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
    
def song_select_onAppStart(app):
    app.global_song_list = []
    app.global_song_metadata = []
    app.song_selected = 0
    app.song_p1_diff = 5
    
    #Create a list of songs that can be indexed and also one with metadata only
    for folder in os.listdir(app.tja_folder_path):
        app.global_song_list.append(folder)
        tja = tja_parser(f'{app.tja_folder_path}\\{folder}')
        app.global_song_metadata.append(tja.get_metadata())        

def song_select_bgm_manager(app, music, path):
    if isinstance(music, sa.PlayObject):
        if not music.is_playing():
            app.song_select_bg_music = sa.WaveObject.from_wave_file(path).play()
    
def song_select_onStep(app):
    fps_manager(app)
    song_select_bgm_manager(app, app.song_select_bg_music, 'Sounds/SongSelect.wav')
    
def song_select_redrawAll(app):
    fps_counter(app)
    for i in range(len(app.global_song_list)):
        color = 'red' if i == app.song_selected else 'black'
        drawLabel(app.global_song_metadata[i][0], app.width/2, 40+(i*40), fill=color, font='DFPKanTeiRyu-XB')
    
def song_select_onKeyPress(app, key):
    if key == 'up':
        app.sfx_kat.play()
        if app.song_selected > 0:
            app.song_selected -= 1
        else:
            app.song_selected += len(app.global_song_list)-1
    elif key == 'down':
        app.sfx_kat.play()
        if app.song_selected < len(app.global_song_list)-1:
            app.song_selected += 1
        else:
            app.song_selected = 0
    elif key == 'enter':
        app.sfx_don.play().wait_done()
        sa.stop_all()
        setActiveScreen('game')
        play_tja(app, f'{app.tja_folder_path}\\{app.global_song_list[app.song_selected]}')
        
    switchScreen(app, key)