from tkinter import *
import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import speech_recognition as sr
import sys
import re
import webbrowser

root = Tk()
root.title('Lora')
root.geometry('400x700')
root.resizable(False, False)
canvas = Canvas(root, width='400', height='700', bg='#a0d6b4')
def Lora(vkl):
    while(vkl==True):

        # import requests

        r = sr.Recognizer()
        m = sr.Microphone(device_index=1)

        with m as source:
            r.adjust_for_ambient_noise(source)

        # настройки
        opts = {
            "alias": ('лора', 'привет лора', 'здравствуй лора', 'лара', 'лаура'),
            "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
            "cmds": {
                "ctime": ('текущее время', 'сейчас времени', 'который час', 'время', 'сейчас время', 'кремлёвское время'),
                "music": ('похороны', 'король и шут', 'включи похороны панка'),
                "milos": ('рикардо', 'рикардо милос', 'рикардо милоса', 'включи рикардо', 'включи рикардо милоса'),
                "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
                "desk": ('открой программу', 'рабочий стол'),
                "web": ('открой браузер', 'сайт', 'открой сайт', 'нужен сайт', 'зайди на сайт', 'найди')
            }
        }

        def callback(recognizer, audio):
            try:

                voices = recognizer.recognize_google(audio, language="ru-RU").lower()
                print("[log] Распознано: " + voices)

                if voices.startswith(opts["alias"]):
                    # обращаются к Лоре
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

            if cmd == 'ctime':
                # сказать текущее время
                now = datetime.datetime.now()
                speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

            elif cmd == 'music':
                # воспроизвести музыку
                link = os.path.abspath("Music\PohoroniPanka.mp3")
                os.system(link)

            elif cmd == "milos":
                # воспроизвести РИКАРДО
                link = os.path.abspath("Video\Halogen.mp4")
                os.system(link)

            # elif cmd == 'desk':
            # открыть с рабочего стола
            # link = os.path.abspath("Desktop\Для курсача.txt")
            # print(link)

            elif cmd == "web":
                k = sr.Recognizer()
                l = sr.Microphone(device_index=1)
                with l as source:
                    k.adjust_for_ambient_noise(source)
                    speak("Просто скажите адрес или поисковый запрос: ")
                    audio = k.listen(source)
                domain = k.recognize_google(audio, language="ru-RU").lower()
                print("[log] Распознано: " + domain)
                print(domain)
                if re.search(r'\.', domain):
                    webbrowser.open_new_tab('https://' + domain)
                elif re.search(r'\ ', domain):
                    webbrowser.open_new_tab('https://yandex.ru/search/?text=' + domain)
                else:
                    webbrowser.open_new_tab('https://yandex.ru/search/?text=' + domain)
                speak('Сайт открывается...')


            elif cmd == 'stupid1':
                # рассказать анекдот
                speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

            else:
                print('Команда не распознана, повторите!')

        stop_listening = r.listen_in_background(m, callback)

        while True: time.sleep(0.1)  # infinity loop
        label_n = Label(root, text='Ваш голосовой ассистент - Лора, запущен. Для начала работы обратитесь к ней, а потом скажите что ей выполнить')
        label_n.place(x=0, y=550)

btn_zp = Button(root, text='Запустить', width=25,height=5)
btn_zp.bind('<Button 1>', lambda event:Lora(vkl=True))
btn_zp.place(x=100, y=600)

root.mainloop()