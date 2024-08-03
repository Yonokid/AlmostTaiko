from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os
import random as rand
import math
from collections import deque

#All images and sounds created by BANDAI NAMCO ENTERTAINMENT

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

    ##########
    ##Graphics
    ##########

    app.game_draw_background_main = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Main.png'))
    app.game_draw_background_sub = CMUImage(Image.open('Graphics/5_Game/12_Lane/Background_Sub.png'))
    app.game_draw_frame = CMUImage(Image.open('Graphics/5_Game/6_Taiko/1P_Frame.png'))
    app.game_draw_background = CMUImage(Image.open('Graphics/5_Game/6_Taiko/1P_Background.png'))

    app.game_draw_judge_circle = CMUImage(Image.open('Graphics/5_Game/Notes.png').crop((10, 11, 117, 118)))

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
    app.game_draw_background_up_clear = CMUImage(Image.open('Graphics/5_Game/5_Background/Bg_up/2/Main_Clear.png'))
    app.game_draw_footer = CMUImage(Image.open(f'Graphics/5_Game/8_Footer/{background_number}.png'))

    app.game_draw_gauge_base = CMUImage(Image.open('Graphics/5_Game/7_Gauge/1P_base.png').crop((0, 0, 695, 43)))
    #app.game_draw_gauge = CMUImage(Image.open('Graphics/7_Gauge/1P.png').crop((0, 0, app.game_p1_gauge_crop, 43)))
    app.game_draw_soul = CMUImage(Image.open('Graphics/5_Game/7_Gauge/Soul.png').crop((0, 0, 80, 80)))

    app.judge_timer = 0

