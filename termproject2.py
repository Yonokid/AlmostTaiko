from cmu_graphics import *
import simpleaudio as sa
import time
import os

def get_current_ms():
    return rounded(time.time() * 1000)

def stripComments(code):
    #Written by Anthony Samms (ME)
    result = ''
    index = 0
    is_line = True
    for line in code.splitlines():
        comment_index = line.find('//')
        if comment_index == -1:
            result += line
            is_line = True
        elif comment_index != 0 and not line[:comment_index].isspace():
            result += line[:comment_index]
            is_line = True
        else:
            is_line = False
        index += 1
    return result

def get_pixels_per_frame(bpm, fps, time_signature, distance):
    beat_duration = fps / bpm
    total_time = time_signature * beat_duration
    total_frames = fps * total_time
    return (distance / total_frames) * (fps/60)
    
class tja_parser:
    def __init__(self, path):
        self.folder_path = path
        self.folder_name = self.folder_path.split('\\')[-1]
        self.file_path = f'{self.folder_path}\\{self.folder_name}.tja'
        self.data = []
        self.title = ''
        self.title_ja = ''
        self.subtitle = ''
        self.subtitle_ja = ''
        self.bpm = 120
        self.time_signature = 4/4
        self.wave = f'{self.folder_path}\\'
        self.offset = 0
        self.demo_start = 0
        self.course_data = dict()
        self.distance = 0
        self.fps = 0
        self.scroll_modifier = 1
        
        self.current_ms = 0
        
    def file_to_list(self):
        with open(self.file_path, 'rt', encoding='utf-8') as tja_file:
            for line in tja_file:
                line = stripComments(line).strip()
                if line != '':
                    self.data.append(str(line))
            return self.data    
            
    def get_metadata(self):
        self.file_to_list()
        i = 1
        highest_diff = -1
        for item in self.data:
            if 'SUBTITLEJA' in item: self.subtitle_ja = str(item.split(':')[1])
            elif 'TITLEJA' in item: self.title_ja = str(item.split(':')[1])
            elif 'SUBTITLE' in item: self.subtitle = str(item.split(':')[1][2:])
            elif 'TITLE' in item: self.title = str(item.split(':')[1])
            elif 'BPM' in item: self.bpm = float(item.split(':')[1])
            elif 'WAVE' in item: self.wave += str(item.split(':')[1])
            elif 'OFFSET' in item: self.offset = float(item.split(':')[1])
            elif 'DEMOSTART' in item: self.demo_start = float(item.split(':')[1])
            elif 'COURSE' in item:
                course = str(item.split(':')[1]).lower()  
                if course == 'edit' or course == '4':
                    self.course_data[4] = []
                elif course == 'oni' or course == '3':
                    self.course_data[3] = []
                elif course == 'hard' or course == '2':    
                    self.course_data[2] = []
                elif course == 'normal' or course == '1':
                    self.course_data[1] = []
                elif course == 'easy' or course == '0':
                    self.course_data[0] = []
                highest_diff = max(self.course_data)
                i -= 1
            elif 'LEVEL' in item:
                item = int(item.split(':')[1])
                self.course_data[i+highest_diff].append(item)
            elif 'BALLOON' in item:
                item = item.split(':')[1]
                self.course_data[i+highest_diff].append([int(x) for x in item.split(',')])
            elif 'SCOREINIT' in item:
                item = item.split(':')[1]
                self.course_data[i+highest_diff].append([int(x) for x in item.split(',')])
            elif 'SCOREDIFF' in item:
                item = int(item.split(':')[1])
                self.course_data[i+highest_diff].append(item)
        return self.title, self.title_ja, self.subtitle, self.subtitle_ja, self.bpm, self.wave, self.offset, self.demo_start, self.course_data
    
    def data_to_position(self):
        self.file_to_list()
        
        note_start = -1
        note_end = -1
        for i in range(len(self.data)):
            if self.data[i] == '#START':
                note_start = i+1
            elif self.data[i] == '#END':
                note_end = i
                break
                      
        notes = []
        #print(self.data[note_start:note_end])
        temp_item = []
        for i in range(note_start, note_end):
            item = self.data[i]
            if item[-1] == ',':
                item = item[:-1]
                temp_item.append(item)
                #notes.append(',')
                notes.append(temp_item)
                temp_item = []
            else:
                temp_item.append(item)
        return notes
        
    def data_to_notes(self):
        note_list = []
        bar_list = []
        notes = self.data_to_position()
        '''
        for i in range(len(notes)):
            if i >= len(notes):
                return note_list
            bar = notes[i].strip()
            if '#MEASURE' in bar:
                self.time_signature = float(int(bar[9])/int(bar[11]))
                #print(self.time_signature)
                continue
            ms_per_measure = 60000 * (self.time_signature*4) / self.bpm
            
            pixels_per_frame = get_pixels_per_frame(self.bpm * self.time_signature, self.fps, self.time_signature*4, self.distance)
            pixels_per_ms = pixels_per_frame / (1000 / self.fps)
                    
            bar_ms = self.current_ms
            load_ms = bar_ms - (self.distance / pixels_per_ms)
            bar_list.append({'note': 'barline', 'ms': bar_ms, 'load_ms': load_ms, 'ppf': pixels_per_frame})
            if len(bar) == 0:
                self.current_ms += ms_per_measure
            else:
                increment = ms_per_measure / len(bar)
                for note in bar:
                    note_ms = self.current_ms    
                    #print(f'Note: {note}, {note_ms}')
                    if note != '0':
                        pixels_per_frame = get_pixels_per_frame(self.bpm * self.time_signature, self.fps, self.time_signature*4, self.distance)
                        pixels_per_ms = pixels_per_frame / (1000 / self.fps)
                        load_ms = note_ms - (self.distance / pixels_per_ms)
                        note_list.append({'note': note, 'ms': note_ms, 'load_ms': load_ms, 'ppf': pixels_per_frame})
                    self.current_ms += increment
            #print(f'Bar: {i}, {bar_ms}, {(bar_ms - (distance / pixels_per_ms))}')
        #print(note_list)
        '''
        for bar in notes:
            bar_len = 0
            for part in bar:
                if '#' not in part:
                    bar_len += len(part)
                    
            for part in bar:
                if '#MEASURE' in part:
                    self.time_signature = float(int(part[9])/int(part[11]))
                    continue
                elif '#SCROLL' in part:
                    self.scroll_modifier = float(part[7:])
                    continue
                elif '#' in part:
                    continue
                ms_per_measure = 60000 * (self.time_signature*4) / self.bpm
                
                pixels_per_frame = get_pixels_per_frame(self.bpm * self.time_signature * self.scroll_modifier, self.fps, self.time_signature*4, self.distance)
                pixels_per_ms = pixels_per_frame / (1000 / self.fps)
                    
                bar_ms = self.current_ms
                load_ms = bar_ms - (self.distance / pixels_per_ms)
                bar_list.append({'note': 'barline', 'ms': bar_ms, 'load_ms': load_ms, 'ppf': pixels_per_frame})
                if len(part) == 0:
                    self.current_ms += ms_per_measure
                else:
                    increment = ms_per_measure / bar_len
                for note in part:
                    note_ms = self.current_ms
                    if note != '0':
                        load_ms = note_ms - (self.distance / (pixels_per_ms))
                        note_list.append({'note': note, 'ms': note_ms, 'load_ms': load_ms, 'ppf': pixels_per_frame})
                        print({'note': note, 'ms': int(note_ms), 'load_ms': int(load_ms), 'ppf': pixels_per_frame})
                    self.current_ms += increment
        return(note_list, bar_list)
    
