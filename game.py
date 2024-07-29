from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os
import random as rand
import math

from global_funcs import *
from result import onScreenSwitch_result

def game_onAppStart(app):
    
    #DO NOT CHANGE
    app.timing_good = 25.0250015258789
    app.timing_ok = 75.0750045776367
    app.timing_bad = 108.441665649414
    
    app.game_judge_x = 412
    #Not implemented, skip
    app.game_ignored_notes = {'5','6','7','8','9'}
    
    app.game_play_song = False
    
    app.game_result_delay = 0
    
    game_p1(app)
    
    ##########
    ##Graphics
    ##########
    
    app.game_draw_arc_dict = dict()
    app.game_draw_arc_points = 25
    app.game_draw_current_frame = 0
    app.game_draw_start_frame = 0
    
    app.game_draw_background_main = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Main.png'))
    app.game_draw_background_sub = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Sub.png'))
    app.game_draw_p1_frame = CMUImage(Image.open('Graphics/5_Game/6_Taiko/1P_Frame.png'))
    app.game_draw_background = CMUImage(Image.open('Graphics/5_Game/6_Taiko/1P_Background.png'))
    
    app.game_draw_p1_judge_circle = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((10, 11, 117, 118)))
    
    app.game_draw_drum = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Base.png'))
    app.game_draw_red_L = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Don.png').crop((0, 0, 59, 88)))
    app.game_draw_red_R = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Don.png').crop((59, 0, 104, 88)))
    app.game_draw_blue_L = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Ka.png').crop((0, 0, 59, 115)))
    app.game_draw_blue_R = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Ka.png').crop((59, 0, 119, 115)))
    
    app.game_draw_don = None
    app.game_draw_kat = None
    app.game_draw_dai_don = None
    app.game_draw_dai_kat = None
    
    app.game_draw_don_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((158, 29, 229, 100)))
    app.game_draw_kat_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((288, 29, 359, 100)))
    app.game_draw_don_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((158, 159, 229, 230)))
    app.game_draw_kat_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((288, 159, 359, 230)))
    
    app.game_draw_dai_don_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((400, 10, 507, 118)))
    app.game_draw_dai_kat_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((530, 10, 637, 118)))
    app.game_draw_dai_don_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((400, 141, 507, 248)))
    app.game_draw_dai_kat_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((530, 141, 637, 248)))
    
    app.game_draw_barline = CMUImage(Image.open('Graphics/5_Game/Bar.png').crop((0, 0, 4, 129)))
    
    background_number = rand.randint(0, 2)
    app.game_draw_background_down = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_down/1/0.png'))
    app.game_draw_background_up = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_up/2/Main.PNG'))
    app.game_draw_background_up_clear = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_up/2/Main_Clear2.png'))
    app.game_draw_footer = CMUImage(Image.open(f'Graphics/5_Game/8_Footer/{background_number}.png'))
    
    app.game_draw_p1_gauge_base = CMUImage(Image.open('Graphics/7_Gauge/1P_base.png').crop((0, 0, 695, 43)))
    #app.game_draw_p1_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((0, 0, app.game_p1_gauge_crop, 43)))
    app.game_draw_soul = CMUImage(Image.open('Graphics/7_Gauge/Soul.png').crop((0, 0, 80, 80)))

def game_p1(app):
    #Judgment Display
    app.game_p1_good = False
    app.game_p1_ok = False
    app.game_p1_bad = False
    app.game_p1_autoplay = False
    
    #Drum Display
    app.game_p1_inner_drum_L = False
    app.game_p1_inner_drum_R = False
    app.game_p1_outer_drum_L = False
    app.game_p1_outer_drum_R = False
    
    #This will be changable in the future
    app.p1_judge_offset = 30
    
    #Note management for p1
    app.game_p1_current_notes = []
    app.game_p1_current_bars = []
    app.game_p1_current_notes_draw = []
    app.game_p1_play_note_index = 0
    app.game_p1_draw_note_index = 0
    app.game_p1_bar_index = 0
    
    #Gauge management for p1
    app.game_p1_gauge_count = 0
    app.game_p1_gauge_crop = 1
    app.game_p1_clear = False
    
    #Score management for p1
    app.game_p1_good_count = 0
    app.game_p1_ok_count = 0
    app.game_p1_bad_count = 0
    app.game_p1_combo = 0
    app.game_p1_score = 0
    app.game_p1_max_combo = 0
    
    app.game_draw_p1_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((0, 0, 1, 43)))
    