class Player:
    def __init__(self, player_number):
        self.player_number = player_number
        #Judgment Display
        self.good = False
        self.ok = False
        self.bad = False
        self.autoplay = False
        self.judge_timer = 0

        #Drum Display
        self.inner_drum_L = False
        self.inner_drum_R = False
        self.outer_drum_L = False
        self.outer_drum_R = False

        #This will be changable in the future
        #Guide:
        #PC Speakers = 30
        #External Speaker = 60
        #Creston Keyboard = 60
        #Creston Drum = 75
        self.judge_offset = 75

        #Note management for p1
        self.current_notes = deque()
        self.current_bars = []
        self.current_notes_draw = []
        self.play_note_index = 0
        self.draw_note_index = 0
        self.bar_index = 0

        #Gauge management for p1
        self.gauge_count = 0
        self.gauge_crop = 1
        self.clear = False

        #Score management for p1
        self.good_count = 0
        self.ok_count = 0
        self.bad_count = 0
        self.combo = 0
        self.score = 0
        self.max_combo = 0

        #Arc management
        self.draw_arc_dict = dict()
        self.draw_arc_points = 25
        self.draw_current_frame = 0
        self.draw_start_frame = 0
        if self.player_number == 1:
            self.draw_gauge = CMUImage(Image.open('Graphics/5_Game/7_Gauge/1P.png').crop((0, 0, 1, 43)))
        else:
            self.draw_gauge = CMUImage(Image.open('Graphics/5_Game/7_Gauge/2P.png').crop((0, 0, 1, 43)))

        #AI Battle display
        self.section_good_count = 0
        self.section_ok_count = 0
        self.section_bad_count = 0

    def get_position(self, app, ms, pixels_per_frame):
        return pixels_per_frame * app.stepsPerSecond / 1000 * (ms - app.current_ms + self.judge_offset)

    def note_manager(self, app, song_play_notes, song_bars, song_draw_notes):
        if self.autoplay:
            self.check_note(app, 1)
            self.check_note(app, 2)
        #Add bar to current_bars list if it is ready to be shown on screen
        if self.bar_index < len(song_bars) and app.current_ms > song_bars[self.bar_index]['load_ms']:
            self.current_bars.append(song_bars[self.bar_index])
            self.bar_index += 1

        #Add note to current_notes list if it is ready to be shown on screen
        if self.play_note_index < len(song_play_notes) and app.current_ms > song_play_notes[self.play_note_index]['load_ms']:
            self.current_notes.append(song_play_notes[self.play_note_index])
            self.play_note_index += 1
        if self.draw_note_index < len(song_draw_notes) and app.current_ms > song_draw_notes[self.draw_note_index]['load_ms']:
            self.current_notes_draw.append(song_draw_notes[self.draw_note_index])
            self.draw_note_index += 1

        #if a note was not hit within the window, remove it
        if len(self.current_notes) != 0:
            note = self.current_notes[0]
            if note['ms'] + app.timing_bad < app.current_ms:
                if note['note'] not in app.game_ignored_notes:
                    self.combo = 0
                    self.bad_count += 1
                    self.section_bad_count += 1
                    self.game_check_end(app, note['index'])
                self.current_notes.popleft()
                if app.ai_battle and self.player_number == 2:
                    if app.section_crop < 120:
                        app.section_crop +=  120 / app.sections[0]

        #If a bar is off screen, remove it
        if len(self.current_bars) != 0:
            for i in range(len(self.current_bars)-1, -1, -1):
                bar_ms, pixels_per_frame = self.current_bars[i]['ms'], self.current_bars[i]['ppf']
                position = self.get_position(app, bar_ms, pixels_per_frame)
                if position < app.game_judge_x - 600:
                    self.current_bars.pop(i)

        #If a note is off screen, remove it
        if len(self.current_notes_draw) != 0:
            for i in range(len(self.current_notes_draw)-1, -1, -1):
                note_ms, pixels_per_frame = self.current_notes_draw[i]['ms'], self.current_notes_draw[i]['ppf']
                position = self.get_position(app, note_ms, pixels_per_frame)
                if position < app.game_judge_x - 600:
                    self.current_notes_draw.pop(i)

        #If a note has reached the soul icon, remove it
        if len(self.draw_arc_dict) != 0:
            remove_keys = set()
            for start_frame in self.draw_arc_dict:
                if self.draw_current_frame >= start_frame + math.floor(self.draw_arc_points * 0.92):
                    remove_keys.add(start_frame)
            #Control the speed of the notes in the arc so game doesn't lag
            self.draw_arc_points = 25 - len(self.draw_arc_dict)
            for key in remove_keys:
                self.draw_arc_dict.pop(key)

    def game_check_end(self, app, index):
        if index == app.song_note_count_with_roll-1:
            if app.game_result_delay == 0:
                app.game_result_delay = app.current_ms

    def note_correct(self, app, note):
        index = note['index']

        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo

        self.draw_start_frame = self.draw_current_frame
        self.draw_arc_dict[self.draw_start_frame] = note['note']

        self.gauge_manager(app)
        self.game_check_end(app, index)

        self.current_notes.popleft()

        #Remove note from the screen
        for note in range(len(self.current_notes_draw)):
            if self.current_notes_draw[note]['index'] == index:
                self.current_notes_draw.pop(note)
                break

    def check_note(self, app, drum_type):
        if len(self.current_notes) != 0:
            note_type = self.current_notes[0]['note']
            index = self.current_notes[0]['index']
            note_ms = float(self.current_notes[0]['ms'])
            #If the wrong key was hit, stop checking
            if drum_type == 1 and note_type not in {'1','3'}:
                return
            if drum_type == 2 and note_type not in {'2','4'}:
                return
            #If the note is too far away, stop checking
            if app.current_ms > (note_ms + app.timing_bad):
                return

            if (note_ms - app.timing_good) + self.judge_offset <= app.current_ms <= (note_ms + app.timing_good) + self.judge_offset:
                self.good = True
                self.judge_timer = app.current_ms
                self.good_count += 1
                self.section_good_count += 1
                self.score += app.song_base_score
                self.note_correct(app, self.current_notes[0])

            elif (note_ms - app.timing_ok) + self.judge_offset <= app.current_ms <= (note_ms + app.timing_ok) + self.judge_offset:
                self.ok = True
                self.judge_timer = app.current_ms
                self.good = False
                self.ok_count += 1
                self.section_ok_count += 1
                self.score += 10 * math.floor(app.song_base_score / 2 / 10)
                self.note_correct(app, self.current_notes[0])

            elif (note_ms - app.timing_bad) + self.judge_offset <= app.current_ms <= (note_ms + app.timing_bad) + self.judge_offset:
                self.combo = 0
                self.judge_timer = app.current_ms
                self.bad = True
                self.ok = False
                self.good = False
                self.bad_count += 1
                self.section_bad_count += 1
                self.game_check_end(app, self.current_notes[0]['index'])

    def draw_judgments(self, app):
        if self.player_number == 1:
            y = 182 - ((app.current_ms - self.judge_timer)*0.7)
            if y <= 140:
                y = 150
        else:
            y = 364 - ((app.current_ms - self.judge_timer)*0.7)
            if y <= 324:
                y = 334
        if self.autoplay: drawLabel('AUTO', app.game_judge_x, y, size=30, fill='white', bold=True, border='black')
        elif self.good: drawLabel('GOOD', app.game_judge_x, y, size=30, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
        elif self.ok: drawLabel('OK', app.game_judge_x, y, size=30, fill='white', bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)
        elif self.bad: drawLabel('BAD', app.game_judge_x, y, size=30, fill=gradient('deepSkyBlue','royalBlue','indigo', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=2.5)

    def spawn_notes(self, app):
        if len(self.current_notes_draw) != 0 or len(self.current_bars) != 0:
            for i in range(len(self.current_bars)):
                bar = self.current_bars[i]
                bar_ms, pixels_per_frame = bar['ms'], bar['ppf']
                position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (bar_ms - app.current_ms + self.judge_offset)
                game_draw_note(app, self.player_number, 'barline', position - (app.width - app.game_judge_x))
            for i in range(len(self.current_notes_draw)):
                note = self.current_notes_draw[i]
                note_type, note_ms, pixels_per_frame = note['note'], note['ms'], note['ppf']
                position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - app.current_ms + self.judge_offset)
                game_draw_note(app, self.player_number, note_type, position - (app.width - app.game_judge_x))

    def draw_note_arc(self, note_type, current_frame, start_frame, draw_arc_points):
        radius = 400
        #Start at 180 degrees, end at 0
        theta_start = 3.14
        if self.player_number == 1:
            theta_end = 2 * 3.14
            #center of circle that does not exist
            center_x, center_y = 785, 168
        else:
            theta_end = 0
            center_x, center_y = 785, 468

        frames_since_call = current_frame - start_frame
        if frames_since_call < 0:
            frames_since_call = 0
        if frames_since_call > draw_arc_points:
            frames_since_call = draw_arc_points
        angle_change = (theta_end - theta_start) / draw_arc_points
        theta_i = theta_start + frames_since_call * angle_change
        x_i = center_x + radius * math.cos(theta_i)
        y_i = center_y + radius * 0.5 * math.sin(theta_i)
        drawImage(note_type, x_i, y_i)

    def draw_arc(self, app):
        if len(self.draw_arc_dict) != 0:
            for start_frame in self.draw_arc_dict:
                self.draw_note_arc(game_get_note_type(self.draw_arc_dict[start_frame]), self.draw_current_frame, start_frame, self.draw_arc_points)

    def gauge_manager(self, app):
        gauge_bar_length = 14
        self.gauge_count = self.good_count + (self.ok_count/2) + (self.bad_count * -2)
        if self.gauge_count == 0:
            return
        gauge_bar = math.floor(app.song_note_count / 63.391)
        self.gauge_crop = ((self.gauge_count // gauge_bar)*gauge_bar_length)
        if self.gauge_crop > 0:
            if self.player_number == 1:
                self.draw_gauge = CMUImage(Image.open('Graphics/5_Game/7_Gauge/1P.png').crop((1, 0, self.gauge_crop, 43)))
            else:
                self.draw_gauge = CMUImage(Image.open('Graphics/5_Game/7_Gauge/2P.png').crop((1, 0, self.gauge_crop, 43)))

def play_tja(app, tja_folder):
    #Initialize p1
    app.player_1 = Player(1)
    app.game_play_song = True
    app.game_result_delay = 0

    #Initialize TJA file
    app.tja = tja_parser(tja_folder)
    app.tja.get_metadata()
    app.tja.distance = app.width - app.game_judge_x
    app.tja.fps = app.stepsPerSecond

    app.start_ms = get_current_ms() - app.tja.offset*1000

    app.song_music = sa.WaveObject.from_wave_file(app.tja.wave)

    app.song_play_notes, app.song_draw_notes, app.song_bars = app.tja.notes_to_position(app.song_1p_diff)

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
        if app.player_1.bad_count == 0:
            if app.ai_battle:
                sa.WaveObject.from_wave_file('Sounds/AI_battle_full_combo.wav').play().wait_done()
            else:
                sa.WaveObject.from_wave_file('Sounds/Full combo.wav').play().wait_done()
        elif app.ai_battle:
            if app.section_wins.count(True) >= 3:
                sa.WaveObject.from_wave_file('Sounds/AI_battle_win.wav').play().wait_done()
            elif app.section_wins.count(False) >= 3:
                sa.WaveObject.from_wave_file('Sounds/AI_battle_lose.wav').play().wait_done()
        elif app.player_1.gauge_crop >= 545:
            sa.WaveObject.from_wave_file('Sounds/Clear.wav').play().wait_done()
        else:
            sa.WaveObject.from_wave_file('Sounds/Failed.wav').play().wait_done()
        onScreenSwitch_result(app)
        setActiveScreen('result')

def game_onStep(app):
    app.player_1.draw_current_frame += 1
    fps_manager(app)
    game_animate_notes(app)

    if app.game_play_song:
        app.player_1.note_manager(app, app.song_play_notes, app.song_bars, app.song_draw_notes)

    if app.game_result_delay != 0:
        game_song_finished(app)
    game_judge_display(app)

def game_judge_display(app):
    if app.player_1.judge_timer + 200 <= app.current_ms:
        app.player_1.good = False
        app.player_1.ok = False
        app.player_1.bad = False

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

def game_draw_note(app, player, note, position):
    if note == 'barline':
        note_type = app.game_draw_barline
        if player == 1:
            y = 192
        else:
            y = 370.5
        drawImage(note_type, position, y)
    elif game_get_note_type(note) != None:
        if player == 1:
            drawImage(game_get_note_type(note), position, 256, align='center')
        elif player == 2:
            drawImage(game_get_note_type(note), position, 434.5, align='center')

def game_draw_background(app):
    drawImage(app.game_draw_background_down, 0, 360)
    if app.player_1.gauge_crop < 550:
        up_image = app.game_draw_background_up
    else:
        up_image = app.game_draw_background_up_clear
    for i in range(4):
        drawImage(up_image, 0+(i*326), 0)
    drawImage(app.game_draw_footer, 0, 720-44)

def game_draw_lane(app):
    drawImage(app.game_draw_background_main, 333, 192)
    drawImage(app.game_draw_background_sub, 333, 326)
    drawImage(app.game_draw_frame, 329, 136)
    drawImage(app.game_draw_judge_circle, 359, 203)

def game_draw_drum(app):
    drum_x = 205
    drawImage(app.game_draw_background, 0, 184)
    drawImage(app.game_draw_drum, drum_x, 210)
    if app.player_1.inner_drum_L:
        drawImage(app.game_draw_red_L, drum_x, 210)
    if app.player_1.inner_drum_R:
        drawImage(app.game_draw_red_R, drum_x+59, 210)
    if app.player_1.outer_drum_L:
        drawImage(app.game_draw_blue_L, drum_x, 210)
    if app.player_1.outer_drum_R:
        drawImage(app.game_draw_blue_R, drum_x+59, 210)
    if 10 <= app.player_1.combo:
        drawLabel(app.player_1.combo, drum_x+60, 250, size=50, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black', font='DFPKanTeiRyu-XB', borderWidth=3)
    drawLabel(app.player_1.score, 190, 208, align='right', size=35, border='black', fill='white', borderWidth=3, bold=True, font='DFPKanTeiRyu-XB')

def game_draw_gauge(app):
    drawImage(app.game_draw_gauge_base, 493, 144)
    drawImage(app.game_draw_soul, 1199, 125)
    drawImage(app.player_1.draw_gauge, 493, 144)

def game_redrawAll(app):
    game_draw_background(app)
    game_draw_lane(app)
    game_draw_gauge(app)

    #draw notes and bars
    app.player_1.spawn_notes(app)
    #Draw arc
    app.player_1.draw_arc(app)

    drawLabel(app.player_1.score, 190, 208, align='right', size=35, border='black', fill='white', borderWidth=3, bold=True, font='DFPKanTeiRyu-XB')
    game_draw_drum(app)
    app.player_1.draw_judgments(app)
    fps_counter(app)

def game_onKeyPress(app, key):
    if key == 'a':
        app.player_1.autoplay = not app.player_1.autoplay
    elif key == 'escape':
        sa.stop_all()
        app.sfx_cancel.play().wait_done()
        app.song_1p_confirmed = False
        app.song_2p_confirmed = False
        setActiveScreen('song_select')
    if not app.player_1.autoplay:
        if key == 'f':
            app.player_1.inner_drum_L = True
            app.player_1.check_note(app, 1)
        if key == 'j':
            app.player_1.inner_drum_R = True
            app.player_1.check_note(app, 1)
        if key == 'e':
            app.player_1.outer_drum_L = True
            app.player_1.check_note(app, 2)
        if key == 'i':
            app.player_1.outer_drum_R = True
            app.player_1.check_note(app, 2)

def game_onKeyRelease(app, key):
    if key == 'f' or key == 'j':
        app.player_1.inner_drum_L = False
        app.player_1.inner_drum_R = False
    if key == 'e' or key == 'i':
        app.player_1.outer_drum_L = False
        app.player_1.outer_drum_R = False
