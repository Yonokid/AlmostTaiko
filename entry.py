from cmu_graphics import *
from PIL import Image
import simpleaudio as sa

from global_funcs import fps_counter, fps_manager, get_current_ms, switchScreen
from song_select import onScreenSwitch_song_select

def onScreenSwitch_entry(app):
    app.entry_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Title_start.wav').play().wait_done()
    app.entry_bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()
    
def entry_onAppStart(app):
    app.entry_draw_bg_image = CMUImage(Image.open('Graphics/1_Title/Background.png'))
    app.entry_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Title_start.wav').play().wait_done()
    app.entry_bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()

def entry_bgm_manager(app, music, path):
    if isinstance(music, sa.PlayObject):
        if not music.is_playing():
            app.entry_bg_music = sa.WaveObject.from_wave_file(path).play()
            
def entry_onStep(app):
    fps_manager(app)
    entry_bgm_manager(app, app.entry_bg_music, 'Sounds/Title.wav')
    
def entry_redrawAll(app):
    drawImage(app.entry_draw_bg_image, 0, 0)
    fps_counter(app)
    
def entry_onKeyPress(app, key):
    if key == 'enter':
        setActiveScreen('song_select')
        onScreenSwitch_song_select(app)
    switchScreen(app, key)