def play_tja(app, tja_folder):
    #Initialize p1
    game_p1(app)
    app.game_play_song = True
    app.game_result_delay = 0
    
    #Initialize TJA file
    app.tja = tja_parser(tja_folder)
    app.tja.get_metadata()
    app.tja.distance = app.width - app.game_judge_x
    app.tja.fps = app.stepsPerSecond
    
    app.start_ms = get_current_ms() - app.tja.offset*1000 
    
    app.song_music = sa.WaveObject.from_wave_file(app.tja.wave)
    
    app.song_play_notes, app.song_draw_notes, app.song_bars = app.tja.notes_to_position(app.song_p1_diff)
    
    #https://outfox.wiki/en/dev/mode-support/tja-support
    #Note count with roll is used for determining when song has ended
    app.song_note_count = (sum(1 for key in app.song_play_notes if key.get('note') in {'1','2','3','4'}))
    app.song_note_count_with_roll = (sum(1 for key in app.song_play_notes))
    
    app.song_base_score = (1000000 / app.song_note_count) / 10
    app.song_base_score = math.ceil(app.song_base_score) * 10
    
    app.song_music.play()

def game_animate_notes(app):
    eighth_in_ms = (60000 * 4 / app.tja.bpm) / 8
    current_eighth = app.current_ms // eighth_in_ms
    if current_eighth % 2 == 0:
        app.game_draw_don = app.game_draw_don_1
        app.game_draw_kat = app.game_draw_kat_1
        app.game_draw_dai_don = app.game_draw_dai_don_1
        app.game_draw_dai_kat = app.game_draw_dai_kat_1
    else:
        app.game_draw_don = app.game_draw_don_2
        app.game_draw_kat = app.game_draw_kat_2
        app.game_draw_dai_don = app.game_draw_dai_don_2
        app.game_draw_dai_kat = app.game_draw_dai_kat_2

def game_song_finished(app):
    if app.current_ms >= app.game_result_delay + 2000:
        if app.game_p1_bad_count == 0:
            sa.WaveObject.from_wave_file('Sounds/Full combo.wav').play().wait_done()
        elif app.game_p1_gauge_crop >= 545:
            sa.WaveObject.from_wave_file('Sounds/Clear.wav').play().wait_done()
        else:
            sa.WaveObject.from_wave_file('Sounds/Failed.wav').play().wait_done()
        onScreenSwitch_result(app)
        setActiveScreen('result')

def game_check_end(app, index):
    if index == app.song_note_count_with_roll-1:
        if app.game_result_delay == 0:
            app.game_result_delay = app.current_ms
            
def game_get_position(app, ms, pixels_per_frame):
    return pixels_per_frame * app.stepsPerSecond / 1000 * (ms - app.current_ms + app.p1_judge_offset)
            