def onAppStart(app):
    app.start_ms = 0
    app.current_ms = 0
    
    app.last_ms = 0
    app.fps_display = 0
    
    app.start_song = False
    app.stepsPerSecond = 60
    
    width_scale_factor = app.width / 1280
    height_scale_factor = app.height / 720
    app.scale_factor = (width_scale_factor + height_scale_factor) / 2
    
    app.p1_gray_bgX = 0 * app.scale_factor
    app.p1_gray_bgY = 185 * app.scale_factor
    app.p1_judge_x = 412 * app.scale_factor
    app.p1_judge_y = 257 * app.scale_factor
    
    app.timing_good = 25.0250015258789
    app.timing_ok = 75.0750045776367
    app.timing_bad = 108.441665649414
    
    app.good = False
    app.ok = False
    app.bad = False
    app.autoplay = False
    
    app.don_L = False
    app.don_R = False
    app.kat_L = False
    app.kat_R = False
    
    app.combo = 0
    
    app.judge_offset = 30

def play_tja(app, tja_folder):
    app.tja = tja_parser(tja_folder)
    app.tja.get_metadata()
    app.tja.distance = app.width - (412 * app.scale_factor)
    app.tja.fps = app.stepsPerSecond                                           
    app.wave_obj = sa.WaveObject.from_wave_file(app.tja.wave)
    app.notes, app.bars = app.tja.data_to_notes()
    app.curr_notes = []
    app.curr_bars = []
    app.note_index = 0
    app.bar_index = 0
    app.start_song = True
    app.wave_obj.play()
    
