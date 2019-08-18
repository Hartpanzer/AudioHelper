import pyaudio
import speech_recognition as sr

r=sr.Recognizer()
r.energy_threshold=4000

with sr.Microphone() as source:
   audio=r.listen(source)

try:
   print("Speech was:" + r.recognize_google(audio, language = "ru-RU"))
except LookupError:
   print('Speech not understood')