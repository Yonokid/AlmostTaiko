from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os
import random as rand
import math

from game import *
from game_2p import *

#All images and sounds created by BANDAI NAMCO ENTERTAINMENT

def ai_battle_onAppStart(app):
    app.draw_ai_background_up = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/ai_enso_panel_0.png').crop((3, 882, 1283, 1067)))
    app.draw_ai_background_up_clear = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/ai_enso_panel_0.png').crop((3, 1071, 1283, 1255)))
    app.draw_ai_lane_background = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/lane_left_4.png'))
    app.draw_ai_lane = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/lane.png').crop((4, 1, 952, 179)))
    app.draw_p1_down = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/p1_down.png').crop((0, 0, 640, 720)))
    app.draw_ai_down = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/ai_down.png'))
    app.draw_section_icon_base = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/section_result_icon.png').crop((2, 1281, 195, 1363)))
    app.draw_section_icon_win = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/section_result_icon.png').crop((548, 1295, 598, 1343)))
    app.draw_section_icon_lose = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/section_result_icon.png').crop((644, 5, 693, 52)))
    app.draw_scoreboard_ai = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/score_board.png').crop((8, 7, 156, 104)))
    app.draw_scoreboard_p1 = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/score_board.png').crop((8, 115, 156, 210)))
    app.draw_scoreboard_judgments = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/score_board.png').crop((18, 216, 52, 282)))
    app.draw_section_timer = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/section_timer.png').crop((3, 2, 135, 39)))

    app.bottom_crop = 640
    app.section_wins = [None, None, None, None, None]
    app.section_index = 0
    app.section_crop = 1

    app.ai_difficulty_table = {1: [60, 30, 10], 2: [70, 23, 7], 3: [80, 15, 5], 4: [90, 8, 2], 5: [98, 1, 1]}
    app.ai_difficulty = rand.randint(1, 5)

