from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os
import random as rand
import math

from global_funcs import *
from result import onScreenSwitch_result
from game import *

def game_2p_onAppStart(app):
    app.player_2 = Player(2)
    app.game_2p_draw_background_up = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_up/2/Main2.PNG'))
    app.game_2p_draw_background_up_clear = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_up/2/Main_Clear2.png'))
    app.game_2p_draw_frame = CMUImage(Image.open('Graphics/5_Game/6_Taiko/2P_Frame.png'))
    app.game_2p_draw_background_main = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Main.png'))
    app.game_2p_draw_background_sub = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Sub.png'))
    app.game_2p_draw_background = CMUImage(Image.open('Graphics/5_Game/6_Taiko/2P_Background.png'))
    app.game_2p_draw_gauge_base = CMUImage(Image.open('Graphics/5_Game/7_Gauge/2P_base.png').crop((0, 0, 695, 43)))


def p2_play_tja(app, tja_folder):
    app.tja2 = tja_parser(tja_folder)
    app.tja2.get_metadata()
    app.tja2.distance = app.width - app.game_judge_x
    app.tja2.fps = app.stepsPerSecond

    app.song_2p_play_notes, app.song_2p_draw_notes, app.song_2p_bars = app.tja2.notes_to_position(app.song_2p_diff)

    app.song_2p_note_count = (sum(1 for key in app.song_2p_play_notes if key.get('note') in {'1','2','3','4'}))
    app.song_2p_note_count_with_roll = (sum(1 for key in app.song_2p_play_notes))

    app.song_2p_base_score = (1000000 / app.song_2p_note_count) / 10
    app.song_2p_base_score = math.ceil(app.song_2p_base_score) * 10

def game_2p_onStep(app):
    app.player_1.draw_current_frame += 1
    app.player_2.draw_current_frame += 1
    fps_manager(app)
    game_animate_notes(app)

    if app.game_play_song:
        app.player_1.note_manager(app, app.song_play_notes, app.song_bars, app.song_draw_notes)
        app.player_2.note_manager(app, app.song_2p_play_notes, app.song_2p_bars, app.song_2p_draw_notes)

    if app.game_result_delay != 0:
        game_song_finished(app)

def game_2p_draw_background(app):
    if app.player_1.gauge_crop < 550:
        up_image = app.game_draw_background_up
    else:
        up_image = app.game_draw_background_up_clear
    if app.player_2.gauge_crop < 550:
        up_image_2 = app.game_2p_draw_background_up
    else:
        up_image_2 = app.game_2p_draw_background_up_clear
    for i in range(4):
        drawImage(up_image, 0+(i*326), 0)
        drawImage(up_image_2, 0+(i*326), app.height-184)
    drawImage(app.game_draw_background, 0, 184)

def game_2p_draw_lane(app):
    drawImage(app.game_2p_draw_background_main, 333, 369)
    drawImage(app.game_draw_background_sub, 333, 502)
    drawImage(app.game_2p_draw_frame, 329, 360)
    drawImage(app.game_draw_judge_circle, 359, 369+11)

def game_2P_draw_gauge(app):
    drawImage(app.game_2p_draw_gauge_base, 493, 532)
    drawImage(app.player_2.draw_gauge, 493, 532)
    drawImage(app.game_draw_soul, 1199, 515)

def game_2p_draw_judgments(app):
    if app.player_2.autoplay: drawLabel('AUTO', app.game_judge_x, 462, size=30, fill='white', bold=True, border='black')
    elif app.player_2.good: drawLabel('GOOD', app.game_judge_x, 462, size=30, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
    elif app.player_2.ok: drawLabel('OK', app.game_judge_x, 462, size=30, fill='white', bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
    elif app.player_2.bad: drawLabel('BAD', app.game_judge_x, 462, size=30, fill=gradient('deepSkyBlue','royalBlue','indigo', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)

def game_2p_draw_drum(app):
    drawImage(app.game_2p_draw_background, 0, 359)
    drawImage(app.game_draw_drum, 190, 386)
    if app.player_2.inner_drum_L:
        drawImage(app.game_draw_red_L, 190, 386)
    if app.player_2.inner_drum_R:
        drawImage(app.game_draw_red_R, 190+59, 386)
    if app.player_2.outer_drum_L:
        drawImage(app.game_draw_blue_L, 190, 386)
    if app.player_2.outer_drum_R:
        drawImage(app.game_draw_blue_R, 190+59, 386)
    if 10 <= app.player_2.combo:
        drawLabel(app.player_2.combo, 250, 426, size=50, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=3)
    drawLabel(app.player_2.score, 190, 510, align='right', size=35, border='black', fill='white', borderWidth=3, bold=True, font='DFPKanTeiRyu-XB')

def game_2p_redrawAll(app):
    game_2p_draw_background(app)
    game_draw_lane(app)
    game_2p_draw_lane(app)
    game_draw_gauge(app)
    game_2P_draw_gauge(app)

    app.player_1.spawn_notes(app)
    app.player_2.spawn_notes(app)
    app.player_1.draw_arc(app)
    app.player_2.draw_arc(app)

    game_draw_drum(app)
    game_2p_draw_drum(app)
    app.player_1.draw_judgments(app)
    app.player_2.draw_judgments(app)
    fps_counter(app)

def game_2p_onKeyPress(app, key):
    if key == 'z':
        app.player_2.autoplay = not app.player_2.autoplay
    if not app.player_2.autoplay:
        if key == 'c':
            app.player_2.inner_drum_L = True
            app.player_2.check_note(app, 1)
        if key == 'm':
            app.player_2.inner_drum_R = True
            app.player_2.check_note(app, 1)
        if key == 'd':
            app.player_2.outer_drum_L = True
            app.player_2.check_note(app, 2)
        if key == 'k':
            app.player_2.outer_drum_R = True
            app.player_2.check_note(app, 2)
    game_onKeyPress(app, key)

def game_2p_onKeyRelease(app, key):
    if key == 'd' or key == 'k':
        app.player_2.good = False
        app.player_2.ok = False
        app.player_2.bad = False
        app.player_2.outer_drum_L = False
        app.player_2.outer_drum_R = False
    if key == 'c' or key == 'm':
        app.player_2.good = False
        app.player_2.ok = False
        app.player_2.bad = False
        app.player_2.inner_drum_L = False
        app.player_2.inner_drum_R = False
    game_onKeyRelease(app, key)
