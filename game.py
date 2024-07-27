from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os
import random as rand
import math

from global_funcs import *

def game_onAppStart(app):
    app.start_ms = 0
    app.current_ms = 0
    
    app.last_ms = 0
    app.fps_display = 0
    
    #Anything higher than 60 will have no effect
    app.stepsPerSecond = 60
    app.current_frame = 0
    app.start_frame = 0
    
    #Just in case some nutjob wants to run this in 1080p
    width_scale_factor = app.width / 1280
    height_scale_factor = app.height / 720
    app.scale_factor = (width_scale_factor + height_scale_factor) / 2
    
    app.timing_good = 25.0250015258789
    app.timing_ok = 75.0750045776367
    app.timing_bad = 108.441665649414
    
    app.p1_good = False
    app.p1_ok = False
    app.p1_bad = False
    app.p1_autoplay = False
    
    app.p1_don_L = False
    app.p1_don_R = False
    app.p1_kat_L = False
    app.p1_kat_R = False
    
    app.p1_judge_x = 412
    #Not implemented, skip
    app.ignored_notes = {'5','6','7','8','9'}
    #This will be changable in the future
    app.p1_judge_offset = 30
    
    app.p1_current_notes = []
    app.p1_current_bars = []
    app.p1_current_notes_draw = []
    app.p1_play_note_index = 0
    app.p1_draw_note_index = 0
    app.p1_bar_index = 0
    app.p1_play_song = False
    
    app.gauge_index = 0
    app.gauge_count = 0
    app.crop = 0
    
    app.result_delay = 0
    
    ##########
    ##Graphics
    ##########
    
    app.draw_arc_dict = dict()
    app.arc_points = 25
    
    app.background_main = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Main.png'))
    app.background_sub = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Sub.png'))
    app.p1_frame = CMUImage(Image.open('Graphics/5_Game/6_Taiko/1P_Frame.png'))
    app.p1_background = CMUImage(Image.open('Graphics/5_Game/6_Taiko/1P_Background.png'))
    
    app.p1_judge_circle = Image.open('Graphics/5_Game/Notes.png').crop((10, 11, 117, 118))
    app.p1_judge_circle = CMUImage(app.p1_judge_circle.convert('RGBA').convert('RGBa'))
    
    app.drum = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Base.png'))
    app.red_L = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Don.png').crop((0, 0, 59, 88)))
    app.red_R = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Don.png').crop((59, 0, 104, 88)))
    app.blue_L = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Ka.png').crop((0, 0, 59, 115)))
    app.blue_R = CMUImage(Image.open('Graphics/5_Game/6_Taiko/Ka.png').crop((59, 0, 119, 115)))
    
    app.don = None
    app.kat = None
    app.dai_don = None
    app.dai_kat = None
    
    app.don_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((158, 29, 229, 100)))
    app.kat_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((288, 29, 359, 100)))
    app.don_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((158, 159, 229, 230)))
    app.kat_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((288, 159, 359, 230)))
    
    app.dai_don_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((400, 10, 507, 118)))
    app.dai_kat_1 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((530, 10, 637, 118)))
    app.dai_don_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((400, 141, 507, 248)))
    app.dai_kat_2 = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((530, 141, 637, 248)))
    
    app.barline = CMUImage(Image.open('Graphics/5_Game/Bar.png').crop((0, 0, 4, 129)))
    
    background_number = rand.randint(0, 2)
    app.background_down = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_down/1/0.png'))
    app.background_up = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_up/2/Main.PNG'))
    app.footer = CMUImage(Image.open(f'Graphics/5_Game/8_Footer/{background_number}.png'))
    
    app.p1_gauge_base = CMUImage(Image.open('Graphics/7_Gauge/1P_base.png').crop((0, 0, 695, 43)))
    app.p1_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((0, 0, 1, 43)))
    app.soul = CMUImage(Image.open('Graphics/7_Gauge/Soul.png').crop((0, 0, 80, 80)))

def reset_song(app):
    app.p1_current_notes = []
    app.p1_current_bars = []
    app.p1_current_notes_draw = []
    app.p1_play_note_index = 0
    app.p1_draw_note_index = 0
    app.p1_bar_index = 0
    app.p1_play_song = True
    app.gauge_index = 0
    app.gauge_count = 0
    app.crop = 0
    app.result_delay = 0
    app.p1_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((0, 0, 1, 43)))
    
    app.p1_good_count = 0
    app.p1_ok_count = 0
    app.p1_bad_count = 0
    app.p1_combo = 0
    app.p1_score = 0
    app.p1_max_combo = 0
    
