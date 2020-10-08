import speech_recognition as sr
import pyaudio

# Test rozpoznawania mowy z pliku wav
# r = sr.Recognizer()
# harvard = sr.AudioFile('harvard.wav')
# with harvard as source:
#     audio = r.record(source)
#
# print(r.recognize_google(audio))

# Test rozpoznawania mowy rejestrowanej przez mikrofon
# Na windowsie - pip install pipwin, pipwin install pyaudio
r = sr.Recognizer()
mic = sr.Microphone()
# with mic as source:
#     r.adjust_for_ambient_noise(source, duration=1)
#     audio = r.listen(source)

# v = r.recognize_google(audio)
# print(v)

# Test udany

hello = sr.AudioFile('harvard.wav')
with hello as source1:
    audio1 = r.record(source1)
u = r.recognize_google(audio1)
print(u)

if __name__ == '__main__':
    print('PyCharm')

