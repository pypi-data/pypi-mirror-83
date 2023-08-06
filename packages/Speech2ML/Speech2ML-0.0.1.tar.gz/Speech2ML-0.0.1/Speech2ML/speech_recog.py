# pip install speechrecognition
# pip install pipwin
# pipwin install pyaudio
# pip nltk
# pip jellyfish

import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:
    print('Say something:')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        if text.lower() == 'dino':
            print("Hey, what command do you want Speech2ML to add...")
            speech_cmd = r.listen(source)
            try:
                recognize_cmd = r.recognize_google(speech_cmd)
                action_cmd = cmd_identify(recognize_cmd)


        print('You said: {}'.format(text))
    except:
        print('Not recognize! Try again!')