def play_tja(app, tja_folder):
    reset_song(app)
    app.tja = tja_parser(tja_folder)
    app.tja.get_metadata()
    
    #100 is the radius of the outer judgment circle
    app.tja.distance = (app.width + 100) - (app.p1_judge_x * app.scale_factor)
    app.tja.fps = app.stepsPerSecond                              
    app.start_ms = get_current_ms() - app.tja.offset*1000    
    app.music = sa.WaveObject.from_wave_file(app.tja.wave)
    
    app.play_notes, app.draw_notes, app.bars = app.tja.notes_to_position()
    
    #https://outfox.wiki/en/dev/mode-support/tja-support
    app.note_count = (sum(1 for key in app.play_notes if key.get('note') in {'1','2','3','4'}))
    app.note_count_with_roll = (sum(1 for key in app.play_notes))
    print(app.note_count_with_roll)
    app.base_score = (1000000 / app.note_count) / 10
    app.base_score = math.ceil(app.base_score) * 10
    #app.music = loadSound(app.tja.wave)    
    app.music.play()
    
def game_onStep(app):
    app.current_frame += 1
    app.current_ms = get_current_ms() - app.start_ms
    app.fps_display = 1000 / (app.current_ms - app.last_ms)
    app.last_ms = app.current_ms
    
    eighth_in_ms = (60000 * 4 / 190) / 8
    current_eighth = app.current_ms // eighth_in_ms
    if current_eighth % 2 == 0:
        app.don = app.don_1
        app.kat = app.kat_1
        app.dai_don = app.dai_don_1
        app.dai_kat = app.dai_kat_1
    else:
        app.don = app.don_2
        app.kat = app.kat_2
        app.dai_don = app.dai_don_2
        app.dai_kat = app.dai_kat_2
    if app.p1_play_song:
        game_note_manager(app)
    if app.result_delay != 0:
        print(app.result_delay, app.current_ms)
        if app.current_ms >= app.result_delay + 2000:
            if app.p1_bad_count == 0:
                sa.WaveObject.from_wave_file('Sounds/Full combo.wav').play().wait_done()
            elif app.crop >= 545:
                sa.WaveObject.from_wave_file('Sounds/Clear.wav').play().wait_done()
            else:
                sa.WaveObject.from_wave_file('Sounds/Failed.wav').play().wait_done()
            sa.WaveObject.from_wave_file('Sounds/Result_In.wav').play().wait_done()
            app.bg_music = sa.WaveObject.from_wave_file('Sounds/Result.wav').play()
            app.result_index = 0
            app.gauge_sfx = None
            setActiveScreen('result')
            return

def game_note_manager(app):
    if app.p1_autoplay:
        game_check_note(app, 1)
        game_check_note(app, 2)
    #Add bar to current_bars list if it is ready to be shown on screen
    if app.p1_bar_index < len(app.bars) and app.current_ms > app.bars[app.p1_bar_index]['load_ms']:
        app.p1_current_bars.append(app.bars[app.p1_bar_index])
        app.p1_bar_index += 1
    #Add note to current_notes list if it is ready to be shown on screen
    if app.p1_play_note_index < len(app.play_notes) and app.current_ms > app.play_notes[app.p1_play_note_index]['load_ms']:
        app.p1_current_notes.append(app.play_notes[app.p1_play_note_index])
        app.p1_play_note_index += 1
    if app.p1_draw_note_index < len(app.draw_notes) and app.current_ms > app.draw_notes[app.p1_draw_note_index]['load_ms']:
        app.p1_current_notes_draw.append(app.draw_notes[app.p1_draw_note_index])
        #print(f'note added {app.p1_current_notes_draw[0]}')
        app.p1_draw_note_index += 1
    #if a note was not hit within the window, remove it
    if len(app.p1_current_notes) != 0:
            if app.p1_current_notes[0]['ms'] + app.timing_bad < app.current_ms:
                current_note = app.p1_current_notes[0]['note']
                app.p1_current_notes.pop(0)
                if current_note not in app.ignored_notes:
                    app.p1_combo = 0
                    app.p1_bad_count += 1
                    game_check_end(app, app.p1_current_notes[0]['index'])
    if len(app.p1_current_bars) != 0:
        for i in range(len(app.p1_current_bars)-1, -1, -1):
            bar_ms, pixels_per_frame = app.p1_current_bars[i]['ms'], app.p1_current_bars[i]['ppf']
            position = pixels_per_frame * app.stepsPerSecond / 1000 * (bar_ms - app.current_ms + app.p1_judge_offset)
            if position < app.p1_judge_x - 600:
                app.p1_current_bars.pop(i)
    if len(app.p1_current_notes_draw) != 0:
        for i in range(len(app.p1_current_notes_draw)-1, -1, -1):
            note_ms, pixels_per_frame = app.p1_current_notes_draw[i]['ms'], app.p1_current_notes_draw[i]['ppf']
            position = pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - app.current_ms + app.p1_judge_offset)
            if position < app.p1_judge_x - 600:
                app.p1_current_notes_draw.pop(i)
    if len(app.draw_arc_dict) != 0:
        remove_keys = set()
        for start_frame in app.draw_arc_dict:
            if app.current_frame >= start_frame + math.floor(app.arc_points * 0.92):
                remove_keys.add(start_frame)
        app.arc_points = 25 - len(app.draw_arc_dict)
        for key in remove_keys:
            app.draw_arc_dict.pop(key)

