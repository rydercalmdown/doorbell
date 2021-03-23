import os
import subprocess
import random
import time
import RPi.GPIO as GPIO


AUDIO_DIRECTORY = '/home/pi/doorbell/audio'
PIN_NUMBER = 12


def get_audio_clips():
    """Returns paths to all available audio clips"""
    list_of_clips = []
    for file in os.listdir(AUDIO_DIRECTORY):
        if file.endswith('.mp3'):
            list_of_clips.append(os.path.join(AUDIO_DIRECTORY, file))
    return list_of_clips


def play_clip():
    clips = get_audio_clips()
    if not clips:
        print('No audio clips available')
        exit(1)
    random_clip = random.choice(clips)
    print('playing clip {}'.format(random_clip))
    subprocess.call(['mpg321', random_clip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def listen_for_gpio_change():
    """Continuously listens for state change of GPIO"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        while True:
            pin_current = GPIO.input(PIN_NUMBER)
            if pin_current == 1:
                play_clip()
            else:
                play_clip()
            while GPIO.input(PIN_NUMBER) == pin_current:
                # waits until the state changes
                time.sleep(0.5)
    except KeyboardInterrupt:
	    GPIO.cleanup()


if __name__ == '__main__':
    listen_for_gpio_change()
