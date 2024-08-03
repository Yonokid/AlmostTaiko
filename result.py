from cmu_graphics import *
from PIL import Image
import simpleaudio as sa
import os
import random as rand

#All images and sounds created by BANDAI NAMCO ENTERTAINMENT

from global_funcs import *

def onScreenSwitch_result(app):
    app.result_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Result_In.wav').play().wait_done()
    app.result_bg_music = sa.WaveObject.from_wave_file('Sounds/Result.wav').play()
    app.result_index = 0
    app.result_sfx_gauge = None

def result_onAppStart(app):

    app.result_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Result_In.wav')
    app.result_bg_music = sa.WaveObject.from_wave_file('Sounds/Result.wav')
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
    app.result_draw_ai_background = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/ai_background_result.png'))
    app.result_draw_ai_panel = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((14, 20, 639, 553)))
    app.result_draw_ai_section_bg = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((1096, 850, 1254, 999)))
    app.result_draw_ai_section_win = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((1151, 1153, 1296, 1293)))
    app.result_draw_ai_section_lose = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((1177, 584, 1323, 722)))
    app.result_draw_ai_win = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((361, 1141, 612, 1339)))
    app.result_draw_ai_win_bg = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((358, 573, 698, 831)))
    app.result_draw_ai_lose = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((872, 841, 1092, 1012)))
    app.result_draw_ai_section = CMUImage(Image.open('Graphics/5_Game/13_AiBattle/result_ai_section.png').crop((706, 786, 817, 812)))

    app.result_draw_difficulty_bar = [CMUImage(Image.open('Graphics/6_Result/DifficultyBar.png').crop((3, 11, 184, 54))),
                                      CMUImage(Image.open('Graphics/6_Result/DifficultyBar.png').crop((3, 68, 184, 108))),
                                      CMUImage(Image.open('Graphics/6_Result/DifficultyBar.png').crop((3, 119, 184, 162))),
                                      CMUImage(Image.open('Graphics/6_Result/DifficultyBar.png').crop((3, 164, 184, 216))),
                                      CMUImage(Image.open('Graphics/6_Result/DifficultyBar.png').crop((3, 218, 184, 270)))]

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
    if app.players == 2:
        p2_gauge_manager(app, app.result_index, app.result_p2_sfx_gauge)

def result_onStep(app):
    result_bgm_manager(app, app.result_bg_music, 'Sounds/Result.wav')
    result_gauge_manager(app)

def result_draw_bg(app):
    if (app.result_p1_crop > 550 / 1.42) or (app.result_p2_crop > 550 / 1.42):
        drawImage(app.result_draw_bg_image_clear, 0, 0)
    if app.ai_battle:
        drawImage(app.result_draw_ai_background, 0, 0)
    elif app.players == 2:
        drawImage(app.result_draw_bg_image_half, 0, 0)
        drawImage(app.result_draw_bg_image_half_2, app.width/2, 0)
        drawImage(app.result_draw_bg_header, 0, 0)
    else:
        drawImage(app.result_draw_bg_image, 0, 0)
        drawImage(app.result_draw_bg_header, 0, 0)
    if app.players == 1:
        drawImage(app.result_draw_bg_mountain, 0, 0)

def result_draw_1p_gauge(app):
    drawImage(app.result_draw_1p_gauge_base, 58, 141)
    drawImage(app.result_draw_1p_gauge, 58, 141)
    drawImage(app.result_draw_soul, 558, 140)

def result_draw_2p_gauge(app):
    drawImage(app.result_draw_2p_gauge_base, 688, 141)
    drawImage(app.result_draw_2p_gauge, 688, 141)
    drawImage(app.result_draw_soul, 1188, 140)

def result_draw_1p_panel(app):
    drawImage(app.result_draw_1p_panel, 0, 0)
    if app.song_1p_diff in {3, 4}:
        y = 103
    else:
        y = 115
    drawImage(app.result_draw_difficulty_bar[app.song_1p_diff], 21, y)
    drawLabel(app.player_1.good_count, 580, 206, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.ok_count, 580, 249, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.bad_count, 580, 290, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.max_combo, 580, 373, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_1.score, 330, 240, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=5, size=55, fill='white', align='right')

def result_draw_2p_panel(app):
    drawImage(app.result_draw_2p_panel, 0, 0)
    if app.song_2p_diff in {3, 4}:
        y = 103
    else:
        y = 115
    drawImage(app.result_draw_difficulty_bar[app.song_2p_diff], 658, y)
    drawLabel(app.player_2.good_count, 1220, 206, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.ok_count, 1220, 249, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.bad_count, 1220, 290, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.max_combo, 1220, 373, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=3, size=35, fill='white', align='right')
    drawLabel(app.player_2.score, 966, 240, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=5, size=55, fill='white', align='right')

def result_draw_ai_panel(app):
    drawImage(app.result_draw_ai_panel, 650, 140)
    drawLabel('VS. AI-Don', 962.5, 160, font='DFPKanTeiRyu-XB', border='white', bold=True, borderWidth=2, size=20, fill='black', align='center')
    for i in range(5):
        if i % 2 == 1:
            y = 50
        else:
            y = 0
        drawImage(app.result_draw_ai_section, 702+(i*100), 220+y)
        drawLabel(f'Section {i}', 760+(i*100), 232+y, font='DFPKanTeiRyu-XB', border='black', bold=True, borderWidth=1.5, size=15, fill='white', align='center')
        drawImage(app.result_draw_ai_section_bg, 680+(i*100), 250+y)
        if app.section_wins[i] == True:
            drawImage(app.result_draw_ai_section_win, 687.5+i*100, 254+y)
        elif app.section_wins[i] == False:
            drawImage(app.result_draw_ai_section_lose, 686+i*100, 256+y)
    if app.section_wins.count(True) >= 3:
        drawImage(app.result_draw_ai_win_bg, 962.5, 550, align='center')
        drawImage(app.result_draw_ai_win, 962.5, 550, align='center')
    elif app.section_wins.count(False) >= 3:
        drawImage(app.result_draw_ai_lose, 962.5, 550, align='center')

def result_redrawAll(app):
    result_draw_bg(app)
    result_draw_1p_panel(app)
    if app.ai_battle:
        result_draw_ai_panel(app)
    elif app.players == 2:
        result_draw_2p_panel(app)
    result_draw_1p_gauge(app)
    if app.players == 2 and not app.ai_battle:
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
        app.ai_difficulty = rand.randint(1, 5)