def game_p1_note_manager(app):
    if app.game_p1_autoplay:
        game_p1_check_note(app, 1)
        game_p1_check_note(app, 2)
    #Add bar to current_bars list if it is ready to be shown on screen
    if app.game_p1_bar_index < len(app.song_bars) and app.current_ms > app.song_bars[app.game_p1_bar_index]['load_ms']:
        app.game_p1_current_bars.append(app.song_bars[app.game_p1_bar_index])
        app.game_p1_bar_index += 1
        
    #Add note to current_notes list if it is ready to be shown on screen
    if app.game_p1_play_note_index < len(app.song_play_notes) and app.current_ms > app.song_play_notes[app.game_p1_play_note_index]['load_ms']:
        app.game_p1_current_notes.append(app.song_play_notes[app.game_p1_play_note_index])
        app.game_p1_play_note_index += 1
    if app.game_p1_draw_note_index < len(app.song_draw_notes) and app.current_ms > app.song_draw_notes[app.game_p1_draw_note_index]['load_ms']:
        app.game_p1_current_notes_draw.append(app.song_draw_notes[app.game_p1_draw_note_index])
        app.game_p1_draw_note_index += 1
    
    #if a note was not hit within the window, remove it
    if len(app.game_p1_current_notes) != 0:
        note = app.game_p1_current_notes[0]
        if note['ms'] + app.timing_bad < app.current_ms:
            print(note['ms'], app.current_ms)
            if note['note'] not in app.game_ignored_notes:
                app.game_p1_combo = 0
                app.game_p1_bad_count += 1
                game_check_end(app, note['index'])
            app.game_p1_current_notes.pop(0)
    
    #If a bar is off screen, remove it
    if len(app.game_p1_current_bars) != 0:
        for i in range(len(app.game_p1_current_bars)-1, -1, -1):
            bar_ms, pixels_per_frame = app.game_p1_current_bars[i]['ms'], app.game_p1_current_bars[i]['ppf']
            position = game_get_position(app, bar_ms, pixels_per_frame)
            if position < app.game_judge_x - 600:
                app.game_p1_current_bars.pop(i)
    
    #If a note is off screen, remove it
    if len(app.game_p1_current_notes_draw) != 0:
        for i in range(len(app.game_p1_current_notes_draw)-1, -1, -1):
            note_ms, pixels_per_frame = app.game_p1_current_notes_draw[i]['ms'], app.game_p1_current_notes_draw[i]['ppf']
            position = game_get_position(app, note_ms, pixels_per_frame)
            if position < app.game_judge_x - 600:
                app.game_p1_current_notes_draw.pop(i)
    
    #If a note has reached the soul icon, remove it
    if len(app.game_draw_arc_dict) != 0:
        remove_keys = set()
        for start_frame in app.game_draw_arc_dict:
            if app.game_draw_current_frame >= start_frame + math.floor(app.game_draw_arc_points * 0.92):
                remove_keys.add(start_frame)
        #Control the speed of the notes in the arc so game doesn't lag
        app.game_draw_arc_points = 25 - len(app.game_draw_arc_dict)
        for key in remove_keys:
            app.game_draw_arc_dict.pop(key)
        
def game_onStep(app):
    app.game_draw_current_frame += 1
    fps_manager(app)
    game_animate_notes(app)
    
    if app.game_play_song:
        game_p1_note_manager(app)
        
    if app.game_result_delay != 0:
        game_song_finished(app)

def game_p1_note_correct(app, note):
    index = note['index']
    
    app.game_p1_combo += 1
    if app.game_p1_combo > app.game_p1_max_combo:
        app.game_p1_max_combo = app.game_p1_combo
        
    app.game_draw_start_frame = app.game_draw_current_frame
    app.game_draw_arc_dict[app.game_draw_start_frame] = note['note']
    
    game_gauge_manager(app)
    game_check_end(app, index)
    
    app.game_p1_current_notes.pop(0)
    
    #Remove note from the screen
    for note in range(len(app.game_p1_current_notes_draw)):
        if app.game_p1_current_notes_draw[note]['index'] == index:
            app.game_p1_current_notes_draw.pop(note)
            break
    
