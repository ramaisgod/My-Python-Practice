import time
import pygame
from pygame import mixer
# import os
# os.system("start baby_ko_bass.mp3")

# pygame.init()
# m = pygame.mixer.music('baby_ko_bass.mp3')
# pygame.mixer.music.play()
# pygame.event.wait()

mixer.init()
mixer.music.load('baby_ko_bass.mp3')
mixer.music.play()
time.sleep(10)
mixer.music.stop()


