import pyaudio
import speech_recognition as sr

r=sr.Recognizer()
r.energy_threshold = 4000  #Начальный уровень шума
r.dynamic_energy_threshold = True  #Динамический уровень шума
print("Скажите что-нибудь...")
with sr.Microphone() as source:
   audio=r.listen(source)

try:
   print("Вы сказали:" + r.recognize_google(audio, language = "ru-RU"))
except LookupError:
   print('Речь не распознана!')