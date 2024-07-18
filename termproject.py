from cmu_graphics import *
import simpleaudio as sa
import time

def get_current_ms():
    return rounded(time.time() * 1000)

def onAppStart(app):
    app.test_tja1 = ['1',
                    '0011',
                    '12000000',
                    '00000110',
                    '000000000000000000000000000000000000000000100000',
                    '0000002220101010',
                    '00210021',
                    '0011102000201000',
                    '1000201110200022',
                    '1020002210201020',
                    '1000201110200022',
                    '1020002210201022',
                    '1000201110200022',
                    '1022202210201022',
                    '2002202000200020',
                    '0020002000111000',
                    '11211122',
                    '12212121',
                    '11211212',
                    '12212210',
                    '11211122',
                    '12212121',
                    '1022201020201020',
                    '12212210',
                    '1000200210102010',
                    '0010201210102000',
                    '1110200210102010',
                    '0010201210102212',
                    '1000200210102010',
                    '0010201210102000',
                    '1110201110201110',
                    '1020101120100000',
                    '20022002',
                    '20220000',
                    '20022002',
                    '20220000',
                    '20022002',
                    '20220000',
                    '20022002',
                    '20220011',
                    '1000102210001022',
                    '1022101010222000',
                    '1011102210111022',
                    '1022101010201111',
                    '1011102211111022',
                    '1122101110201111',
                    '0',
                    '0',
                    '021',
                    '0',
                    '1000100020100022',
                    '1000221000221000',
                    '21021021',
                    '000000200000100000000000',
                    '000000000000000000000000',
                    '1000201000201022',
                    '2210101010102022',
                    '1022221022221022',
                    '2210222212221222',
                    '00020010',
                    '1000221000221000',
                    '21021021',
                    '0020100210102022',
                    '1020222210121010',
                    '1020002010201022',
                    '1000102012221222',
                    '1222122212221222',
                    '1000200210102010',
                    '0210201212102010',
                    '1110201210102012',
                    '1010102212102000',
                    '1000200210102010',
                    '0010201212102022',
                    '1022221022221022',
                    '2210222210102000',
                    '1002201020102110',
                    '2010200210102000',
                    '1110201210102010',
                    '0010220212102022',
                    '1022221222221222',
                    '2212222212221111',
                    '1012221012221011',
                    '1210111210102000',
                    '1001101020002010',
                    '1110101020002020',
                    '1001101020002010',
                    '1122101020101010',
                    '1001101020002010',
                    '1110101020002020',
                    '1001101020002010',
                    '1122102000102000',
                    '1002102010221020',
                    '1022102010221022',
                    '1022122210221222',
                    '1022122212221222',
                    '1111221122112212',
                    '1111221122112222',
                    '20022002',
                    '20220000',
                    '0']
    app.test_tja1 = ['10010010',
                    '0',
                    '10010010',
                    '0',
                    '10010010',
                    '0',
                    '10010010',
                    '1',
                    '10101011',
                    '1000100010111010',
                    '10101011',
                    '00000120',
                    '1000100010111010',
                    '1111',
                    '000000000000000000000000000000000000000000000000',
                    '0002',
                    '1000100010001011',
                    '10101222',
                    '10101011',
                    '1112',
                    '1011100010001000',
                    '1000100011102020',
                    '11101010',
                    '1002',
                    '1000100010001011',
                    '10101222',
                    '10101011',
                    '1022',
                    '1011100010001000',
                    '1000100011102020',
                    '1000101110101000',
                    '0000',
                    '10200222',
                    '10200222',
                    '10200222',
                    '000000000000000000000000000000100000200000000000',
                    '10200222',
                    '10200222',
                    '10200222',
                    '000000000000000000000000000000000000000000000000',
                    '1000001110010010',
                    '11100000',
                    '1000001110010010',
                    '11101020',
                    '0',
                    '0',
                    '0',
                    '0',
                    '1011100010001000',
                    '1000100010111010',
                    '10101111',
                    '2221',
                    '1011100010001000',
                    '1000100010111010',
                    '1000100010111010',
                    '2212',
                    '10211020',
                    '1000200011102000',
                    '1010200011102020',
                    '000000000000000000000000000000000000000000000000',
                    '00000000',
                    '0',
                    '12',
                    '0120',
                    '12',
                    '0120',
                    '12',
                    '0120',
                    '12',
                    '2222',
                    '10200120',
                    '10202120',
                    '10200120',
                    '10202120',
                    '10200120',
                    '10202120',
                    '10200120',
                    '11012000',
                    '22222022',
                    '22200000',
                    '22222022',
                    '22222000',
                    '22222022',
                    '22200000',
                    '20222020',
                    '20222220',
                    '12222022',
                    '22200000',
                    '12222022',
                    '22222000',
                    '10222020',
                    '10222220',
                    '10221020',
                    '1',
                    '0',
                    '0',
                    '0',
                    '0',
                    '10101011',
                    '10101111',
                    '600000000000000000000000000000000000000000000000',
                    '0',
                    '1011101010001000',
                    '1010101010001011',
                    '11101011',
                    '0000',
                    '11201020',
                    '11221022',
                    '10221122',
                    '10222020',
                    '11201020',
                    '11221022',
                    '10221122',
                    '1011100010002000',
                    '12222022',
                    '22200020',
                    '20222020',
                    '20222210',
                    '10221020',
                    '10221122',
                    '1000100011102020',
                    '00000000']
    app.test_tja = ['10010010',
                    '0',
                    '10010010',
                    '0',
                    '10010010',
                    '0',
                    '10010010',
                    '1002',
                    '1020102011201020',
                    '1020102011221010',
                    '1020102011201020',
                    '00000120',
                    '1020102010211010',
                    '1022102010211020',
                    '1111111122222222',
                    '1002',
                    '1020102010201011',
                    '1020102011202020',
                    '1120102010201012',
                    '1112',
                    '1011102010201020',
                    '1022102011211020',
                    '1012102012201020',
                    '1120200010002000',
                    '1020102010201011',
                    '1020102011202020',
                    '1120102010201012',
                    '1000101120002000',
                    '1011102010201020',
                    '1022102011201011',
                    '1022102211112222',
                    '100200200200200020002000000000000000200000000000',
                    '1000222000102220',
                    '1000222000102220',
                    '1000222000102220',
                    '1000222010102000',
                    '1000222000102220',
                    '1000222000102220',
                    '1000222000102220',
                    '000000000000000000000000000000000000200000000000',
                    '1000001110010011',
                    '1111100010111110',
                    '1000001110010011',
                    '1111100010112000',
                    '1110112011101120',
                    '1110112011101120',
                    '1122112211221122',
                    '100000000000100000000000000000000000200000000000',
                    '1011101010001000',
                    '100100100100100111100111',
                    '1010100010111010',
                    '22122010',
                    '1011102010201020',
                    '100200100200100111100111',
                    '1020102010111010',
                    '222200200000100000200000',
                    '1110221011102220',
                    '1110222011212120',
                    '1111221121121121',
                    '000000000000000000000000000000000000000000000000',
                    '00000000',
                    '0',
                    '10002001',
                    '02102002',
                    '10002001',
                    '000200100000200000000000',
                    '10002001',
                    '02102002',
                    '10002001',
                    '20102120',
                    '10200120',
                    '10202122',
                    '10200120',
                    '10202120',
                    '10200120',
                    '10202122',
                    '10200120',
                    '11012000',
                    '2220202020002220',
                    '2020202210202020',
                    '2220202020002220',
                    '22222010',
                    '2220102020002220',
                    '2020102220202020',
                    '2000122020002000',
                    '2000122020202020',
                    '1220202010002220',
                    '1020202210202020',
                    '1220202010002220',
                    '12221020',
                    '1020222010201020',
                    '1020222010201012',
                    '1020101210201212',
                    '1002',
                    '1110112011101120',
                    '1110112011101120',
                    '1122112211221122',
                    '00000120',
                    '1000100010001011',
                    '10101122',
                    '1010101011111111',
                    '2000100020112000',
                    '100000100100100000100000101010100000101010100000',
                    '100000100000100000100000101010100000100000100100',
                    '100100111100111100100100',
                    '2020002000212000',
                    '100000100200100000200000101010100000100000200000',
                    '100000200000100000200000101010100000100200100100',
                    '100200100222100200100200',
                    '111100100100200000111100',
                    '100000100200100000200000101010100000100000200000',
                    '100000200000100000200000101010100000100000100100',
                    '111100100222100200200200',
                    '100000100100100000000000101010100000100000000000',
                    '2220102020001220',
                    '2020102220201020',
                    '2000122020001000',
                    '2000122020102000',
                    '100010100200100010102020',
                    '1020112010201120',
                    '100000001000100020002000100100100100200200200200',
                    '100200200200200020002000200000200000000000000000',
                    '0']
    
    #app.wave_obj = sa.WaveObject.from_wave_file("IssoKonoMamaDe.wav")
    app.wave_obj = sa.WaveObject.from_wave_file("SUPERNOVA.wav")
    app.bpm = 212
    
    app.stepsPerSecond = 60
    app.time_signature = 4
    app.scroll = 1
    app.offset = 50
    app.judge_offset = -50
    app.note_position = []
    app.bar_position = []
    
    app.p1_circleX, app.p1_circleY = app.width/3.11, app.height/2.8
    app.p1_gray_bgX, app.p1_gray_bgY = 0, app.height/3.9
    app.curr_note_position = app.width
    
    app.red_L = False
    app.red_R = False
    app.blue_L = False
    app.blue_R = False
    
    app.good = False
    app.ok = False
    app.bad = False
    
    app.start_game = False
    app.autoplay = False
    app.start_ms = 0
    app.combo = 0
    app.combo_size = 40
    app.frame = 0
    beat_duration = app.stepsPerSecond / app.bpm
    print(beat_duration)
    total_time = app.time_signature * beat_duration
    print(total_time)
    total_frames = app.stepsPerSecond * total_time
    print(total_frames)
    app.distance = app.width - (app.p1_circleX)
    print(app.distance)
    app.pixels_per_frame = (app.distance / total_frames) * (app.stepsPerSecond/60)
    print(app.pixels_per_frame)
    
