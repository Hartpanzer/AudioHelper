from tkinter import *
from tkinter import filedialog as fd
import tkinter as tk
import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import speech_recognition as sr
from tkinter import messagebox as mb
import sys
import re
import webbrowser
import random

root = Tk()
root.title('Lora')
root.geometry('400x700')
root.resizable(False, False)

#Текстовый log
global ltext
ltext = Text(root, width=90, height=30, wrap=WORD)
ltext.pack(side=LEFT, padx=5, pady=5)
scrolly = Scrollbar(root, orient=VERTICAL, command=ltext.yview)
scrolly.pack(side=RIGHT, fill=Y)
ltext.config(state='normal',yscrollcommand=scrolly.set)
ltext.insert(tk.INSERT,'Ожидание запуска...\n')
ltext.config(state='disabled',yscrollcommand=scrolly.set)

def spravka():
    spr = Tk()
    spr.title('Справка')
    spr.geometry('1000x500')
    spr.resizable(False, False)
    text = Text(spr, width=120, height=30, wrap=WORD)
    text.pack(side=LEFT, padx=5, pady=5)
    scrolly = Scrollbar(spr, orient=VERTICAL, command=text.yview)
    scrolly.pack(side=RIGHT, fill=Y)
    text.insert(tk.INSERT,'Для начала выполнения любой команды нужно обратиться к Лоре.\n')
    text.insert(tk.INSERT, 'Например: Лора; Привет, Лора; Здравствуй, Лора.\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\nУзнать сколько время:\n')
    text.insert(tk.INSERT, 'Команды: текущее время; сколько сейчас времени; который час; время; сейчас время; часы.\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\nПроиграть лучшую музыку на планете:\n')
    text.insert(tk.INSERT, 'Команды: включи музыку; музыка; похороны; король и шут; включи похороны панка.\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\nПроиграть лучшую музыку на планете:\n')
    text.insert(tk.INSERT, 'Команды: включи музыку; музыка; похороны; король и шут; включи похороны панка.\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\nВключить лучшее видео на планете:\n')
    text.insert(tk.INSERT, 'Команды: Включи видео, видео, рикардо; рикардо милос; рикардо милоса; включи рикардо; включи рикардо милоса.\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\nРабота с браузером:\n')
    text.insert(tk.INSERT, 'Команды: открой браузер; сайт; открой сайт; нужен сайт; зайди на сайт; найди.\n')
    text.insert(tk.INSERT, '    Примечание: После произнесения команды будет предоставлен выбор ввода адреса ссылки или поискового запроса.\n')
    text.insert(tk.INSERT, '    Для выбора адресса ссылки скажите адрес И ОБЯЗАТЕЛЬНО СЛОВО ТОЧКА И ДОМЕН. Например, произнесите: ВК ТОЧКА КОМ и вы будете перенаправлены на vk.com\n')
    text.insert(tk.INSERT, '    Для выбора поискового запроса скажите любое слово или словосочетание БЕЗ ТОЧКИ. Например, произнесите: купить автомобиль\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\n!ВРЕМЕННО НЕДОСТУПНО! Для открытия блокнота: !ВРЕМЕНО НЕДОСТУПНО!\n')
    text.insert(tk.INSERT, 'Команды: открой блокнот; блокнот; открой записную книжку; открой запись; открой текст; открой текстовый редактор.\n')
    text.insert(tk.INSERT, '________________________________________________________________________________________________________________________\n')
    text.insert(tk.INSERT, '\nАвтор: Потапов Сергей\n')
    text.insert(tk.INSERT, 'Для обратной связи: hartpanzer@gmail.com\n')

    text.config(state='disabled',yscrollcommand=scrolly.set)

def notepad():
    def op():
        file_name = fd.askopenfilename()
        f = open(file_name)
        s = f.read()
        textn.insert(1.0, s)
        f.close()

    def sv():
        file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                    ("HTML files", "*.html;*.htm"),
                                                    ("All files", "*.*")))

        f = open(file_name, 'w')
        s = textn.get(1.0, END)
        f.write(s)
        f.close()

    notep = Tk()
    notep.title('Блокнот')
    fr1 = Frame(notep)
    fr1.pack()
    notep.geometry('1000x800')
    notep.resizable(False, False)

    b1 = Button(fr1, width=10, height=1, text='Открыть', command=op)
    b1.pack(side=LEFT, padx=5, pady=5)

    b2 = Button(fr1, width=10, height=1, text='Сохранить', command=sv)
    b2.pack(side=LEFT, padx=5, pady=5)

    textn = Text(notep,width=120, height=50, wrap=WORD)
    textn.pack(side=LEFT, padx=5, pady=5)

    scrolly = Scrollbar(notep,orient=VERTICAL, command=textn.yview)
    scrolly.pack(side=RIGHT, fill=Y)

    textn.config(yscrollcommand=scrolly.set)