def game_p1_check_note(app, drum_type):
    if len(app.game_p1_current_notes) != 0:
        note_type = app.game_p1_current_notes[0]['note']
        index = app.game_p1_current_notes[0]['index']
        note_ms = float(app.game_p1_current_notes[0]['ms'])
        #If the wrong key was hit, stop checking
        if drum_type == 1 and note_type not in {'1','3'}:
            return
        if drum_type == 2 and note_type not in {'2','4'}:
            return
        #If the note is too far away, stop checking
        if app.current_ms > (note_ms + app.timing_bad):
            return
            
        if (note_ms - app.timing_good) + app.p1_judge_offset <= app.current_ms <= (note_ms + app.timing_good) + app.p1_judge_offset:
            app.game_p1_good = True
            app.game_p1_good_count += 1
            app.game_p1_score += app.song_base_score
            game_p1_note_correct(app, app.game_p1_current_notes[0])
            
        elif (note_ms - app.timing_ok) + app.p1_judge_offset <= app.current_ms <= (note_ms + app.timing_ok) + app.p1_judge_offset:
            app.game_p1_ok = True
            app.game_p1_ok_count += 1
            app.game_p1_score += 10 * math.floor(app.song_base_score / 2 / 10)
            game_p1_note_correct(app, app.game_p1_current_notes[0])
            
        elif (note_ms - app.timing_bad) + app.p1_judge_offset <= app.current_ms <= (note_ms + app.timing_bad) + app.p1_judge_offset:
            app.game_p1_combo = 0
            app.game_p1_bad = True
            app.game_p1_bad_count += 1
            game_check_end(app, app.game_p1_current_notes[0]['index'])

