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
        
        self.current_ms = 0
        
    def file_to_list(self):
        with open(self.file_path, 'rt', encoding='utf-8') as tja_file:
            for line in tja_file:
                line = stripComments(line.strip())
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
        notes = ''
        for i in range(len(self.data)):
            if '#START' in self.data[i]:
                note_start = i+1
                break
        for i in range(note_start, len(self.data)):
            item = self.data[i]
            if not '#END' in item:
                if '#' not in item:
                    notes += item
                elif '#MEASURE' in item:
                    notes += item + ','
            else:
                break
        return notes
    def data_to_notes(self, distance, pixels_per_ms):
        note_list = []
        notes = self.data_to_position()
        notes = notes.split(',')
        for i in range(len(notes)):
            if i >= len(notes):
                return note_list
            bar = notes[i].strip()
            if '#MEASURE' in bar:
                self.time_signature = float(int(bar[9])/int(bar[11]))
                #print(self.time_signature)
                continue
            ms_per_measure = 60000 * (self.time_signature*4) / self.bpm
            bar_ms = self.current_ms
            if len(bar) == 0:
                self.current_ms += ms_per_measure
            else:
                increment = ms_per_measure / len(bar)
                for note in bar:
                    note_ms = self.current_ms
                    #print(f'Note: {note}, {note_ms}')
                    if note != '0':
                        note_list.append({'note': note, 'ms': note_ms, 'load_ms': (note_ms - (distance / pixels_per_ms))})
                    self.current_ms += increment
            note_list.append({'note': 'barline', 'ms': bar_ms, 'load_ms': (bar_ms - (distance / pixels_per_ms))})
            #print(f'Bar: {i}, {bar_ms}, {(bar_ms - (distance / pixels_per_ms))}')
        #print(note_list)
        return(note_list)

def get_pixels_per_frame(app, bpm, fps, time_signature, judge_circle_x):
    beat_duration = fps / bpm
    total_time = time_signature * beat_duration
    total_frames = fps * total_time
    distance = app.width - judge_circle_x
    return (distance / total_frames) * (fps/60)
    
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

def play_tja(app, tja_folder):
    app.tja = tja_parser(tja_folder)
    app.tja.get_metadata()
    app.pixels_per_frame = get_pixels_per_frame(app, app.tja.bpm, app.stepsPerSecond, 
                                                app.tja.time_signature*4, (412 * app.scale_factor))
    pixels_per_ms = app.pixels_per_frame / (1000 / app.stepsPerSecond)                                               
    app.wave_obj = sa.WaveObject.from_wave_file(app.tja.wave)
    app.notes = app.tja.data_to_notes((app.width-app.p1_judge_x), pixels_per_ms)
    app.curr_notes = []
    app.note_index = 0
    app.start_song = True
    app.wave_obj.play()
    
def onStep(app):
    app.current_ms = get_current_ms() - app.start_ms
    app.fps_display = 1000 / (app.current_ms - app.last_ms)
    app.last_ms = app.current_ms
    
    if app.start_song:
        if app.note_index < len(app.notes) and app.current_ms > app.notes[app.note_index]['load_ms']:
            app.curr_notes.append(app.notes[app.note_index])
            app.note_index += 1
        if len(app.curr_notes) != 0:
            if app.curr_notes[0]['ms'] + app.timing_bad < app.current_ms:
                print(f'removed {app.curr_notes[0]}')
                app.curr_notes.pop(0)

def check_note(app, note_type):
    if len(app.curr_notes) != 0:
        note = app.curr_notes[0]['note']
        if note_type == 1:
            if note != '1' and note != '3':
                return
        elif note_type == 2:
            if note != '2' and note != '4':
                return
        note_ms = float(app.curr_notes[0]['ms'])
        if app.current_ms > (note_ms + app.timing_bad):
            return
        if (note_ms - app.timing_good) <= app.current_ms <= (note_ms + app.timing_good):
            print('GOOD')
            app.curr_notes.pop(0)
        elif (note_ms - app.timing_ok) <= app.current_ms <= (note_ms + app.timing_ok):
            print('OK')
            app.curr_notes.pop(0)
        elif (note_ms - app.timing_bad) <= app.current_ms <= (note_ms + app.timing_bad):
            print('BAD')
        
def onKeyPress(app, key):
    if key == 'p':
        play_tja(app, 'Isso Kono Mama De')
        app.start_ms = get_current_ms() - app.tja.offset*1000
    if key == 'f' or key == 'j':
        check_note(app, 1)
    if key == 'e' or key == 'i':
        check_note(app, 2)

def draw_p1_bg(app):
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY, app.width, app.p1_gray_bgY/1.05, fill=rgb(41,39,40))
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY+((app.p1_gray_bgY/5)*4), app.width, app.p1_gray_bgY/5, fill=rgb(133,131,132), border='black', borderWidth=8)
    
def draw_judge_circle(app):
    drawCircle(app.p1_judge_x, app.p1_judge_y, 25 * app.scale_factor, fill=rgb(42, 42, 40))
    drawCircle(app.p1_judge_x, app.p1_judge_y, 35 * app.scale_factor, fill=None, border=rgb(91,91,91), borderWidth=4)
    drawCircle(app.p1_judge_x, app.p1_judge_y, 50 * app.scale_factor, fill=None, border=rgb(56,56,56))
        
def draw_note(app, player, note, position):
    if player == 1:
        if note == 'barline':
            drawLine(position, app.p1_gray_bgY, position, app.p1_gray_bgY+((app.p1_gray_bgY/5)*4), fill=rgb(133,131,132), lineWidth=3)
            return
        if note == '1' or note == '3':
            note_color = rgb(224,56,39)
            name = 'Do'
        elif note == '2' or note == '4':
            note_color = rgb(78,210,193)
            name = 'Ka'
        else:
            return
        drawCircle(position, app.p1_judge_y, 35 * app.scale_factor, fill=note_color, border='white', borderWidth=5) 
        #drawCircle(position, app.p1_judge_y, 37 * app.scale_factor, fill=None, border='black', borderWidth=2) 
        drawLabel(name, position, app.p1_judge_y+93 * app.scale_factor, fill='white', border='black', size=20, borderWidth=1.5, bold=True)
        
def redrawAll(app):
    drawLabel(int(app.fps_display), 20, 20)
    draw_p1_bg(app)
    draw_judge_circle(app)
    if app.start_song:
        for note in app.curr_notes:
            note_type, note_ms = note['note'], note['ms']
            position = app.width + app.pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - app.current_ms)
            draw_note(app, 1, note_type, position - (app.width - app.p1_judge_x))
    
def main():
    runApp(width=1280,height=720)
    
main()