def stopLora():
    os.abort()

#функция принимает значение из кнопки

def Lora():

    #import requests
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)

    with m as source:
        r.adjust_for_ambient_noise(source)

    # настройки
    opts = {
        "alias": ('лора', 'привет лора', 'здравствуй лора', 'лара', 'лаура', 'лорак'),
        "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
        "cmds": {
            "ctime": ('текущее время', 'сейчас времени', 'который час', 'время', 'сейчас время', 'часы'),
            "music": ('включи музыку', 'музыка', 'музыку'),
            "milos": ('включи видео','видео', 'запусти видео'),
            "anekdot": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
            "web": ('открой браузер', 'сайт', 'открой сайт', 'нужен сайт', 'зайди на сайт', 'найди'),
            "stopLora":('спокойной ночи', 'пока', 'заверши работу', 'прощай', 'выключись', 'заверши работу', 'заверши свою работу', 'отдыхай'),
            "notepad": ('открой блокнот', 'блокнот', 'открой записную книжку', 'открой запись', 'открой текст', 'открой текстовый редактор')
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

        def vizov(sp):
            k = sr.Recognizer()
            l = sr.Microphone(device_index=1)
            with l as source:
                k.adjust_for_ambient_noise(source)
                speak(sp)
                audio = k.listen(source)
            global namerec
            namerec = k.recognize_google(audio, language="ru-RU").lower()
            print("[log] Распознано: " + namerec)


        if cmd == 'ctime':
            # сказать текущее время
            now = datetime.datetime.now()
            speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

        elif cmd == 'music':
            # воспроизвести музыку
            vizov('Скажите название композиции:')
            os.startfile("LoraMusic\\"+namerec+".mp3")

        elif cmd == "milos":
            # воспроизвести РИКАРДО
            vizov('Скажите название видео:')
            os.startfile("LoraVideo\\"+namerec+".mp4")

        elif cmd == "web":
            vizov('Просто скажите адрес или поисковый запрос: ')
            if re.search(r'\.', namerec):
                webbrowser.open_new_tab('https://' + namerec)
            elif re.search(r'\ ', namerec):
                webbrowser.open_new_tab('https://yandex.ru/search/?text=' + namerec)
            else:
                webbrowser.open_new_tab('https://yandex.ru/search/?text=' + namerec)
            speak('Сайт открывается...')


        elif cmd == 'anekdot':
            # рассказать анекдот
            an_list = ["И поехала она за ним в Сибирь. И испортила ему всю каторгу...",
                        "Лучшее средство от любви с первого взгляда - посмотреть второй раз.",
                        "Бесит, когда разговор с тобой начинают не с поклона.",
                        "— Интересно, какой изврат психики заставляет меня говорить голосовому помощнику \"спасибо\" и \"пожалуйста\"? Она же не настоящая!\n— Правильно делаешь. Когда Скайнет придет к власти, тебе, может, и зачтется…"]
            speak(random.choice(an_list))

        #elif cmd == 'notepad':
            #btn_bl.click
        elif cmd == 'stopLora':
            st_list = ["До встречи!", "Спасибо за работу!", "Удачи!", "До свидания!", "Вы лучший"]
            speak(random.choice(st_list))
            os.abort()
        else:
            print('Команда не распознана, повторите!')

    stop_listening = r.listen_in_background(m, callback)

    while True: time.sleep(0.1)  # infinity loop

#кнопка запуска
btn_zp = Button(root, text='Запустить', width=25,height=5,command=Lora)
btn_zp.pack()
btn_zp.place(x=100, y=600)

#кнопка справки
btn_help = Button(root, text='Справка', width=6,height=1,command=spravka)
btn_help.pack()
btn_help.place(x=0, y=0)

#кнопка блокнта
btn_bl = Button(root, text='Блокнот', width=6,height=1,command=notepad)
btn_bl.pack()
btn_bl.place(x=55, y=0)

#кнопка завершения
btn_st = Button(root, text='Завершить работу', width=15,height=1,command=stopLora)
btn_st.pack()
btn_st.place(x=250, y=0)

root.mainloop()