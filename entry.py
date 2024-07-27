from cmu_graphics import *
from PIL import Image
import simpleaudio as sa

from global_funcs import loadSound, fps_counter, get_current_ms, switchScreen

def entry_onAppStart(app):
    #FPS counter vars
    app.current_ms = 0
    app.start_ms = 0
    app.last_ms = 0
    app.fps_display = 0
    
    app.stepsPerSecond = 60
    app.bg_image = CMUImage(Image.open('Graphics/1_Title/Background.png'))
    sa.WaveObject.from_wave_file('Sounds/Title_start.wav').play().wait_done()
    app.bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()
    
def entry_onStep(app):
    app.current_ms = get_current_ms() - app.start_ms
    app.fps_display = 1000 / (app.current_ms - app.last_ms)
    app.last_ms = app.current_ms
    if isinstance(app.bg_music, sa.PlayObject):
        if not app.bg_music.is_playing():
            app.bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()
            return
   
def entry_redrawAll(app):
    drawImage(app.bg_image, 0, 0)
    fps_counter(app)
    
def entry_onKeyPress(app, key):
    if key == 'enter':
        setActiveScreen('song_select')
        sa.WaveObject.from_wave_file('Sounds/inst_00_don.wav').play().wait_done()
        sa.stop_all()
        sa.WaveObject.from_wave_file('Sounds/SongSelect_start.wav').play().wait_done()
        app.bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
    switchScreen(app, key)