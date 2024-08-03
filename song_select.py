from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os

#All images and sounds created by BANDAI NAMCO ENTERTAINMENT

from global_funcs import *
from game import play_tja
from game_2p import p2_play_tja
from ai_battle import initialize_battle

def onScreenSwitch_song_select(app):
    app.sfx_don.play().wait_done()
    sa.stop_all()
    if app.ai_battle:
        app.song_select_bg_music_start = sa.WaveObject.from_wave_file('Sounds/AI_Battle_start.wav').play().wait_done()
        app.song_select_bg_music = sa.WaveObject.from_wave_file('Sounds/AI_Battle.wav').play()
    else:
        app.song_select_bg_music_start = sa.WaveObject.from_wave_file('Sounds/SongSelect_start.wav').play().wait_done()
        app.song_select_bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
    app.song_1p_confirmed = False
    app.song_2p_confirmed = False

def song_select_onAppStart(app):
    app.global_song_list = []
    app.global_song_metadata = []
    app.song_selected = 3
    app.song_1p_diff = 0
    app.song_2p_diff = 0
    app.song_1p_confirmed = False
    app.song_2p_confirmed = False

    app.song_select_difficulty = False

    #Create a list of songs that can be indexed and also one with metadata only
    for folder in os.listdir(app.tja_folder_path):
        app.global_song_list.append(folder)
        tja = tja_parser(f'{app.tja_folder_path}\\{folder}')
        app.global_song_metadata.append(tja.get_metadata())

    app.song_select_draw_bg_image = CMUImage(Image.open('Graphics/3_SongSelect/Genre_Background/GenreBackground_5.png'))
    app.song_select_draw_bg_ai_image = CMUImage(Image.open('Graphics/3_SongSelect/AI_Background.png'))
    app.song_select_draw_bar_genre = CMUImage(Image.open('Graphics/3_SongSelect/Bar_Genre/Bar_Genre_5.png'))
    app.song_select_draw_diff_back = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Back/Difficulty_Back_5.png'))
    app.song_select_draw_diff_bar = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Bar.png').crop((166, 0, 879, 236)))
    app.song_select_draw_diff_select = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Select_Bar_1P.png').crop((0, 133, 259, 386)))
    app.song_select_draw_diff_select_1P = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Select_Bar_1P.png').crop((0, 0, 259, 109)))
    app.song_select_draw_diff_select_2P = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Select_Bar_2P.png').crop((0, 0, 259, 109)))
    app.song_select_draw_diff_star = CMUImage(Image.open('Graphics/3_SongSelect/Difficulty_Select/Difficulty_Star.png'))

    app.song_select_draw_ai_difficulty = CMUImage(Image.open('Graphics/5_Game/13_AIBattle/ai_song_select_tension.png').crop((11, 7, 176, 98)))
    app.song_select_draw_ai_diff_bar = CMUImage(Image.open('Graphics/5_Game/13_AIBattle/ai_song_select_tension.png').crop((6, 128, 31, 139)))
    app.song_select_draw_ai_don = CMUImage(Image.open('Graphics/5_Game/13_AIBattle/story_1.png').crop((468, 15, 830, 335)).resize((int(362 * (2/3)),int(320 * (2/3)))))

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
    if app.players == 2 and not app.ai_battle:
        if app.song_2p_confirmed:
            drawImage(app.song_select_draw_diff_select, 230+(143*app.song_2p_diff), 293)
    if app.song_1p_confirmed:
        drawImage(app.song_select_draw_diff_select, 230+(143*app.song_1p_diff), 293)
    drawImage(app.song_select_draw_diff_bar, app.width/2, app.height/2 + 60, align='center')
    difficulties = app.global_song_metadata[3][-1]
    for i in range(6):
        if i not in difficulties:
            continue
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
    drawImage(app.song_select_draw_diff_select_1P, 230+(143*app.song_1p_diff), 180)
    if app.players == 2 and not app.ai_battle:
        drawImage(app.song_select_draw_diff_select_2P, 230+(143*app.song_2p_diff), 180)

