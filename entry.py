from cmu_graphics import *
from PIL import Image
import simpleaudio as sa

from global_funcs import fps_counter, fps_manager, get_current_ms, switchScreen
from song_select import onScreenSwitch_song_select

#All images and sounds created by BANDAI NAMCO ENTERTAINMENT

def onScreenSwitch_entry(app):
    app.entry_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Title_start.wav').play().wait_done()
    app.entry_bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()
    app.ai_battle = False

def entry_onAppStart(app):
    app.entry_draw_bg_image = CMUImage(Image.open('Graphics/1_Title/Background.png'))
    app.entry_draw_network_status = CMUImage(Image.open('Graphics/1_Title/NetworkStatus/0.png'))
    app.entry_draw_banapass = CMUImage(Image.open('Graphics/1_Title/Bana_OK.png'))
    app.entry_draw_select_p1 = CMUImage(Image.open('Graphics/1_Title/Mode/Enso/Bar.png'))
    app.entry_draw_select_p1_chara = CMUImage(Image.open('Graphics/1_Title/Mode/Enso/Chara.png'))
    app.entry_draw_select_p2 = CMUImage(Image.open('Graphics/1_Title/Mode/Dan/Bar.png'))
    app.entry_draw_select_p2_chara = CMUImage(Image.open('Graphics/1_Title/Mode/Dan/Chara.png'))
    app.entry_draw_select_cpu = CMUImage(Image.open('Graphics/1_Title/Mode/AI/Bar.png'))
    app.entry_draw_select_cpu_chara = CMUImage(Image.open('Graphics/1_Title/Mode/AI/Chara.png'))

    app.entry_draw_select_mode = CMUImage(Image.open('Graphics/1_Title/Mode/YellowFrameBack.png'))
    app.entry_select_mode = True

    app.entry_current_pos_x = 10
    app.entry_mode_movement = 30

    app.players = 0
    app.ai_battle = False

    app.entry_bg_music_start = sa.WaveObject.from_wave_file('Sounds/Title_start.wav').play().wait_done()
    app.entry_bg_music = sa.WaveObject.from_wave_file('Sounds/Title.wav').play()

def entry_bgm_manager(app, music, path):
    if isinstance(music, sa.PlayObject):
        if not music.is_playing():
            app.entry_bg_music = sa.WaveObject.from_wave_file(path).play()

def entry_onStep(app):
    fps_manager(app)
    entry_bgm_manager(app, app.entry_bg_music, 'Sounds/Title.wav')
    if not app.entry_select_mode:
        app.entry_current_pos_x += app.entry_mode_movement
        if app.entry_current_pos_x == 1300:
            app.entry_select_mode = True
        elif app.entry_current_pos_x == 10:
            app.entry_select_mode = True
        elif app.entry_current_pos_x == -1310:
            app.entry_select_mode = True

def entry_redrawAll(app):
    drawImage(app.entry_draw_bg_image, 0, 0)
    drawImage(app.entry_draw_network_status, 0, 0)
    drawImage(app.entry_draw_banapass, 0, 0)

    if app.entry_select_mode:
        drawImage(app.entry_draw_select_mode, 18, 0)

    p1_location = app.entry_current_pos_x+(app.width/2)
    drawImage(app.entry_draw_select_p1, p1_location, app.height/2, align='center')
    drawImage(app.entry_draw_select_p1_chara, app.entry_current_pos_x, 0)
    drawLabel('1 PLAYER', p1_location, (app.height/2)-50, align='center', font='DFPKanTeiRyu-XB', fill='black', size=60, border='black', borderWidth=10)
    drawLabel('1 PLAYER', p1_location, (app.height/2)-50, align='center', font='DFPKanTeiRyu-XB', fill='white', size=60, border=rgb(198, 9, 51), borderWidth=4)
    drawLabel(f'Play on your own', p1_location, (app.height/2)+25, align='center', font='FOT-Seurat Pro', size=20, bold=True)
    drawLabel(f'to get the best score!', p1_location, (app.height/2)+50, align='center', font='FOT-Seurat Pro', size=20, bold=True)

    p2_location = (app.entry_current_pos_x-app.width/2)-15
    drawImage(app.entry_draw_select_p2, p2_location, app.height/2, align='center')
    drawImage(app.entry_draw_select_p2_chara, (app.entry_current_pos_x-app.width)-15, 0)
    drawLabel('2 PLAYERS', p2_location, (app.height/2)-50, align='center', font='DFPKanTeiRyu-XB', fill='black', size=60, border='black', borderWidth=10)
    drawLabel('2 PLAYERS', p2_location, (app.height/2)-50, align='center', font='DFPKanTeiRyu-XB', fill='white', size=60, border=rgb(80, 67, 155), borderWidth=4)
    drawLabel(f'Play with another', p2_location, (app.height/2)+25, align='center', font='FOT-Seurat Pro', size=20, bold=True)
    drawLabel(f'person together!', p2_location, (app.height/2)+50, align='center', font='FOT-Seurat Pro', size=20, bold=True)

    cpu_location = app.entry_current_pos_x+(app.width + (app.width/2)) + 35
    drawImage(app.entry_draw_select_cpu, cpu_location, app.height/2, align='center')
    drawLabel('AI BATTLE', cpu_location, (app.height/2)-50, align='center', font='DFPKanTeiRyu-XB', fill='black', size=60, border='black', borderWidth=10)
    drawLabel('AI BATTLE', cpu_location, (app.height/2)-50, align='center', font='DFPKanTeiRyu-XB', fill='white', size=60, border=rgb(56, 155, 140), borderWidth=4)
    drawLabel(f'Battle against a CPU', cpu_location, (app.height/2)+25, align='center', font='FOT-Seurat Pro', size=20, bold=True)
    drawLabel(f'of varying difficulties!', cpu_location, (app.height/2)+50, align='center', font='FOT-Seurat Pro', size=20, bold=True)
    drawImage(app.entry_draw_select_cpu_chara, app.entry_current_pos_x+app.width + 35, 0)

    fps_counter(app)

def entry_onKeyPress(app, key):
    if key == 'left':
        app.sfx_kat.play()
        if app.entry_current_pos_x != 1300:
            app.entry_select_mode = False
            app.entry_mode_movement = 30
    elif key == 'right':
        app.sfx_kat.play()
        if app.entry_current_pos_x != -1310:
            app.entry_select_mode = False
            app.entry_mode_movement = -30
    if key == 'enter':
        if app.entry_current_pos_x == 10:
            app.players = 1
            app.ai_battle = False
            setActiveScreen('song_select')
            onScreenSwitch_song_select(app)
        elif app.entry_current_pos_x == 1300:
            app.players = 2
            app.ai_battle = False
            setActiveScreen('song_select')
            onScreenSwitch_song_select(app)
        elif app.entry_current_pos_x == -1310:
            app.ai_battle = True
            app.players = 2
            setActiveScreen('song_select')
            onScreenSwitch_song_select(app)
    switchScreen(app, key)