def draw_p1_bg(app):
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY, app.width, app.p1_gray_bgY/1.05, fill=rgb(41,39,40))
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY+((app.p1_gray_bgY/5)*4), app.width, app.p1_gray_bgY/5, fill=rgb(133,131,132), border='black', borderWidth=8)

def draw_bar(app, player, bar, position):
    if position > app.width or position < app.p1_circleX-60:
        return
    if player == 1:
        drawLine(position, app.p1_gray_bgY, position, app.p1_gray_bgY+((app.p1_gray_bgY/5)*4), fill=rgb(133,131,132), lineWidth=3)
        
def draw_note(app, player, note, position):
    if position > app.width:
        return
    if player == 1:
        if note == '1' or note == '3':
            note_color = rgb(224,56,39)
            name = 'Do'
        elif note == '2' or note == '4':
            note_color = rgb(78,210,193)
            name = 'Ka'
        else:
            return
        drawCircle(position, app.p1_circleY, 35, fill=note_color, border='white', borderWidth=5) 
        #drawCircle(position, app.p1_circleY, 37, fill=None, border='black', borderWidth=2) 
        drawLabel(name, position, app.p1_circleY+93, fill='white', border='black', size=20, borderWidth=1.5, bold=True)

def draw_judgments(app):
    if app.good: drawLabel('GOOD', app.p1_circleX, app.p1_circleY-100, size=30, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black')
    elif app.ok: drawLabel('OK', app.p1_circleX, app.p1_circleY-100, size=30, fill='white', bold=True, border='black')
    elif app.bad: drawLabel('BAD', app.p1_circleX, app.p1_circleY-100, size=30, fill=gradient('deepSkyBlue','royalBlue','indigo', start='bottom'), bold=True, border='black')
    elif app.autoplay: drawLabel('AUTO', app.p1_circleX, app.p1_circleY-100, size=30, fill='white', bold=True, border='black')
    
def draw_judge_circle(app):
    drawCircle(app.p1_circleX, app.p1_circleY, 25, fill=rgb(42, 42, 40))
    drawCircle(app.p1_circleX, app.p1_circleY, 35, fill=None, border=rgb(91,91,91), borderWidth=4)
    drawCircle(app.p1_circleX, app.p1_circleY, 50, fill=None, border=rgb(56,56,56))

def draw_drum(app):
    offset_from_judge = -120
    drawRect(0, app.p1_gray_bgY, app.p1_circleX-60, app.p1_gray_bgY, fill=gradient(rgb(240,148,118), rgb(205,15,15), start='bottom'), border='black', borderWidth=8)
    drawOval(app.p1_circleX+offset_from_judge, app.p1_circleY+10, 80, 100, fill=rgb(115,32,15))
    drawCircle(app.p1_circleX+offset_from_judge, app.p1_circleY, 40, fill='beige')
    drawRect(app.p1_gray_bgX, app.p1_gray_bgY, app.width, app.p1_gray_bgY, fill=None, border='black', borderWidth=8)
    if app.blue_L:
        drawArc(app.p1_circleX+offset_from_judge, app.p1_circleY, 80, 80, 90, 180, fill=None, border=rgb(78,210,193), borderWidth=10)
        drawCircle(app.p1_circleX+offset_from_judge, app.p1_circleY, 30, fill='beige')
    if app.blue_R:
        drawArc(app.p1_circleX+offset_from_judge, app.p1_circleY, 80, 80, -90, 180, fill=None, border=rgb(78,210,193), borderWidth=10)
        drawCircle(app.p1_circleX+offset_from_judge, app.p1_circleY, 30, fill='beige')
    if app.red_L:
        drawArc(app.p1_circleX+offset_from_judge, app.p1_circleY, 60, 60, 90, 180, fill=rgb(224,56,39))
    if app.red_R:
        drawArc(app.p1_circleX+offset_from_judge, app.p1_circleY, 60, 60, -90, 180, fill=rgb(224,56,39))
    if 10 <= app.combo < 50:
        #drawLabel(app.combo, app.p1_circleX+offset_from_judge, app.p1_circleY, size=40, fill=gradient('red', 'orange', 'yellow', start='bottom'), bold=True, border='black')
        drawLabel(app.combo, app.p1_circleX+offset_from_judge, app.p1_circleY, size=app.combo_size, fill='white', bold=True, border='black')
    elif 50 <= app.combo < 100:
        drawLabel(app.combo, app.p1_circleX+offset_from_judge, app.p1_circleY, size=app.combo_size, fill=gradient(rgb(167, 173, 187), rgb(170,188,210), start='bottom'), bold=True, border='black')
    elif 100 <= app.combo:
        drawLabel(app.combo, app.p1_circleX+offset_from_judge, app.p1_circleY, size=app.combo_size, fill=gradient(rgb(235, 198, 143), rgb(243,171,76), start='bottom'), bold=True, border='black')
    
def redrawAll(app):
    ms = get_current_ms() - app.start_ms
    draw_p1_bg(app)
    draw_judge_circle(app)
    if app.bar_position != []:
        for bar, position, bar_ms in app.bar_position:
            position = app.width + app.pixels_per_frame * app.stepsPerSecond / 1000 * (bar_ms - ms)
            draw_bar(app, 1, bar, position+app.offset)
    if app.note_position != []:
        for note, position, note_ms in app.note_position:
            position = app.width + app.pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - ms)
            draw_note(app, 1, note, position+app.offset)   
    draw_drum(app)
    draw_judgments(app)

