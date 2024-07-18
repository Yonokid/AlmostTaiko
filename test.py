test_tja = ['1111','1111','1111','11112222','1022202020111010','1111']
bpm = 190
note_position = []
bar_position = []

def parse(tja):
    position = 0
    note_position = []
    bar_position = []
    bars = len(tja)
    for i in range(bars):
        print(f'Bar: {i}, {position}')
        bar = tja[i]
        for note in bar:
            print(f'Note: {note}, {position}')
            position += 1 / len(bar)
       
parse(test_tja)