import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# import requests

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

# настройки
opts = {
    "alias": ('данко', 'привет данко', 'здравствуй данко'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час', 'время', 'сейчас время', 'кремлёвское время'),
        "radio": ('похороны', 'король и шут', 'включи похороны панка'),
        "milos": ('рикардо', 'рикардо милос', 'рикардо милоса', 'включи рикардо'),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}


def callback(recognizer, audio):
    try:

        voices = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voices)

        if voices.startswith(opts["alias"]):
            # обращаются к Данко
            cmd = voices

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    def speak(wait):
        print(wait)
        speak_engine.say(wait)
        speak_engine.runAndWait()
        speak_engine.stop()

    speak_engine = pyttsx3.init()
    voices = speak_engine.getProperty('voices')
    speak_engine.setProperty('rate', 130)
    speak_engine.setProperty('voices', voices[0].id)

    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("E:\\AH\\Музыка\\PohoroniPanka.mp3")

    elif cmd == "milos":
        # воспроизвести РИКАРДО
        os.system("E:\\AH\\Видео\\Halogen.mp4")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

    else:
        print('Команда не распознана, повторите!')


stop_listening = r.listen_in_background(m, callback)

while True: time.sleep(0.1)  # infinity loop