def tja_parse(app, tja):
    position = 0
    current_ms = 0
    app.note_position = []
    app.bar_position = []
    bars = len(tja)
    for i in range(bars):
        bar_ms = current_ms
        print(f'Bar: {i}, {position}')
        app.bar_position.append((i, position, bar_ms))
        bar = tja[i]
        mspermeasure = 60000 * app.time_signature / app.bpm
        # if len(bar) == 0:
        #     current_ms += mspermeasure
        # else:
        increment = mspermeasure / len(bar)
        for note in bar:
            note_ms = current_ms # store note ms along with ms
            #print(f'Note: {note}, {position}, {note_ms}')
            app.note_position.append((note, position, note_ms))
            position += 1 / len(bar) * app.bpm * app.time_signature
            current_ms += increment

def check_note(app, note_type):
    if note_type == '0':
        return
    while app.note_position:
        note, position, note_ms = app.note_position[0]
        ms = get_current_ms() - app.start_ms
        position = app.width + app.pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - ms)
        if note != note_type:
            return
        if position > app.p1_circleX+100:
            break
        if app.p1_circleX-25 + app.judge_offset <= position <= app.p1_circleX+25 + app.judge_offset:
            app.combo += 1
            app.combo_size = 50
            app.good = True
            app.note_position.pop(0)
            break
        if app.p1_circleX-50 + app.judge_offset <= position <= app.p1_circleX+50 + app.judge_offset:
            app.combo += 1
            app.combo_size = 50
            app.ok = True
            app.note_position.pop(0)
            break
        else:
            break
            

