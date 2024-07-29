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
    app.song_selected = 3
    app.song_p1_diff = 0
    
    app.song_select_difficulty = False
    
    #Create a list of songs that can be indexed and also one with metadata only
    for folder in os.listdir(app.tja_folder_path):
        app.global_song_list.append(folder)
        tja = tja_parser(f'{app.tja_folder_path}\\{folder}')
        app.global_song_metadata.append(tja.get_metadata())   

    app.song_select_draw_bg_image = CMUImage(Image.open('Graphics/3_SongSelect/Genre_Background/GenreBackground_5.png'))
    app.song_select_draw_bar_genre = CMUImage(Image.open('Graphics/3_SongSelect/Bar_Genre/Bar_Genre_5.png'))
    app.song_select_draw_diff_back = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Back/Difficulty_Back_5.png'))
    app.song_select_draw_diff_bar = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Bar.png').crop((166, 0, 879, 236)))
    app.song_select_draw_diff_select = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Select_Bar_1P.png').crop((0, 133, 259, 386)))
    app.song_select_draw_diff_select_1P = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Select_Bar_1P.png').crop((0, 0, 259, 109)))
    app.song_select_draw_diff_star = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Star.png'))

def song_select_bgm_manager(app, music, path):
    if isinstance(music, sa.PlayObject):
        if not music.is_playing():
            app.song_select_bg_music = sa.WaveObject.from_wave_file(path).play()
    
def song_select_onStep(app):
    fps_manager(app)
    song_select_bgm_manager(app, app.song_select_bg_music, 'Sounds/SongSelect.wav')

def song_select_draw_song_list(app):
    for i in range(9):
        song_title = app.global_song_metadata[i][0]
        color = 'red' if i == app.song_selected else 'white'
        location = (i*100)
        drawImage(app.song_select_draw_bar_genre, app.width/2, location, align='center')
        if len(song_title) > 25:
            text_size = 20
        else:
            text_size = 30
        drawLabel(song_title, app.width/2, location, fill=color, font='DFPKanTeiRyu-XB', border='black', size=text_size)
        
def song_select_draw_diff_select(app):
    drawImage(app.song_select_draw_diff_back, app.width/2, app.height/2, align='center')
    drawImage(app.song_select_draw_diff_select, 230+(143*app.song_p1_diff), 293)
    drawImage(app.song_select_draw_diff_bar, app.width/2, app.height/2 + 60, align='center')
    difficulties = app.global_song_metadata[3][8]
    for i in range(len(difficulties)):
        for j in range(difficulties[i][0]):
            drawImage(app.song_select_draw_diff_star, 305+(143*i)+(j*10.5), 491)
        drawLabel(str(difficulties[i][0]), 370+(143*i), 477, fill='white', font='DFPKanTeiRyu-XB', border='black', borderWidth=2, size=25)    
    song_title = app.global_song_metadata[app.song_selected][0]
    song_subtitle = app.global_song_metadata[app.song_selected][2]
    if len(song_title) > 24:
        text_size = 28
        text_border_width = 2
    else:
        text_size = 60
        text_border_width = 4
    drawLabel(song_title, app.width/2, 200, fill='white', font='DFPKanTeiRyu-XB', border='black', size=text_size, borderWidth=text_border_width)
    drawLabel(song_subtitle, app.width/2, 250, fill='white', font='DFPKanTeiRyu-XB', border='black', size=20, borderWidth=2)
    drawImage(app.song_select_draw_diff_select_1P, 230+(143*app.song_p1_diff), 180)
    
def song_select_redrawAll(app):
    drawImage(app.song_select_draw_bg_image, 0, 0)
    if app.song_select_difficulty:
        song_select_draw_diff_select(app)
    else:
        song_select_draw_song_list(app)
    fps_counter(app)

def song_select_move_list(app, key):
    if key == 'up':
        app.global_song_list.insert(0, (app.global_song_list.pop()))
        app.global_song_metadata.insert(0, (app.global_song_metadata.pop()))
    else:
        app.global_song_list.append(app.global_song_list.pop(0))
        app.global_song_metadata.append(app.global_song_metadata.pop(0))
    
def song_select_onKeyPress(app, key):
    if not app.song_select_difficulty:
        if key == 'up':
            app.sfx_kat.play()
            song_select_move_list(app, 'up')
        elif key == 'down':
            app.sfx_kat.play()
            song_select_move_list(app, 'down')
        elif key == 'enter':
            app.sfx_don.play()
            app.song_select_difficulty = True
    else:
        difficulties = app.global_song_metadata[3][8]
        if key == 'left':
            app.sfx_kat.play()
            if app.song_p1_diff > 0:
                app.song_p1_diff -= 1
        elif key == 'right':
            app.sfx_kat.play()
            if app.song_p1_diff < len(difficulties)-1:
                app.song_p1_diff += 1
        elif key == 'escape':
            app.song_select_difficulty = False
        elif key == 'enter':
            sa.stop_all()
            setActiveScreen('game')
            play_tja(app, f'{app.tja_folder_path}\\{app.global_song_list[app.song_selected]}')
        
    switchScreen(app, key)