def initialize_battle(app):
    app.sections = [(app.song_note_count_with_roll // 5), (app.song_note_count_with_roll * 2) // 5, (app.song_note_count_with_roll * 3) // 5, (app.song_note_count_with_roll * 4) // 5, (app.song_note_count_with_roll)]

def ai_battle_onStep(app):
    app.player_1.draw_current_frame += 1
    app.player_2.draw_current_frame += 1
    fps_manager(app)
    game_animate_notes(app)

    if app.game_play_song:
        if len(app.player_2.current_notes) > 0 and app.section_index <= 4:
            ai_battle_ai(app)
        app.player_1.note_manager(app, app.song_play_notes, app.song_bars, app.song_draw_notes)
        app.player_2.note_manager(app, app.song_2p_play_notes, app.song_2p_bars, app.song_2p_draw_notes)

    if app.game_result_delay != 0:
        game_song_finished(app)
    game_judge_display(app)
    game_p2_judge_display(app)

def ai_battle_init_section(app):
    app.player_1.section_good_count = 0
    app.player_1.section_ok_count = 0
    app.player_1.section_bad_count = 0

    app.player_2.section_good_count = 0
    app.player_2.section_ok_count = 0
    app.player_2.section_bad_count = 0
    app.section_crop = 1

def ai_battle_note_correct(app, note, index):
    app.player_2.combo += 1

    app.player_2.draw_start_frame = app.player_2.draw_current_frame
    app.player_2.draw_arc_dict[app.player_2.draw_start_frame] = note['note']

    app.player_2.current_notes.popleft()

    #Remove note from the screen
    for note in range(len(app.player_2.current_notes_draw)):
        if app.player_2.current_notes_draw[note]['index'] == index:
            app.player_2.current_notes_draw.pop(note)
            break

def ai_battle_check_section_win(app):
    player_1_score = (app.player_1.section_good_count) + (app.player_1.section_ok_count / 2) + (app.player_1.section_bad_count * -2)
    player_2_score = (app.player_2.section_good_count) + (app.player_2.section_ok_count / 2) + (app.player_2.section_bad_count * -2)
    if player_1_score > player_2_score:
        app.section_wins[app.section_index] = True
        #sa.WaveObject.from_wave_file('Sounds/AI_section_win.wav').play()
    else:
        app.section_wins[app.section_index] = False
        #sa.WaveObject.from_wave_file('Sounds/AI_section_lose.wav').play()

def ai_battle_ai(app):
    if app.player_2.current_notes[0]['index'] == app.sections[app.section_index]:
        ai_battle_check_section_win(app)
        app.section_index += 1
        ai_battle_init_section(app)
    elif app.player_2.current_notes[0]['index'] == app.sections[app.section_index]-1:
        ai_battle_check_section_win(app)
    app.bottom_crop = 640 + (app.player_1.section_good_count - app.player_2.section_good_count)

    note = app.player_2.current_notes[0]
    if note['note'] not in {'5', '6', '7', '8', '9'}:
        if app.current_ms - 25 <= note['ms'] <= app.current_ms + 25:
            app.player_2.judge_timer = app.current_ms
            index = note['index']
            judgement = rand.randint(0, 100)
            difficulty_table = app.ai_difficulty_table[app.ai_difficulty]
            if judgement >= difficulty_table[1]:
                app.player_2.good = True
                app.player_2.section_good_count += 1
                ai_battle_note_correct(app, note, index)
            elif judgement >= difficulty_table[2]:
                app.player_2.ok = True
                app.player_2.section_ok_count += 1
                ai_battle_note_correct(app, note, index)
            else:
                app.player_2.bad = True
                app.player_2.section_bad_count += 1
                app.player_2.combo = 0
            if app.section_crop < 120:
                app.section_crop += 120 / app.sections[0]


def ai_battle_draw_scoreboards(app):
    y_p1 = 240
    y_p2 = 390
    drawImage(app.draw_scoreboard_p1, 0, y_p1)
    drawImage(app.draw_scoreboard_judgments, 18, y_p1+11)
    drawLabel(app.player_1.section_good_count, 70, y_p1+18, align='right', fill='white', font='DFPKanTeiRyu-XB', border='black', size=10, borderWidth=1)
    drawLabel(app.player_1.section_ok_count, 70, y_p1+35, align='right', fill='white', font='DFPKanTeiRyu-XB', border='black', size=10, borderWidth=1)
    drawLabel(app.player_1.section_bad_count, 70, y_p1+52, align='right', fill='white', font='DFPKanTeiRyu-XB', border='black', size=10, borderWidth=1)

    drawImage(app.draw_scoreboard_ai, 0, y_p2)
    drawImage(app.draw_scoreboard_judgments, 18, y_p2+12)
    drawLabel(app.player_2.section_good_count, 70, y_p2+19, align='right', fill='white', font='DFPKanTeiRyu-XB', border='black', size=10, borderWidth=1)
    drawLabel(app.player_2.section_ok_count, 70, y_p2+36, align='right', fill='white', font='DFPKanTeiRyu-XB', border='black', size=10, borderWidth=1)
    drawLabel(app.player_2.section_bad_count, 70, y_p2+53, align='right', fill='white', font='DFPKanTeiRyu-XB', border='black', size=10, borderWidth=1)

def ai_battle_draw_sections(app):
    drawImage(app.draw_section_icon_base, 155, 100)
    for i in range(5):
        if i % 2 == 0:
            y_pos = 0
        else:
            y_pos = 15
        if app.section_wins[i] == True:
            drawImage(app.draw_section_icon_win, 164.5+(i*31), 107+y_pos)
        elif app.section_wins[i] == False:
            drawImage(app.draw_section_icon_lose, 164.5+(i*31), 107+y_pos)
        else:
            continue
def ai_battle_draw_section_timer(app):
    drawRect(202, 197, 124, 17, fill='gray')
    drawRect(202, 197, app.section_crop, 17, fill=rgb(0,198,7))
    drawImage(app.draw_section_timer, 198, 180)

def ai_battle_redrawAll(app):
    drawImage(app.draw_ai_down, 0, 0)
    drawImage(app.draw_p1_down, 0, 0)
    if app.player_1.gauge_crop > 550:
        drawImage(app.draw_ai_background_up_clear, 0, 0)
    else:
        drawImage(app.draw_ai_background_up, 0, 0)

    drawImage(app.draw_ai_lane, 333, 358)
    game_draw_lane(app)
    drawImage(app.game_draw_judge_circle, 359, 369+11)

    game_draw_gauge(app)

    app.player_1.spawn_notes(app)
    app.player_2.spawn_notes(app)
    app.player_1.draw_arc(app)
    app.player_2.draw_arc(app)

    drawImage(app.draw_ai_lane_background, 0, 357)
    game_draw_drum(app)
    game_2p_draw_drum(app)
    ai_battle_draw_sections(app)
    ai_battle_draw_section_timer(app)
    ai_battle_draw_scoreboards(app)
    app.player_1.draw_judgments(app)
    app.player_2.draw_judgments(app)

    fps_counter(app)

def ai_battle_onKeyPress(app, key):
    switchScreen(app, key)
    game_onKeyPress(app, key)

def ai_battle_onKeyRelease(app, key):
    game_onKeyRelease(app, key)