def song_select_draw_ai_difficulty(app):
    drawImage(app.song_select_draw_ai_don, 1000, 450)
    drawImage(app.song_select_draw_ai_difficulty, 1100, 400)
    drawLabel('Status', 1145, 410, fill='black', font='DFPKanTeiRyu-XB', border='white', borderWidth=1)
    if app.ai_difficulty == 5:
        label = 'On Fire'
    elif app.ai_difficulty == 4:
        label = 'Good'
    elif app.ai_difficulty == 3:
        label = 'Meh'
    elif app.ai_difficulty == 2:
        label = 'Bad'
    else:
        label = 'Awful'
    drawLabel(label, 1190, 433, fill=rgb(67,254,218), size=20, font='DFPKanTeiRyu-XB', bold=True, align='center')
    for i in range(app.ai_difficulty):
        drawImage(app.song_select_draw_ai_diff_bar, 1134+(i*21), 445)

def song_select_redrawAll(app):
    if app.ai_battle:
        drawImage(app.song_select_draw_bg_ai_image, 0, 0)
        song_select_draw_ai_difficulty(app)
    else:
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

def song_select_players_confirmed(app):
    sa.stop_all()
    app.sfx_don.play().wait_done()
    play_tja(app, f'{app.tja_folder_path}\\{app.global_song_list[app.song_selected]}')
    if app.ai_battle:
        app.song_2p_diff = app.song_1p_diff
        p2_play_tja(app, f'{app.tja_folder_path}\\{app.global_song_list[app.song_selected]}')
        initialize_battle(app)
        setActiveScreen('ai_battle')
    elif app.players == 1:
        setActiveScreen('game')
    elif app.players == 2:
        setActiveScreen('game_2p')
        p2_play_tja(app, f'{app.tja_folder_path}\\{app.global_song_list[app.song_selected]}')

def song_select_keys_p1(app, key):
    difficulties = app.global_song_metadata[3][8]
    if key == 'e':
        app.sfx_kat.play()
        if app.song_1p_diff > 0 and not app.song_1p_confirmed:
            app.song_1p_diff -= 1
    elif key == 'i':
        app.sfx_kat.play()
        if app.song_1p_diff < len(difficulties)-1 and not app.song_1p_confirmed:
            app.song_1p_diff += 1
    elif key == 'f' or key == 'j':
        app.song_1p_confirmed = True
        if app.players == 2:
            if app.song_1p_confirmed and app.song_2p_confirmed:
                song_select_players_confirmed(app)
            elif app.ai_battle:
                song_select_players_confirmed(app)
            else:
                app.sfx_don.play()
        else:
            song_select_players_confirmed(app)

def song_select_keys_p2(app, key):
    difficulties = app.global_song_metadata[3][8]
    if key == 'd':
        app.sfx_kat.play()
        if app.song_2p_diff > 0 and not app.song_2p_confirmed:
            app.song_2p_diff -= 1
    elif key == 'k':
        app.sfx_kat.play()
        if app.song_2p_diff < len(difficulties)-1 and not app.song_2p_confirmed:
            app.song_2p_diff += 1
    elif key == 'c' or key == 'm':
        app.song_2p_confirmed = True
        if app.players == 2:
            if app.song_1p_confirmed and app.song_2p_confirmed:
                song_select_players_confirmed(app)
            else:
                app.sfx_don.play()
        else:
            song_select_players_confirmed(app)

def song_select_onKeyPress(app, key):
    if not app.song_select_difficulty:
        if key in {'up', 'e', 'd', 'left'}:
            app.sfx_kat.play()
            song_select_move_list(app, 'up')
        elif key in {'down', 'i', 'k', 'right'}:
            app.sfx_kat.play()
            song_select_move_list(app, 'down')
        elif key in {'enter', 'c','f','j','m'}:
            app.sfx_don.play()
            app.song_select_difficulty = True
        elif key == 'escape':
            sa.stop_all()
            app.sfx_cancel.play().wait_done()
            setActiveScreen('entry')

    else:
        song_select_keys_p1(app, key)
        if app.players == 2 and not app.ai_battle:
            song_select_keys_p2(app, key)
        if key == 'escape':
            app.sfx_cancel.play()
            app.song_select_difficulty = False
            app.song_1p_confirmed = False
            app.song_2p_confirmed = False
    switchScreen(app, key)