def game_check_end(app, index):
    if index == app.note_count_with_roll-1:
        if app.result_delay == 0:
            app.result_delay = app.current_ms
def game_check_note(app, note_type):
    if len(app.p1_current_notes) != 0:
        note = app.p1_current_notes[0]['note']
        index = app.p1_current_notes[0]['index']
        don_notes = {'1','3'}
        kat_notes = {'2','4'}
        if note_type == 1:
            if note not in don_notes:
                return
        if note_type == 2:
            if note not in kat_notes:
                return
        note_ms = float(app.p1_current_notes[0]['ms'])
        if app.current_ms > (note_ms + app.timing_bad):
            return
        if (note_ms - app.timing_good) + app.p1_judge_offset <= app.current_ms <= (note_ms + app.timing_good) + app.p1_judge_offset:
            app.p1_good = True
            app.p1_good_count += 1
            app.p1_combo += 1
            if app.p1_combo > app.p1_max_combo:
                app.p1_max_combo = app.p1_combo
            app.p1_score += app.base_score
            app.start_frame = app.current_frame
            game_gauge_manager(app)
            app.draw_arc_dict[app.start_frame] = app.p1_current_notes[0]['note']
            game_check_end(app, app.p1_current_notes[0]['index'])
            app.p1_current_notes.pop(0)
            for note in range(len(app.p1_current_notes_draw)):
                if app.p1_current_notes_draw[note]['index'] == index:
                    app.p1_current_notes_draw.pop(note)
                    break
        elif (note_ms - app.timing_ok) + app.p1_judge_offset <= app.current_ms <= (note_ms + app.timing_ok) + app.p1_judge_offset:
            app.p1_ok = True
            app.p1_ok_count += 1
            app.p1_combo += 1
            if app.p1_combo > app.p1_max_combo:
                app.p1_max_combo = app.p1_combo
            app.p1_score += 10 * math.floor(app.base_score / 2 / 10)
            app.start_frame = app.current_frame
            game_gauge_manager(app)
            app.draw_arc_dict[app.start_frame] = app.p1_current_notes[0]['note']
            game_check_end(app, app.p1_current_notes[0]['index'])
            app.p1_current_notes.pop(0)
            for note in range(len(app.p1_current_notes_draw)):
                if app.p1_current_notes_draw[note]['index'] == index:
                    app.p1_current_notes_draw.pop(note)
                    break
        elif (note_ms - app.timing_bad) + app.p1_judge_offset <= app.current_ms <= (note_ms + app.timing_bad) + app.p1_judge_offset:
            app.p1_combo = 0
            app.p1_bad = True
            game_check_end(app, app.p1_current_notes[0]['index'])
            app.p1_bad_count += 1
        

def game_gauge_manager(app):
    gauge_bar_length = 14
    app.gauge_count = app.p1_good_count + (app.p1_ok_count/2)
    if app.gauge_count == 0:
        return
    if int(app.gauge_count) % math.floor(app.note_count / 63.391) == 0:
        app.gauge_index += 1
    app.crop = (app.gauge_index*gauge_bar_length) + (app.p1_bad_count * -(gauge_bar_length/2))
    if app.crop > 0:
        app.p1_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((1, 0, app.crop, 43)))

def game_get_note_type(note):
    if note == '1':
        return app.don
    elif note == '2':
        return app.kat
    elif note == '3':
        return app.dai_don
    elif note == '4':
        return app.dai_kat
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
    if frames_since_call > app.arc_points:
        frames_since_call = app.arc_points
    angle_change = (theta_end - theta_start) / app.arc_points
    theta_i = theta_start + frames_since_call * angle_change
    x_i = center_x + radius * math.cos(theta_i)
    y_i = center_y + radius * 0.5 * math.sin(theta_i)
    drawImage(note_type, x_i, y_i)
        
    
