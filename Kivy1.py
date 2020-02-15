from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter.ttk import Combobox
import os
import time
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import speech_recognition as sr
import re
import webbrowser
import random



def spravka():
    spr = Tk()
    spr.title('Справка')
    spr.geometry('1000x500')
    spr.resizable(False, False)
    text = Text(spr, width=120, height=30, wrap=WORD)
    text.pack(side=LEFT, padx=5, pady=5)
    scrolly = Scrollbar(spr, orient=VERTICAL, command=text.yview)
    scrolly.pack(side=RIGHT, fill=Y)
    text.config(state='normal', yscrollcommand=scrolly.set)
    parent_dir = os.path.dirname('SpravkaLora.txt')
    f = open(os.path.join(parent_dir, 'SpravkaLora.txt'))
    s = f.read()
    text.insert(1.0, s)
    f.close()
    text.config(state='disabled', yscrollcommand=scrolly.set)
    spr.mainloop()

def clear():
    ltext.config(state='normal')
    ltext.delete(1.0, END)  # мы передали координаты очистки
    ltext.config(state='disabled')

searcher = 'Яндекс'

def settihgs():

    def submit():
        global searcher
        searcher = searchers.get()
        sets.destroy()


    sets = Tk()
    sets.title('Настройки')
    sets.geometry('500x450')
    sets.resizable(False, False)

    set1 = Label(sets, text='Тема: ')
    set1.grid(column=0, row=0, padx=5, pady=5, sticky=W)

    theme = Combobox(sets, state='readonly')
    theme['values'] = ('Light', 'Dark')
    theme.current(0)  # установите вариант по умолчанию
    theme.grid(column=1, row=0)

    set2 = Label(sets, text='Поисковые сервисы: ')
    set2.grid(column=0, row=1, padx=5, pady=10)

    searchers = Combobox(sets, state='readonly')
    searchers['values'] = ('Яндекс', 'Google', 'Mail.ru', 'Bing')
    searchers.current(0)  # установите вариант по умолчанию
    searchers.grid(column=1, row=1)

    btn_sub = Button(sets, text="Применить", command=submit)
    btn_sub.grid(column=1, row=2)

    sets.mainloop()

