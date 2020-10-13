import speech_recognition as sr
import webbrowser
import pyttsx3
from datetime import datetime
from googlesearch import search


def sa_speak(text: str):
    engine.say(text)
    engine.runAndWait()


def sa_listen(recogniser, microphone) -> str:
    with microphone as source:
        recogniser.adjust_for_ambient_noise(source, duration=2)
        sa_speak("How can I help you, sir?")
        audio = recogniser.listen(source)

    try:
        query = recogniser.recognize_google(audio)
        print(f"User said:\n{query}\n")

    except Exception as e:
        print("Unable to recognize voice.")
        print(e)
        return ""

    return query.lower()


EXIT_EXPRESSIONS = [
    "this is all",
    "exit",
    "bye"
]

if __name__ == '__main__':
    r = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)  # default is 200
    engine.setProperty('voice', voices[2].id)

    sa_speak("Welcome, Sir. I'm Macik, your speech assistant.")
    while True:
        query = sa_listen(r, mic)

        if "search" in query:
            url = "https://www.google.com.tr/search?q={}".format(query.split("search")[-1])
            webbrowser.open(url)

        elif "open website" in query:
            website = query.split("open website")[-1]
            for j in search(website, tld="pl", num=1, stop=1):
                sa_speak(f"I found something! Opening {website}")
                webbrowser.open(j)

        elif "time" in query:
            current_time = datetime.now().strftime("%H %M")
            sa_speak(f"It's {current_time}")

        elif "who made you" in query:
            sa_speak("I have been created by Martin and Jacob")

        elif any(expression in query for expression in EXIT_EXPRESSIONS):
            sa_speak("Thank you, see you later!")
            engine.stop()
            break
