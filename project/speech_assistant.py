import speech_recognition as sr
import webbrowser
import random
import os
import googlesearch
import wikipedia
from gtts import gTTS
from playsound import playsound
from datetime import datetime

"""
Currently available instructions:
- 'Search ...'
- 'Open website ...'
- 'What time is it?'
- 'What is the weather in ...?'
- 'Tell me about ...'
- 'Who are you?'
- 'Who made you?'
- exit script
"""

REPLIES = {
    "welcome": [
        "Welcome. I'm Maciak, your speech assistant.",
        "Hi there. I hope you're fine today.",
        "Hello, Sir."
    ],
    "not understand": [
        "Sorry, I don't understand.",
        "I'm so sorry. I don't know what you said.",
        "I'm not sure about what you said."
    ],
    "exit": [
        "Thank you, see you later!",
        "I was happy to help you. Goodbye!",
        "Goodbye.",
        "I'll be waiting for you here."
    ]
}

INSTRUCTIONS = {
    "exit": [
        "this is all",
        "exit",
        "bye"
    ]
}

SAMPLE_REQUESTS = [
    "search how far is from Earth to Moon",
    "open website harvard university",
    "what time is it",
    "what is the weather in Krakow",
    "tell me about facebook",
    "who are you",
    "who made you",
    "exit"
]


def sa_speak(text: str):
    if os.path.isfile("text.mp3"):
        os.remove("text.mp3")

    tts = gTTS(text, lang='en-gb')
    tts.save("text.mp3")
    playsound("text.mp3")


def sa_listen(recogniser, microphone) -> str:
    with microphone as source:
        recogniser.adjust_for_ambient_noise(source, duration=2)
        sa_speak("How can I help you?")
        print("Say something")
        audio = recogniser.listen(source)

    try:
        query = recogniser.recognize_google(audio)
        print(f"User said:\n{query}\n")

    except Exception as e:
        print("Unable to recognize voice.")
        sa_speak(random.choice(REPLIES["not understand"]))
        return ""

    return query.lower()


if __name__ == '__main__':
    r = sr.Recognizer()
    mic = sr.Microphone()

    r.operation_timeout = 7  # in seconds
    isInDemoWrittenMode = True

    sa_speak(random.choice(REPLIES["welcome"]))
    while True:
        if not isInDemoWrittenMode:
            query = sa_listen(r, mic)
        else:
            query = SAMPLE_REQUESTS[1]

        if "search" in query:
            url = "https://www.google.com.tr/search?q={}".format(query.split("search")[-1])
            sa_speak("No problem!")
            webbrowser.open(url)

        elif "open website" in query:
            website = query.split("open website")[-1]
            if "google" in website:
                webbrowser.open("https://www.google.com/")
            else:
                for j in googlesearch.search(website, tld="pl", num=1, stop=1):
                    sa_speak(f"I found something! Opening {website}")
                    webbrowser.open(j)

        elif "time" in query:
            current_time = datetime.now().strftime("%H:%M")
            sa_speak(f"It's {current_time}")

        elif "weather" in query:
            phrase = query.split("weather")[-1]
            place = phrase.split("in")[-1]
            url = "https://www.google.com/search?q={}".format(query.split("search")[-1])
            sa_speak(f"Let me check the weather in {place}")
            webbrowser.open(url)

        elif "tell me about" in query:
            topic = query.split("about")[-1]
            if topic:
                info = wikipedia.summary(topic, sentences=3)
                sa_speak("According to Wikipedia")
                sa_speak(info)

            else:
                print("Unable to recognize the topic.")
                sa_speak(random.choice(REPLIES["not understand"]))

        elif "who are you" in query:
            sa_speak("I'm Maciak, your personal speech assistant.")

        elif "who made you" in query:
            sa_speak("I have been created by Martin and Jacob.")

        elif any(expression in query for expression in INSTRUCTIONS["exit"]):
            sa_speak(random.choice(REPLIES["exit"]))
            break

        if isInDemoWrittenMode:
            break
