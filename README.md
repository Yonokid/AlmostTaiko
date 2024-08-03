AlmostTaiko: A CMU 15-112 Project

This project aims to recreate the arcade game "Taiko no Tatsujin" within CMU graphics. There are 3 modes: 1 Player, 2 Players, and AI battle mode.
To execute, run main.py. These libraries must be installed:

simpleaudio: https://pypi.org/project/simpleaudio/
cmu_graphics

There are a few shortcut commands that can be used:
"1": Switch to entry screen
"2": Switch to song select screen
"3": switch to main game screen
"4": switch to result screen
I would not suggest using these as they may break the game, but they may work for some use cases.

Left and right keys will switch the mode in the entry screen.
Hitting 'A' during the game will turn on autoplay for player 1.
Hitting 'Z' during the game will turn on autoplay for player 2.
Hitting 'escape' during the game will go back to song select.
Hitting 'escape' during difficulty select will go back to song select.

Keybinds for player 1:
E, F, J, I, in order of left to right on the drum
Keybinds for player 2:
D, C, M, K, in order of left to right on the drum
If any menus do not work with these keybinds, use left, right and enter to navigate. Escape can be used to move back a menu
Judgement offset can be modified in game.py, self.judge_offset, provided your speakers have added latency.


To load songs, they can be downloaded on the internet, preferrably from my website https://tjadataba.se.
Audio must be converted from ogg to wav! This simulator can only load wav files! The .tja WAVE: attribute must also end with .wav.
Demo songs are provided.

These fonts must also be installed:
https://drive.google.com/file/d/1OKbd2f4lGFwLkkp3wiENsybwc6VvLc6r/view
https://drive.google.com/file/d/1Au8BzkPLCIunt-GypA4qvkUtpwGnKisp/view
TTF files are also included.

Credits:
All images and sounds created by BANDAI NAMCO ENTERTAINMENT

Hope this doesn't get taken down LOL