def onStep(app):
    ms = get_current_ms() - app.start_ms
    if app.autoplay:
        for i in range(1, 3):
            check_note(app, str(i))
            app.good = False
            app.ok = False
            app.bad = False
    if app.note_position:
        note, position, note_ms = app.note_position[0]
        if note != '0':
            position = app.width + app.pixels_per_frame * app.stepsPerSecond / 1000 * (note_ms - ms)
            if position < app.p1_circleX-50 + app.judge_offset:
                app.note_position.pop(0)
                app.combo = 0
                app.bad = True
        else:
            app.note_position.pop(0)
    if app.frame % 3 == 0:
        app.combo_size = 40
    app.frame += 1
    
def onKeyPress(app, key):
    if key == 'p':
        tja_parse(app, app.test_tja)
        app.start_game = True
        app.start_ms = get_current_ms()
        app.wave_obj.play()
    if key == 'm':
        sa.stop_all()
    if key == 'f':
        app.red_L = True
        check_note(app, '1')
    if key == 'j':
        app.red_R = True
        check_note(app, '1')
    if key == 'e':
        app.blue_L = True
        check_note(app, '2')
    if key == 'i':
        app.blue_R = True
        check_note(app, '2')
    if key == 'a':
        app.autoplay = not app.autoplay

def onKeyRelease(app, key):
    if key == 'f' or key == 'j':
        app.red_L = False
        app.red_R = False
    elif key == 'e' or key == 'i':
        app.blue_L = False
        app.blue_R = False
    app.good = False
    app.ok = False
    app.bad = False
    
def main():
    runApp(width=1280, height=720)
    
main()