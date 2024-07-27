from cmu_graphics import *

from entry import *
from song_select import *
from game import *
from result import *

def onAppStart(app):
    app.tja_folder_path = 'Songs'
    
def main():
    runAppWithScreens(initialScreen='entry', width=1280,height=720)
    
main()