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
    app.result_draw_bg_image_half = CMUImage(Image.open('Graphics/6_Result/Background_0.png').crop((0, 0, app.width/2, app.height)))
    app.result_draw_bg_image_half_2 = CMUImage(Image.open('Graphics/6_Result/Background_2.png').crop((app.width/2, 0, app.width, app.height)))
    app.result_draw_bg_image_clear = CMUImage(Image.open('Graphics/6_Result/Background_1.png'))
    app.result_draw_bg_mountain = CMUImage(Image.open('Graphics/6_Result/Background_Mountain_0.png'))
    app.result_draw_1p_panel = CMUImage(Image.open('Graphics/6_Result/Panel_1P/0.png'))
    app.result_draw_2p_panel = CMUImage(Image.open('Graphics/6_Result/Panel_2P/0.png'))
    app.result_draw_bg_header = CMUImage(Image.open('Graphics/6_Result/Header.png'))
    app.result_draw_1p_gauge_base = CMUImage(Image.open('Graphics/6_Result/Gauge_Base.png'))
    app.result_draw_1p_gauge = CMUImage(Image.open('Graphics/6_Result/Gauge.png').crop((0, 0, 1, 38)))
    app.result_draw_2p_gauge_base = CMUImage(Image.open('Graphics/6_Result/Gauge_Base_2.png'))
    app.result_draw_2p_gauge = CMUImage(Image.open('Graphics/6_Result/Gauge_2.png').crop((0, 0, 1, 38)))
    app.result_draw_soul = CMUImage(Image.open('Graphics/6_Result/Soul_Text.png').crop((37, 0, 74, 36)))

    app.result_p1_crop = 0
    app.result_p2_crop = 0

def result_bgm_manager(app, music, path):
    if isinstance(music, sa.PlayObject):
        if not music.is_playing():
            app.result_bg_music = sa.WaveObject.from_wave_file(path).play()

def p1_gauge_manager(app, index, gauge_sfx):
    gauge_bar_length = 10
    app.result_p1_crop = (index*gauge_bar_length)
    if 0 < app.result_p1_crop*1.42 < app.player_1.gauge_crop:
        app.result_draw_1p_gauge = CMUImage(Image.open('Graphics/6_Result/Gauge.png').crop((0, 0, app.result_p1_crop, 38)))
    if app.result_p1_crop * 1.42 >= app.player_1.gauge_crop:
        gauge_sfx.stop()

def p2_gauge_manager(app, index, gauge_sfx):
    gauge_bar_length = 10
    app.result_p2_crop = (index*gauge_bar_length)
    if 0 < app.result_p2_crop*1.42 < app.player_2.gauge_crop:
        app.result_draw_2p_gauge = CMUImage(Image.open('Graphics/6_Result/Gauge_2.png').crop((0, 0, app.result_p2_crop, 38)))
    if app.result_p2_crop * 1.42 >= app.player_2.gauge_crop:
        gauge_sfx.stop()

def result_gauge_manager(app):
    app.result_index += 0.3
    if app.result_index == 0.3:
        app.result_p1_sfx_gauge = sa.WaveObject.from_wave_file('Sounds/Result_Gauge.wav').play()
        app.result_p2_sfx_gauge = sa.WaveObject.from_wave_file('Sounds/Result_Gauge.wav').play()
    p1_gauge_manager(app, app.result_index, app.result_p1_sfx_gauge)
    p2_gauge_manager(app, app.result_index, app.result_p2_sfx_gauge)

def result_onStep(app):
    result_bgm_manager(app, app.result_bg_music, 'Sounds/Result.wav')
    result_gauge_manager(app)

def result_draw_bg(app):
    if (app.result_p1_crop > 550 / 1.42) or (app.result_p2_crop > 550 / 1.42):
        drawImage(app.result_draw_bg_image_clear, 0, 0)
    elif app.players == 2:
        drawImage(app.result_draw_bg_image_half, 0, 0)
        drawImage(app.result_draw_bg_image_half_2, app.width/2, 0)
    else:
        drawImage(app.result_draw_bg_image, 0, 0)
    if app.players == 1:
        drawImage(app.result_draw_bg_mountain, 0, 0)
    drawImage(app.result_draw_bg_header, 0, 0)

def result_draw_1p_gauge(app):
    drawImage(app.result_draw_1p_gauge_base, 55, 141)
    drawImage(app.result_draw_1p_gauge, 55, 141)
    drawImage(app.result_draw_soul, 558, 140)

def result_draw_2p_gauge(app):
    drawImage(app.result_draw_2p_gauge_base, 688, 141)
    drawImage(app.result_draw_2p_gauge, 688, 141)
    drawImage(app.result_draw_soul, 1188, 140)

def result_draw_1p_panel(app):
    drawImage(app.result_draw_1p_panel, 0, 0)
    drawLabel(app.player_1.good_count, 580, 206, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.ok_count, 580, 249, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.bad_count, 580, 290, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.max_combo, 580, 373, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.score, 330, 240, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=5, size=55, fill='white', align='right')

def result_draw_2p_panel(app):
    drawImage(app.result_draw_2p_panel, 0, 0)
    drawLabel(app.player_2.good_count, 1220, 206, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.ok_count, 1220, 249, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.bad_count, 1220, 290, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.max_combo, 1220, 373, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.score, 966, 240, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=5, size=55, fill='white', align='right')

def result_redrawAll(app):
    result_draw_bg(app)
    result_draw_1p_panel(app)
    result_draw_2p_panel(app)
    result_draw_1p_gauge(app)
    result_draw_2p_gauge(app)
    drawLabel(app.global_song_metadata[app.song_selected][0], app.width/2, 50, font='FOT-OedKtr Std E', border='black', bold=True, borderWidth=3, size=40, fill='white', align='center')

def result_onKeyPress(app, key):
    if key == 'enter':
        setActiveScreen('song_select')
        app.sfx_don.play().wait_done()
        sa.stop_all()
        app.song_select_bg_music_start = sa.WaveObject.from_wave_file('Sounds/SongSelect_start.wav').play().wait_done()
        app.song_select_bg_music = sa.WaveObject.from_wave_file('Sounds/SongSelect.wav').play()
        app.song_select_difficulty = False
    switchScreen(app, key)
