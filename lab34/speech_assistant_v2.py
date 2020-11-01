import webbrowser
import random
import googlesearch
import wikipedia
from gtts import gTTS
from playsound import playsound

import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import os
import librosa
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

"""
Currently available instructions:
- 'marvin' - play song 'Marvin" on YouTube
- 'wow' - ???
- 'cat' - show cats in Google Graphics
- 'dog' - read dog info on Wikipedia
- 'stop' - exit script
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

SAMPLE_RECORDS = [
    "r_marvin.wav",
    "r_cat.wav",
    "r_dog.wav",
    "r_wow.wav",
    "r_stop.wav"
]


def sa_predict(audio):
    labels=["stop", "marvin", "wow", "cat", "dog"]

    le = LabelEncoder()
    y = le.fit_transform(labels)
    classes = list(le.classes_)

    prob = model.predict(audio.reshape(-1, 8000, 1))
    index = np.argmax(prob[0])
    return classes[index]


def sa_speak(text: str):
    if os.path.isfile("text.mp3"):
        os.remove("text.mp3")

    tts = gTTS(text, lang='en-gb')
    tts.save("text.mp3")
    playsound("text.mp3")


def sa_listen(file=None) -> str:
    sampleRate = 16000
    duration = 1 # seconds
    filename = 'record.wav'

    if file is None:
        sa_speak("How can I help you?")
        print("Talk now")
        print("Talk now")
        myData = sd.rec(int(sampleRate * duration), samplerate=sampleRate, channels=1, blocking=True)
        print("Stop talking")
        sd.wait()
        sf.write(filename, myData, sampleRate)

        samples, sampleRate = librosa.load('record.wav', sr=sampleRate)
        samples = librosa.resample(samples, sampleRate, 8000)

    else:
        samples, sampleRate = librosa.load(file, sr=sampleRate)
        samples = librosa.resample(samples, sampleRate, 8000)

    return sa_predict(samples)


if __name__ == '__main__':
    model = load_model('bestModel_set3_80_forSpeechAssistant.hdf5')

    isInDemoWrittenMode = False

    sa_speak(random.choice(REPLIES["welcome"]))
    while True:
        if not isInDemoWrittenMode:
            query = sa_listen()
            print(query)
        else:
            query = sa_listen(SAMPLE_RECORDS[0])
            print(query)

        if "cat" in query:
            url = "https://www.google.com.tr/search?q={}".format("cat")
            sa_speak("No problem!")
            webbrowser.open(url)

        elif "dog" in query:
            info = wikipedia.summary("dog ", sentences=3)
            sa_speak("According to Wikipedia")
            sa_speak(info)

        elif "marvin" in query:
            website = "schafter marvin youtube"
            for j in googlesearch.search(website, tld="pl", num=1, stop=1):
                sa_speak(f"I found something! Opening {website}")
                webbrowser.open(j)

        elif "wow" in query:
            sa_speak("Sorry, this feature is not implemented yet.")
            # TODO: make implementation for 'wow'

        elif "stop" in query:
            sa_speak(random.choice(REPLIES["exit"]))
            break

        if isInDemoWrittenMode:
            break
        else:
            time.sleep(10)
