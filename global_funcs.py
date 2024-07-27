from cmu_graphics import *
import time
import os
import pathlib
from PIL import Image
import simpleaudio as sa

def get_current_ms():
    return rounded(time.time() * 1000)

def stripComments(code):
    #Written by Anthony Samms (ME) for one of the homework problems I think why do I need to cite this
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
        #Defined on startup
        self.folder_path = path
        self.folder_name = self.folder_path.split('\\')[-1]
        self.file_path = f'{self.folder_path}\\{self.folder_name}.tja'
        
        #Defined on file_to_data()
        self.data = []
        
        #Defined on get_metadata()
        self.title = ''
        self.title_ja = ''
        self.subtitle = ''
        self.subtitle_ja = ''
        self.wave = f'{self.folder_path}\\'
        self.offset = 0
        self.demo_start = 0
        self.course_data = dict()
        
        #Defined in metadata but can change throughout the chart
        self.bpm = 120
        self.time_signature = 4/4
        
        self.distance = 0
        self.fps = 0
        self.scroll_modifier = 1
        self.current_ms = 0
        self.barline_display = True
        
    def file_to_data(self):
        with open(self.file_path, 'rt', encoding='utf-8-sig') as tja_file:
            for line in tja_file:
                #print(line)
                line = stripComments(line).strip()
                if line != '':
                    self.data.append(str(line))
            return self.data
    
    def get_metadata(self):
        self.file_to_data()
        diff_index = 1
        highest_diff = -1
        for item in self.data:
            #print(item)
            if 'SUBTITLEJA' in item: self.subtitle_ja = str(item.split('SUBTITLEJA:')[1])
            elif 'TITLEJA' in item: self.title_ja = str(item.split('TITLEJA:')[1])
            elif 'SUBTITLE' in item: self.subtitle = str(item.split('SUBTITLE:')[1][2:])
            elif 'TITLE' in item: self.title = str(item.split('TITLE:')[1])
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
                diff_index -= 1
            elif 'LEVEL' in item:
                item = int(item.split(':')[1])
                self.course_data[diff_index+highest_diff].append(item)
            elif 'BALLOON' in item:
                item = item.split(':')[1]
                if item == '':
                    continue
                self.course_data[diff_index+highest_diff].append([int(x) for x in item.split(',')])
            elif 'SCOREINIT' in item:
                if item.split(':')[1] == '':
                    continue
                item = item.split(':')[1]
                self.course_data[diff_index+highest_diff].append([int(x) for x in item.split(',')])
            elif 'SCOREDIFF' in item:
                if item.split(':')[1] == '':
                    continue
                item = int(item.split(':')[1])
                self.course_data[diff_index+highest_diff].append(item)
            elif '#START' in item:
                return [self.title, self.title_ja, self.subtitle, self.subtitle_ja, self.bpm, self.wave, self.offset, self.demo_start, self.course_data]
                
    def data_to_notes(self):
        self.file_to_data()
        
        #Get notes start and end (only works on highest difficulty right now)
        note_start = -1
        note_end = -1
        for i in range(len(self.data)):
            if self.data[i] == '#START':
                note_start = i+1
            elif self.data[i] == '#END':
                note_end = i
                break
                      
        notes = []
        bar = []
        #Check for measures and separate when comma exists
        for i in range(note_start, note_end):
            item = self.data[i].strip(',')
            bar.append(item)
            if item != self.data[i]:
                notes.append(bar)
                bar = []
        return notes
        
    def notes_to_position(self):
        play_note_list = []
        bar_list = []
        draw_note_list = []
        notes = self.data_to_notes()
        index = 0
        for bar in notes:
            #Length of the bar is determined by number of notes excluding commands
            bar_length = sum(len(part) for part in bar if '#' not in part)
            
            for part in bar:
                if '#MEASURE' in part:
                    divisor = part.find('/')
                    self.time_signature = float(part[9:divisor]) / float(part[divisor+1:])
                    continue
                elif '#SCROLL' in part:
                    self.scroll_modifier = float(part[7:])
                    continue
                elif '#BPMCHANGE' in part:
                    self.bpm = float(part[11:])
                    continue
                elif '#BARLINEOFF' in part:
                    self.barline_display = False
                    continue
                elif '#BARLINEON' in part:
                    self.barline_display = True
                    continue
                #Unrecognized commands will be skipped for now
                elif '#' in part:
                    continue
                    
                #https://gist.github.com/KatieFrogs/e000f406bbc70a12f3c34a07303eec8b#measure
                ms_per_measure = 60000 * (self.time_signature*4) / self.bpm
                
                #Determines how quickly the notes need to move across the screen to reach the judgment circle in time
                pixels_per_frame = get_pixels_per_frame(self.bpm * self.time_signature * self.scroll_modifier, self.fps, self.time_signature*4, self.distance)
                pixels_per_ms = pixels_per_frame / (1000 / self.fps)
                
                bar_ms = self.current_ms
                load_ms = bar_ms - (self.distance / pixels_per_ms)
                
                if self.barline_display:
                    bar_list.append({'note': 'barline', 'ms': bar_ms, 'load_ms': load_ms, 'ppf': pixels_per_frame})
                
                #Empty bar is still a bar, otherwise start increment
                if len(part) == 0:
                    self.current_ms += ms_per_measure
                else:
                    increment = ms_per_measure / bar_length
                
                for note in part:
                    note_ms = self.current_ms
                    #Do not add blank notes otherwise lag
                    if note != '0':
                        load_ms = note_ms - (self.distance / pixels_per_ms)
                        play_note_list.append({'note': note, 'ms': note_ms, 'load_ms': load_ms, 'ppf': pixels_per_frame, 'index': index})
                        print({'note': note, 'ms': int(note_ms), 'load_ms': int(load_ms), 'ppf': int(pixels_per_frame), 'index': index})
                        index += 1
                    self.current_ms += increment
                
        # https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
        # Sorting by load_ms is necessary for drawing, as some notes appear on the
        # screen slower regardless of when they reach the judge circle
        # Bars can be sorted like this because they don't need hit detection
        draw_note_list = sorted(play_note_list, key=lambda d: d['load_ms'])
        bar_list = sorted(bar_list, key=lambda d: d['load_ms'])
        return play_note_list, draw_note_list, bar_list

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
        
def loadSound(path):
    full_path = os.path.abspath(path)
    url = pathlib.Path(full_path).as_uri()
    return Sound(url)
    
def switchScreen(app, key):
    if key == '0':
        sa.stop_all()
        setActiveScreen('title')
    elif key == '1':
        sa.stop_all()
        setActiveScreen('entry')
        sa.WaveObject.from_wave_file('Sounds/Title_start.wav').play().wait_done()
        app.bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()
    elif key == '2':
        sa.stop_all()
        setActiveScreen('song_select')
        sa.WaveObject.from_wave_file('Sounds/SongSelect_start.wav').play().wait_done()
        app.bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
    elif key == '3':
        sa.stop_all()
        setActiveScreen('game')
    elif key == '4':
        sa.stop_all()
        setActiveScreen('result')

def fps_counter(app):
    if app.fps_display >= 55:
        fps_color = 'green'
    elif 30 <= app.fps_display < 55:
        fps_color = 'yellow'
    else:
        fps_color = 'red'
    drawLabel(int(app.fps_display), 80, 40, size=40, fill=fps_color, bold=True, border='black')