def game_gauge_manager(app):
    gauge_bar_length = 14
    app.game_p1_gauge_count = app.game_p1_good_count + (app.game_p1_ok_count/2) + (app.game_p1_bad_count * -2)
    if app.game_p1_gauge_count == 0:
        return
    gauge_bar = math.floor(app.song_note_count / 63.391)
    app.game_p1_gauge_crop = ((app.game_p1_gauge_count // gauge_bar)*gauge_bar_length)
    if app.game_p1_gauge_crop > 0:
        app.game_draw_p1_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((1, 0, app.game_p1_gauge_crop, 43)))

def game_get_note_type(note):
    if note == '1':
        return app.game_draw_don
    elif note == '2':
        return app.game_draw_kat
    elif note == '3':
        return app.game_draw_dai_don
    elif note == '4':
        return app.game_draw_dai_kat
    else:
        return None
    
def game_draw_note_arc(note_type, current_frame, start_frame):
    #center of circle that does not exist
    center_x, center_y = 785, 168
    radius = 400
    #Start at 180 degrees, end at 0
    theta_start = 3.14
    theta_end = 2 * 3.14
    
    frames_since_call = current_frame - start_frame
    if frames_since_call < 0:
        frames_since_call = 0
    if frames_since_call > app.game_draw_arc_points:
        frames_since_call = app.game_draw_arc_points
    angle_change = (theta_end - theta_start) / app.game_draw_arc_points
    theta_i = theta_start + frames_since_call * angle_change
    x_i = center_x + radius * math.cos(theta_i)
    y_i = center_y + radius * 0.5 * math.sin(theta_i)
    drawImage(note_type, x_i, y_i)   
    
def game_draw_note(app, player, note, position):
    if player == 1:
        if note == 'barline':
            note_type = app.game_draw_barline
            drawImage(note_type, position, 192)
        elif game_get_note_type(note) != None:
            drawImage(game_get_note_type(note), position, 256, align='center') 
    
def game_draw_background(app):
    drawImage(app.game_draw_background_down, 0, 360)
    if app.game_p1_gauge_crop < 550:
        up_image = app.game_draw_background_up
    else:
        up_image = app.game_draw_background_up_clear
    for i in range(4):
        drawImage(up_image, 0+(i*326), 0)
    drawImage(app.game_draw_footer, 0, 720-44)
    
def game_draw_lane(app):
    drawImage(app.game_draw_background_main, 333, 192)
    drawImage(app.game_draw_background_sub, 333, 326)
    drawImage(app.game_draw_p1_frame, 329, 136)
    drawImage(app.game_draw_p1_judge_circle, 359, 203)
    
def game_draw_judgments(app):
    if app.game_p1_autoplay: drawLabel('AUTO', app.game_judge_x, 162, size=30, fill='white', bold=True, border='black')
    elif app.game_p1_good: drawLabel('GOOD', app.game_judge_x, 162, size=30, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
    elif app.game_p1_ok: drawLabel('OK', app.game_judge_x, 162, size=30, fill='white', bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
    elif app.game_p1_bad: drawLabel('BAD', app.game_judge_x, 162, size=30, fill=gradient('deepSkyBlue','royalBlue','indigo', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)

def game_draw_drum(app):
    drawImage(app.game_draw_drum, 190, 210)
    if app.game_p1_inner_drum_L:
        drawImage(app.game_draw_red_L, 190, 210)
    if app.game_p1_inner_drum_R:
        drawImage(app.game_draw_red_R, 190+59, 210)
    if app.game_p1_outer_drum_L:
        drawImage(app.game_draw_blue_L, 190, 210)
    if app.game_p1_outer_drum_R:
        drawImage(app.game_draw_blue_R, 190+59, 210)
    if 10 <= app.game_p1_combo:
        drawLabel(app.game_p1_combo, 250, 250, size=50, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=3)

def game_draw_gauge(app):
    drawImage(app.game_draw_p1_gauge_base, 493, 144)
    drawImage(app.game_draw_soul, 1199, 125)
    drawImage(app.game_draw_p1_gauge, 493, 144)
    
def game_redrawAll(app):
    game_draw_background(app)
    game_draw_lane(app)
    game_draw_gauge(app)
    
    #draw notes and bars
    if len(app.game_p1_current_notes_draw) != 0 or len(app.game_p1_current_bars) != 0:
        for i in range(len(app.game_p1_current_bars)):
            bar = app.game_p1_current_bars[i]
            bar_ms, pixels_per_frame = bar['ms'], bar['ppf']
            position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (bar_ms - app.current_ms + app.p1_judge_offset)
            game_draw_note(app, 1, 'barline', position - (app.width - app.game_judge_x))
        for i in range(len(app.game_p1_current_notes_draw)):
            note = app.game_p1_current_notes_draw[i]
            note_type, note_ms, pixels_per_frame = note['note'], note['ms'], note['ppf']
            position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - app.current_ms + app.p1_judge_offset)
            game_draw_note(app, 1, note_type, position - (app.width - app.game_judge_x))
            
    #Draw arc
    if len(app.game_draw_arc_dict) != 0:
            for start_frame in app.game_draw_arc_dict:
                game_draw_note_arc(game_get_note_type(app.game_draw_arc_dict[start_frame]), app.game_draw_current_frame, start_frame)
                
    drawImage(app.game_draw_background, 0, 184)
    drawLabel(app.game_p1_score, 190, 208, align='right', size=35, border='black', fill='white', borderWidth=3, bold=True, font='DFPKanTeiRyu-XB')
    game_draw_drum(app)
    game_draw_judgments(app)
    fps_counter(app)
 
def game_onKeyPress(app, key):
    switchScreen(app, key)
    if key == 'a':
        app.game_p1_autoplay = not app.game_p1_autoplay
    if not app.game_p1_autoplay:
        if key == 'f' or key == 'd':
            app.game_p1_inner_drum_L = True
            game_p1_check_note(app, 1)
        if key == 'j' or key == 'k':
            app.game_p1_inner_drum_R = True
            game_p1_check_note(app, 1)
        if key == 'e' or key == 'r':
            app.game_p1_outer_drum_L = True
            game_p1_check_note(app, 2)
        if key == 'i' or key == 'u':
            app.game_p1_outer_drum_R = True
            game_p1_check_note(app, 2)

def game_onKeyRelease(app, key):
    if key == 'f' or key == 'j':
        app.game_p1_good = False
        app.game_p1_ok = False
        app.game_p1_bad = False
        app.game_p1_inner_drum_L = False
        app.game_p1_inner_drum_R = False
    if key == 'e' or key == 'i':
        app.game_p1_good = False
        app.game_p1_ok = False
        app.game_p1_bad = False
        app.game_p1_outer_drum_L = False
        app.game_p1_outer_drum_R = False

def game_onMousePress(app, mouseX, mouseY):
    print(mouseX, mouseY)