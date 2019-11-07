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

def spravka():
    spr = Tk()
    spr.title('Справка')
    spr.geometry('1000x500')
    spr.resizable(False, False)
    label_sp = Label(spr,text='Для начала выполнения любой команды нужно обратиться к Лоре.',font=('bold'))
    label_sp.grid(column=0,row=0, sticky=W)
    label_sp1 = Label(spr, text='Например: Лора; Привет, Лора; Здравствуй, Лора.')
    label_sp1.grid(column=0, row=1, sticky=W)
    label_sp2 = Label(spr,text='Узнать сколько время:',font=('bold'))
    label_sp2.grid(column=0,row=2, sticky=W)
    label_sp3 = Label(spr,text='Команды: текущее время; сколько сейчас времени; который час; время; сейчас время; кремлёвское время; часы.')
    label_sp3.grid(column=0, row=3, sticky=W)
    label_sp4 = Label(spr, text='Проиграть лучшую музыку на планете:', font=('bold'))
    label_sp4.grid(column=0, row=4, sticky=W)
    label_sp5 = Label(spr,text='Команды: похороны; король и шут; включи похороны панка.')
    label_sp5.grid(column=0, row=5, sticky=W)
    label_sp6 = Label(spr, text='Включить лучшее видео на планете:', font=('bold'))
    label_sp6.grid(column=0, row=6, sticky=W)
    label_sp7 = Label(spr, text='Команды: рикардо; рикардо милос; рикардо милоса; включи рикардо; включи рикардо милоса.')
    label_sp7.grid(column=0, row=7, sticky=W)
    label_sp8 = Label(spr, text='Работа с браузером', font=('bold'))
    label_sp8.grid(column=0, row=8, sticky=W)
    label_sp9 = Label(spr, text='Команды: открой браузер; сайт; открой сайт; нужен сайт; зайди на сайт; найди.')
    label_sp9.grid(column=0, row=9, sticky=W)
    label_sp10 = Label(spr, text='Примечание: После произнесения команды будет предоставлен выбор ввода адреса ссылки или поискового запроса.')
    label_sp10.grid(column=0, row=10, sticky=W)
    label_sp11 = Label(spr,text='Для выбора адресса ссылки скажите адрес И ОБЯЗАТЕЛЬНО СЛОВО ТОЧКА И ДОМЕН. Например, произнесите: ВК ТОЧКА КОМ и вы будете перенаправлены на vk.com')
    label_sp11.grid(column=0, row=11, sticky=W)
    label_sp12 = Label(spr,text='Для выбора поискового запроса скажите любое слово или словосочетание БЕЗ ТОЧКИ. Например, произнесите: купить автомобиль')
    label_sp12.grid(column=0, row=12, sticky=W)
    label_sp13 = Label(spr,text='Автор: Потапов Сергей', font=('bold'))
    label_sp13.grid(column=0, row=13, sticky=S)
    label_sp14 = Label(spr, text='Для обратной связи: hartpanzer@gmail.com', font=('bold'))
    label_sp14.grid(column=0, row=14, sticky=S)

#функция принимает значение из кнопки

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
                "ctime": ('текущее время', 'сейчас времени', 'который час', 'время', 'сейчас время', 'кремлёвское время', 'часы'),
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
    if vkl == True:
        label_n = Label(root, text='Ваш голосовой ассистент - Лора, запущен.')
        label_n.place(x=0, y=550)
    else:
        label_n = Label(root, text='Ожидание запуска...')
        label_n.place(x=0, y=550)
#кнопка запуска
btn_zp = Button(root, text='Запустить', width=25,height=5)
btn_zp.bind('<Button 1>', lambda event:Lora(vkl=True))
btn_zp.place(x=100, y=600)

#кнопка справки
btn_help = Button(root, text='Справка', width=6,height=1,command=spravka)
btn_help.pack()
btn_help.place(x=0, y=0)

root.mainloop()