def onStep(app):
    app.current_ms = get_current_ms() - app.start_ms
    app.fps_display = 1000 / (app.current_ms - app.last_ms)
    app.last_ms = app.current_ms
    ignore = {'5','6','7','8','9'}
    
    if app.start_song:
        if app.autoplay:
            check_note(app, 1)
            check_note(app, 2)
        if app.bar_index < len(app.bars) and app.current_ms > app.bars[app.bar_index]['load_ms']:
            app.curr_bars.append(app.bars[app.bar_index])
            app.bar_index += 1
        if app.note_index < len(app.notes) and app.current_ms > app.notes[app.note_index]['load_ms']:
            app.curr_notes.append(app.notes[app.note_index])
            app.note_index += 1
        if len(app.curr_bars) != 0:
            if app.curr_bars[0]['ms'] + app.timing_bad < app.current_ms:
                app.curr_bars.pop(0)
        if len(app.curr_notes) != 0:
            if app.curr_notes[0]['ms'] + app.timing_bad < app.current_ms:
                #print(f'removed {app.curr_notes[0]}')
                curr_note = app.curr_notes[0]['note']
                app.curr_notes.pop(0)
                if curr_note not in ignore:
                    app.combo = 0

def check_note(app, note_type):
    if len(app.curr_notes) != 0:
        note = app.curr_notes[0]['note']
        don_notes = {'1','3'}
        kat_notes = {'2','4'}
        if note_type == 1:
            if note not in don_notes:
                return
        if note_type == 2:
            if note not in kat_notes:
                return
        note_ms = float(app.curr_notes[0]['ms'])
        if app.current_ms > (note_ms + app.timing_bad):
            return
        if (note_ms - app.timing_good) + app.judge_offset <= app.current_ms <= (note_ms + app.timing_good) + app.judge_offset:
            app.good = True
            app.combo += 1
            app.curr_notes.pop(0)
        elif (note_ms - app.timing_ok) + app.judge_offset <= app.current_ms <= (note_ms + app.timing_ok) + app.judge_offset:
            app.ok = True
            app.combo += 1
            app.curr_notes.pop(0)
        elif (note_ms - app.timing_bad) + app.judge_offset <= app.current_ms <= (note_ms + app.timing_bad) + app.judge_offset:
            app.combo = 0
            app.bad = True
        
def onKeyPress(app, key):
    if key == 'p':
        play_tja(app, 'SUPERNOVA')
        app.start_ms = get_current_ms() - app.tja.offset*1000
    if key == 'a':
        app.autoplay = not app.autoplay
    if not app.autoplay:
        if key == 'f':
            app.don_L = True
            check_note(app, 1)
        if key == 'j':
            app.don_R = True
            check_note(app, 1)
        if key == 'e':
            app.kat_L = True
            check_note(app, 2)
        if key == 'i':
            app.kat_R = True
            check_note(app, 2)
        
def onKeyRelease(app, key):
    if key == 'f' or key == 'j':
        #sa.WaveObject.from_wave_file('inst_00_don.wav').play()
        app.good = False
        app.ok = False
        app.bad = False
        app.don_L = False
        app.don_R = False
    if key == 'e' or key == 'i':
        #sa.WaveObject.from_wave_file('inst_00_katsu.wav').play()
        app.good = False
        app.ok = False
        app.bad = False
        app.kat_L = False
        app.kat_R = False
        
def draw_p1_bg(app):
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY, app.width, app.p1_gray_bgY/1.05, fill=rgb(41,39,40))
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY+((app.p1_gray_bgY/5)*4), app.width, app.p1_gray_bgY/5, fill=rgb(133,131,132), border='black', borderWidth=8)
    
def draw_judge_circle(app):
    drawCircle(app.p1_judge_x, app.p1_judge_y, 25 * app.scale_factor, fill=rgb(42, 42, 40))
    drawCircle(app.p1_judge_x, app.p1_judge_y, 35 * app.scale_factor, fill=None, border=rgb(91,91,91), borderWidth=4)
    drawCircle(app.p1_judge_x, app.p1_judge_y, 50 * app.scale_factor, fill=None, border=rgb(56,56,56))
        
