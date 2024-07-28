from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os

from global_funcs import *

def onScreenSwitch_result(app):
    app.result_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Result_In.wav').play().wait_done()
    app.result_bg_music = sa.WaveObject.from_wave_file('Sounds/Result.wav').play()
    app.result_index = 0
    app.result_sfx_gauge = None
    
def result_onAppStart(app):
    app.result_draw_bg_image = CMUImage(Image.open('Graphics/6_Result/Background_0.png'))
    app.result_draw_bg_mountain = CMUImage(Image.open('Graphics/6_Result/Background_Mountain_0.png'))
    app.result_draw_p1_panel = CMUImage(Image.open('Graphics/6_Result/Panel_1P/0.png'))
    app.result_draw_bg_header = CMUImage(Image.open('Graphics/6_Result/Header.png'))
    
    app.result_draw_p1_gauge_base = CMUImage(Image.open('Graphics/6_Result/Gauge_Base.png'))
    app.result_draw_p1_gauge = CMUImage(Image.open('Graphics/6_Result/Gauge.png').crop((0, 0, 1, 38)))
    app.result_draw_soul = CMUImage(Image.open('Graphics/6_Result/Soul_Text.png').crop((37, 0, 74, 36)))

def result_bgm_manager(app, music, path):
    if isinstance(music, sa.PlayObject):
        if not music.is_playing():
            app.result_bg_music = sa.WaveObject.from_wave_file(path).play()
    
def result_onStep(app):
    result_bgm_manager(app, app.result_bg_music, 'Sounds/Result.wav')
    app.result_index += 0.3
    if app.result_index == 0.3:
        app.result_sfx_gauge = sa.WaveObject.from_wave_file('Sounds/Result_Gauge.wav').play()
    result_gauge_manager(app, app.result_index, app.result_sfx_gauge)
    
def result_gauge_manager(app, index, gauge_sfx):
    gauge_bar_length = 10
    crop = (index*gauge_bar_length)
    if 0 < crop*1.42 < app.game_p1_gauge_crop:
        app.result_draw_p1_gauge = CMUImage(Image.open('Graphics/6_Result/Gauge.png').crop((0, 0, crop, 38)))
    if crop * 1.42 >= app.game_p1_gauge_crop:
        gauge_sfx.stop()
            
def result_draw_bg(app):
    drawImage(app.result_draw_bg_image, 0, 0)
    drawImage(app.result_draw_bg_mountain, 0, 0)
    drawImage(app.result_draw_p1_panel, 0, 0)
    drawImage(app.result_draw_bg_header, 0, 0)
    
def result_draw_p1_gauge(app):
    drawImage(app.result_draw_p1_gauge_base, 55, 141)
    drawImage(app.result_draw_p1_gauge, 55, 141)
    drawImage(app.result_draw_soul, 558, 140)
    
def result_redrawAll(app):
    result_draw_bg(app)
    result_draw_p1_gauge(app)
    drawLabel(app.game_p1_good_count, 580, 206, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.game_p1_ok_count, 580, 249, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.game_p1_bad_count, 580, 290, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.game_p1_max_combo, 580, 373, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.game_p1_score, 320, 240, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=5, size=55, fill='white', align='right')
    drawLabel(app.global_song_metadata[app.song_selected][0], app.width/2, 50, font='FOT-OedKtr Std E', border='black', bold=True, borderWidth=3, size=40, fill='white', align='center')
    
def result_onKeyPress(app, key):
    if key == 'enter':
        setActiveScreen('song_select')
        app.sfx_don.play().wait_done()
        sa.stop_all()
        app.song_select_bg_music_start = sa.WaveObject.from_wave_file('Sounds/SongSelect_start.wav').play().wait_done()
        app.song_select_bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
    switchScreen(app, key)