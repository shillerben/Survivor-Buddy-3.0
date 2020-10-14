import vlc
import time

player = vlc.MediaPlayer("./cdr-presentation.mp4")
player.play()
time.sleep(10)