def draw_note(app, player, note, position):
    if note == 'barline':
        drawLine(position, app.p1_gray_bgY, position, app.p1_gray_bgY+((app.p1_gray_bgY/5)*4), fill=rgb(133,131,132), lineWidth=3)
        return
    elif note == '1':
        note_scale = 1
        note_color = rgb(224,56,39)
        name = 'Do'
    elif note == '3':
        note_scale = 1.5
        note_color = rgb(224,56,39)
        name = 'DON!'
    elif note == '2':
        note_scale = 1
        note_color = rgb(78,210,193)
        name = 'Ka'
    elif note == '4':
        note_scale = 1.5
        note_color = rgb(78,210,193)
        name = 'KAT!'
    else:
        return
    if player == 1:
        drawCircle(position, app.p1_judge_y,  35 * note_scale * app.scale_factor, fill=note_color, border='white', borderWidth=5 * note_scale) 
        #drawCircle(position, app.p1_judge_y, 37 * app.scale_factor, fill=None, border='black', borderWidth=2) 
        drawLabel(name, position, app.p1_judge_y+93 * app.scale_factor, fill='white', border='black', size=20, borderWidth=1.5, bold=True)

def draw_judgments(app):
    if app.autoplay: 
        drawLabel('AUTO', app.p1_judge_x, app.p1_judge_y-100, size=30, fill='white', bold=True, border='black')
        return
    elif app.good: drawLabel('GOOD', app.p1_judge_x, app.p1_judge_y-100, size=30, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black')
    elif app.ok: drawLabel('OK', app.p1_judge_x, app.p1_judge_y-100, size=30, fill='white', bold=True, border='black')
    elif app.bad: drawLabel('BAD', app.p1_judge_x, app.p1_judge_y-100, size=30, fill=gradient('deepSkyBlue','royalBlue','indigo', start='bottom'), bold=True, border='black')

def draw_drum(app):
    offset_from_judge = -120 * app.scale_factor
    drawRect(0, app.p1_gray_bgY, app.p1_judge_x-(60*app.scale_factor), app.p1_gray_bgY, fill=gradient(rgb(240,148,118), rgb(205,15,15), start='bottom'), border='black', borderWidth=8)
    drawOval(app.p1_judge_x+offset_from_judge, app.p1_judge_y+(10 * app.scale_factor), 80, 100, fill=rgb(115,32,15))
    drawCircle(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 40, fill='beige')
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY, app.width, app.p1_gray_bgY, fill=None, border='black', borderWidth=8)
    if app.kat_L:
        drawArc(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 80, 80, 90, 180, fill=None, border=rgb(78,210,193), borderWidth=10)
        drawCircle(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 30, fill='beige')
    if app.kat_R:
        drawArc(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 80, 80, -90, 180, fill=None, border=rgb(78,210,193), borderWidth=10)
        drawCircle(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 30, fill='beige')
    if app.don_L:
        drawArc(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 60, 60, 90, 180, fill=rgb(224,56,39))
    if app.don_R:
        drawArc(app.p1_judge_x+offset_from_judge, app.p1_judge_y, 60, 60, -90, 180, fill=rgb(224,56,39))
    if 10 <= app.combo:
        drawLabel(app.combo, app.p1_judge_x+offset_from_judge, app.p1_judge_y, size=40, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black')
        #drawLabel(app.combo, app.p1_judge_x+offset_from_judge, app.p1_judge_y, size=40, fill='white', bold=True, border='black')
    #elif 50 <= app.combo < 100:
        #drawLabel(app.combo, app.p1_judge_x+offset_from_judge, app.p1_judge_y, size=app.combo_size, fill=gradient(rgb(167, 173, 187), rgb(170,188,210), start='bottom'), bold=True, border='black')
    #elif 100 <= app.combo:
        #drawLabel(app.combo, app.p1_judge_x+offset_from_judge, app.p1_judge_y, size=app.combo_size, fill=gradient(rgb(235, 198, 143), rgb(243,171,76), start='bottom'), bold=True, border='black')
        
def redrawAll(app):
    fps_color = 'green' if app.fps_display >= 55 else 'yellow'
    drawLabel(int(app.fps_display), 40, 40, size=40, fill=fps_color, bold=True, border='black')
    draw_p1_bg(app)
    draw_judge_circle(app)
    draw_judgments(app)
    if app.start_song:
        for bar in app.curr_bars:
            bar_ms, pixels_per_frame = bar['ms'], bar['ppf']
            position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (bar_ms - app.current_ms + app.judge_offset)
            draw_note(app, 1, 'barline', position - (app.width - app.p1_judge_x))
        for note in app.curr_notes:
            note_type, note_ms, pixels_per_frame = note['note'], note['ms'], note['ppf']
            position = app.width + pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - app.current_ms + app.judge_offset)
            draw_note(app, 1, note_type, position - (app.width - app.p1_judge_x))
    draw_drum(app)
def main():
    runApp(width=1280,height=720)
    
main()