def game_draw_note(app, player, note, position):
    if player == 1:
        if note == 'barline':
            note_type = app.barline
            drawImage(note_type, position, 192)
            return
        if game_get_note_type(note) != None:
            drawImage(game_get_note_type(note), position, 256, align='center') 
    
def game_draw_background(app):
    drawImage(app.background_down, 0, 360)
    for i in range(4):
        drawImage(app.background_up, 0+(i*326), 0)
    drawImage(app.footer, 0, 720-44)
    
def game_draw_lane(app):
    drawImage(app.background_main, 333, 192)
    drawImage(app.background_sub, 333, 326)
    drawImage(app.p1_frame, 329, 136)
    drawImage(app.p1_judge_circle, 359, 203)
    
def game_draw_judgments(app):
    if app.p1_autoplay: 
        drawLabel('AUTO', app.p1_judge_x, 162, size=30, fill='white', bold=True, border='black')
        return
    elif app.p1_good: drawLabel('GOOD', app.p1_judge_x, 162, size=30, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
    elif app.p1_ok: drawLabel('OK', app.p1_judge_x, 162, size=30, fill='white', bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
    elif app.p1_bad: drawLabel('BAD', app.p1_judge_x, 162, size=30, fill=gradient('deepSkyBlue','royalBlue','indigo', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)

def game_draw_drum(app):
    drawImage(app.drum, 190, 210)
    if app.p1_don_L:
        drawImage(app.red_L, 190, 210)
    if app.p1_don_R:
        drawImage(app.red_R, 190+59, 210)
    if app.p1_kat_L:
        drawImage(app.blue_L, 190, 210)
    if app.p1_kat_R:
        drawImage(app.blue_R, 190+59, 210)
    if 10 <= app.p1_combo:
        drawLabel(app.p1_combo, 250, 250, size=50, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=3)

def game_draw_gauge(app):
    drawImage(app.p1_gauge_base, 493, 144)
    drawImage(app.soul, 1199, 125)
    drawImage(app.p1_gauge, 493, 144)
    
def game_redrawAll(app):
    game_draw_background(app)
    game_draw_lane(app)
    game_draw_gauge(app)
    if len(app.p1_current_notes_draw) != 0 or len(app.p1_current_bars) != 0:
        for i in range(len(app.p1_current_bars)):
            bar = app.p1_current_bars[i]
            bar_ms, pixels_per_frame = bar['ms'], bar['ppf']
            position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (bar_ms - app.current_ms + app.p1_judge_offset)
            game_draw_note(app, 1, 'barline', position - (app.width - app.p1_judge_x))
        for i in range(len(app.p1_current_notes_draw)):
            note = app.p1_current_notes_draw[i]
            note_type, note_ms, pixels_per_frame = note['note'], note['ms'], note['ppf']
            position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - app.current_ms + app.p1_judge_offset)
            game_draw_note(app, 1, note_type, position - (app.width - app.p1_judge_x))
    if len(app.draw_arc_dict) != 0:
            for start_frame in app.draw_arc_dict:
                game_draw_note_arc(game_get_note_type(app.draw_arc_dict[start_frame]), app.current_frame, start_frame)
    drawImage(app.p1_background, 0, 184)
    drawLabel(app.p1_score, 190, 208, align='right', size=35, border='black', fill='white', borderWidth=3, bold=True, font='DFPKanTeiRyu-XB')
    game_draw_drum(app)
    game_draw_judgments(app)
    fps_counter(app)
 
def game_onKeyPress(app, key):
    switchScreen(app, key)
    if key == 'a':
        app.p1_autoplay = not app.p1_autoplay
    if not app.p1_autoplay:
        if key == 'f' or key == 'd':
            app.p1_don_L = True
            game_check_note(app, 1)
        if key == 'j' or key == 'k':
            app.p1_don_R = True
            game_check_note(app, 1)
        if key == 'e' or key == 'r':
            app.p1_kat_L = True
            game_check_note(app, 2)
        if key == 'i' or key == 'u':
            app.p1_kat_R = True
            game_check_note(app, 2)

def game_onKeyRelease(app, key):
    if key == 'f' or key == 'j':
        app.p1_good = False
        app.p1_ok = False
        app.p1_bad = False
        app.p1_don_L = False
        app.p1_don_R = False
    if key == 'e' or key == 'i':
        app.p1_good = False
        app.p1_ok = False
        app.p1_bad = False
        app.p1_kat_L = False
        app.p1_kat_R = False

def game_onMousePress(app, mouseX, mouseY):
    print(mouseX, mouseY)