def Lora():

    #включение микрофона
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)

    with m as source:
        r.adjust_for_ambient_noise(source)

    def log(logg):
        ltext.config(state='normal')
        ltext.insert(tk.INSERT, '\n{}\n'.format(logg))
        ltext.config(state='disabled')

    speak_engine = pyttsx3.init()

    def speak(wait):
        log(wait)
        speak_engine.say(wait)
        speak_engine.runAndWait()
        speak_engine.stop()

    speak('Слушаю Вас!')

    # настройки
    opts = {
        'alias': ('лора', 'привет лора', 'здравствуй лора', 'лара', 'лаура', 'лорак', 'лор', 'lori','lora','',' '),
        'tbr': ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'включи'),
        'cmds': {
            'ctime': ('текущее время', 'сейчас времени', 'который час', 'время', 'сейчас время', 'часы'),
            'music': ('музыка', 'музыку'),
            'milos': ('видео', 'запусти видео'),
            'web': ('открой браузер', 'сайт', 'открой сайт', 'нужен сайт', 'зайди на сайт', 'найди'),
            'stopLora':('спокойной ночи', 'пока', 'заверши работу', 'прощай', 'выключись', 'заверши работу', 'заверши свою работу', 'отдыхай'),
            'anekdot': ('расскажи анектдот', 'анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
            }
        }

    def callback(recognizer, audio):
        try:
            voices = recognizer.recognize_google(audio, language='ru-RU').lower()
            log1 = 'Распознано: {}'.format(voices)
            log(log1)

            if voices.startswith(opts['alias']):
                # обращаются к Лоре
                cmd = voices

                for x in opts['alias']:
                    cmd = cmd.replace(x, '').strip()

                for x in opts['tbr']:
                    cmd = cmd.replace(x, '').strip()

                # распознаем и выполняем команду
                cmd = recognize_cmd(cmd)
                execute_cmd(cmd['cmd'])

        except sr.UnknownValueError:
            log2 = '\nГолос не распознан!\n'
            log(log2)
        except sr.RequestError as e:
            log3 = 'Неизвестная ошибка, проверьте интернет!'
            log(log3)

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

        def vizov(sp):
            k = sr.Recognizer()
            l = sr.Microphone(device_index=1)
            with l as source:
                k.adjust_for_ambient_noise(source)
                speak(sp)
                audio = k.listen(source)
            global namerec
            namerec = k.recognize_google(audio, language='ru-RU').lower()
            log2 = 'Распознано: {}'.format(namerec)
            log(log2)

        global searcher

        if cmd == 'ctime':
            # сказать текущее время
            now = datetime.datetime.now()
            speak('Сейчас ' + str(now.hour) + ':' + str(now.minute))

        elif cmd == 'music':
            # воспроизвести музыку
            vizov('Скажите название композиции:')
            try:
                os.startfile('LoraMusic\\'+namerec+'.mp3')
            except FileNotFoundError:
                speak('Композиция не найдена')

        elif cmd == 'milos':
            # воспроизвести РИКАРДО
            vizov('Скажите название видео:')
            try:
                os.startfile('LoraVideo\\'+namerec+'.mp4')
            except FileNotFoundError:
                speak('Видео не найдено')

        elif cmd == 'web':
            vizov('Просто скажите адрес или поисковый запрос: ')
            if re.search(r'\.', namerec):
                webbrowser.open_new_tab('https://' + namerec)
            elif re.search(r'\ ', namerec):
                if searcher == 'Яндекс':
                        webbrowser.open_new_tab('https://yandex.ru/search/?text=' + namerec)
                elif searcher == 'Google':
                    webbrowser.open_new_tab('https://www.google.ru/search?q=' + namerec)
                elif searcher == 'Mail.ru':
                    webbrowser.open_new_tab('https://go.mail.ru/search?q=' + namerec)
                elif searcher == 'Bing':
                    webbrowser.open_new_tab('https://www.bing.com/search?q=' + namerec)
            else:
                if searcher == 'Яндекс':
                    webbrowser.open_new_tab('https://yandex.ru/search/?text=' + namerec)
                elif searcher == 'Google':
                    webbrowser.open_new_tab('https://www.google.ru/search?q=' + namerec)
                elif searcher == 'Mail.ru':
                    webbrowser.open_new_tab('https://go.mail.ru/search?q=' + namerec)
                elif searcher == 'Bing':
                    webbrowser.open_new_tab('https://www.bing.com/search?q=' + namerec)
            speak('Сайт открывается...')


        elif cmd == 'anekdot':
            # рассказать анекдот
            an_list = ['И поехала она за ним в Сибирь. И испортила ему всю каторгу...',
                        'Лучшее средство от любви с первого взгляда - посмотреть второй раз.',
                        'Бесит, когда разговор с тобой начинают не с поклона.',
                        '— Интересно, какой изврат психики заставляет меня говорить голосовому помощнику \'спасибо\' и \'пожалуйста\'? Она же не настоящая!\n— Правильно делаешь. Когда Скайнет придет к власти, тебе, может, и зачтется…']
            speak(random.choice(an_list))

        elif cmd == 'stopLora':
            st_list = ['До встречи!', 'Спасибо за работу!', 'Удачи!', 'До свидания!', 'Вы лучший']
            speak(random.choice(st_list))
            stop_listening(wait_for_stop=False)
            log('Для продолжения нажмите кнопку запуска.')
        else:
            speak('Команда не распознана, пожалуйста повторите!')

    stop_listening = r.listen_in_background(m, callback)



root = Tk()
root.title('Lora')
root.geometry('400x700')
root.resizable(False, False)

#кнопка запуска
btn_zp = Button(root, text='Запустить', width=25,height=5,command=Lora)
btn_zp.pack()
btn_zp.place(x=100, y=600)

#Текстовый log
ltext = scrolledtext.ScrolledText(root, width=90, height=36, wrap=WORD)
ltext.pack(side=TOP, padx=5)
ltext.config(state='normal')
ltext.insert(tk.INSERT,'Ожидание запуска...\n')
ltext.config(state='disabled')

#меню
menu = Menu(root)
item = Menu(menu)
item = Menu(menu, tearoff=0)
item.add_command(label='Настройки', command=settihgs)
menu.add_cascade(label='Меню', menu=item)
menu.add_cascade(label='Очистка лога', command=clear)
menu.add_cascade(label='Справка', command=spravka)
root.config(menu=menu)

root.mainloop()
