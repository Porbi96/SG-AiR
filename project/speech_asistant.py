import time
import webbrowser
import requests
from googlesearch import search
import speech_recognition as sr
import pyttsx3


def sa_speak(text: str):
    engine.say(text)
    engine.runAndWait()


def sa_listen(recogniser, microphone) -> str:

    with microphone as source:

        recogniser.adjust_for_ambient_noise(source, duration=2)
        # r.pause_threshold = 1
        sa_speak("Say something!")
        audio = recogniser.listen(source)

    try:
        query = recogniser.recognize_google(audio)
        print(f"User said:\n{query}\n")

    except Exception as e:
        print("Unable to recognize voice.")
        print(e)
        return ""

    return query.lower()





def sa_open_website(website: str):
    for j in search(website, tld="pl", num=1, stop=1):
        sa_speak(f"I found something! Opening {website}")
        webbrowser.open(j)


RESPONSES = {
    "time": "",
    "open google": ""
}

# TODO: open yt, open google, who made you, exit, who are you, search

if __name__ == '__main__':
    r = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)  # default is 200
    engine.setProperty('voice', voices[1].id)

    sa_speak("Welcome, I'm Macik, your speech assistant. How can I help you?")
    while True:
        query = sa_listen(r, mic)
        if "open website" in query:
            sa_open_website(query.split("open website")[-1])

        elif "that's all" in query:
            sa_speak("Thank you, see you later!")
            engine.stop()
            break
        # time.sleep(5)



