# Exercise 7: Healthy Programmer by Harry

from pygame import mixer
from datetime import datetime
from time import time

def music_on_loop(file, stopper):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    while True:
        a = input()
        if a == stopper:
            mixer.music.stop()
            break

def log_now(msg):
    with open("mylog.txt", "a") as f:
        f.write(f"{msg} {datetime.now()}\n")

if __name__ == "__main__":
    init_water = time()
    init_eyes = time()
    init_exercise = time()
    water_interval = 5
    eyes_interval = 10
    exercise_interval = 20

    while True:
        if time() - init_water > water_interval:
            print("Water Drinking time. Enter 'drank' to stop the alarm. !!!")
            music_on_loop("alarm.mp3", "drank")
            init_water = time()
            log_now("Drank water at")

        if time() - init_eyes > eyes_interval:
            print("Eye Relax time. Enter 'eydone' to stop the alarm. !!!")
            music_on_loop("alarm.mp3", "eydone")
            init_eyes = time()
            log_now("Eye Relaxed at")

        if time() - init_exercise > exercise_interval:
            print("Physical Activity time. Enter 'exdone' to stop the alarm. !!!")
            music_on_loop("alarm.mp3", "exdone")
            init_exercise = time()
            log_now("Physical Exercise at")



