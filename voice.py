# - *- coding: utf- 8 - *-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from textblob import TextBlob
from gtts import gTTS
import speech_recognition as sr 
import os
import webbrowser
import vlc, pafy, time
import search_google.api
import threading
import random
import sys


chatbot = ChatBot('Tamil Chat', logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Im sorry, I do not understand.',
            'maximum_similarity_threshold': 0.90
        },
		'chatterbot.logic.MathematicalEvaluation',
        {
            'import_path': 'timeLogicAdaptor.TimeLogicAdapter'
        }
		])
trainer = ListTrainer(chatbot)
conv1 = open('chat.txt', 'r').readlines()
trainer.train(conv1)
conv2 = open('chat2.txt', 'r').readlines()
trainer.train(conv2)
conv3 = open('chat3.txt', 'r').readlines()
trainer.train(conv3)
conv4 = open('chat4.txt', 'r').readlines()
trainer.train(conv4)
def tamil2English(keyword):
    text = TextBlob(keyword)
    text = str(text.translate(from_lang='ta', to='en'))
    print(text)
    return text


def playVideo(url):
    video = pafy.new(url)
    best = video.getbest()
    global media 
    media = vlc.MediaPlayer(best.url)
    media.play()
    timeout = time.time() + video.length + 3
    while True:
        if time.time() > timeout:
            media.stop()
            break

def playLiveVideo(url):
    video = pafy.new(url)
    best = video.getbest()
    global media 
    media = vlc.MediaPlayer(best.url)
    media.play()
    while True:
        pass

def DailyThanthi(query):
    # Define buildargs for cse api
    buildargs = {
    'serviceName': 'customsearch',
    'version': 'v1',
    'developerKey': 'AIzaSyCPIncTNH3uGx6jVAkZ_3GRImASiIVKoeY'
    }

    # Define cseargs for search
    cseargs = {
    'q': query,
    'cx': '017676376527666120669:b2wriwvqkja',
    'num': 3
    }

    # Create a results object
    results = search_google.api.results(buildargs, cseargs)
    url = results.links
    webbrowser.get('firefox').open(url[0])
    webbrowser.get('firefox').open(url[1])
    webbrowser.get('firefox').open(url[2])

def uTubeSearch(query):
    query = tamil2English(query)
    urlChoice = random.randint(0, 4)
    buildargs = {
    'serviceName': 'customsearch',
    'version': 'v1',
    'developerKey': 'AIzaSyCyquP_tuiTcVaQr-OeFWG8orS-93HPZhs'
    }

    # Define cseargs for search
    cseargs = {
    'q': query,
    'cx': '017676376527666120669:ccfdy4iiisk',
    'num': 5
    }

    # Create a results object
    results = search_google.api.results(buildargs, cseargs)
    url = results.links
    print(url)
    print(urlChoice)
    return url[urlChoice]

def talkTome(audio):
    print(audio)
    tts = gTTS(text=audio, lang='ta')
    tts.save('audio.mp3')
    os.system('mpg321 audio.mp3')

#Listens for commands

def myCommand():
    command = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("I am ready for your next command")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration= 1)
        print("Talk now")
        audio = r.listen(source, timeout=10)
    
    try:
        command = r.recognize_google(audio, language='ta-IN')
        print('you said: '+ command + '\n')
        #talkTome(command)
    #loop back to continue 
    except (sr.UnknownValueError):
        assistant(myCommand())
    except sr.WaitTimeoutError:
        assistant(myCommand())
    return command
#If statements

def assistant(Vcommand):
    if 'பாடல்கள்' in Vcommand or 'பாடல்' in Vcommand:
        thread1 = threading.Thread(target=playVideo, args=(uTubeSearch(Vcommand),))
        thread1.start()
        time.sleep(10)      
    # elif 'பாடல்களை நிறுத்தவும்'  in Vcommand or 'பாடல்களை நிறுத்துங்கள்' in Vcommand:
    #     media.stop()
    # elif 'பாடல்களை இடை நிறுத்துங்கள்' in Vcommand or 'பாடல்களை இடைநிறுத்தங்கள்' in Vcommand:
    #     media.pause()
    # elif 'பாடல்களை இயக்கு' in Vcommand or 'பாடல்களை இயக்குங்கள் ' in Vcommand:
    #     media.play()
    elif 'நிறுத்தவும்'  in Vcommand or 'நிறுத்துங்கள்' in Vcommand:
        media.stop()
    elif 'இடைநிறுத்து்' in Vcommand or 'இடைநிறுத்தங்கள்' in Vcommand:
        media.pause()
    elif 'இயக்கு' in Vcommand or 'இயக்குங்கள் ' in Vcommand:
        media.play()
    elif 'தமிழ் நேரலை செய்திகள்' in Vcommand:
        thread2 = threading.Thread(target=playLiveVideo,args=('https://www.youtube.com/watch?v=ntwdBX-PZpA',))
        thread2.start()
        time.sleep(10)
    # elif 'செய்தியை நிறுத்தவும்'  in Vcommand or 'செய்தியை நிறுத்துங்கள்' in Vcommand:
    #     media.stop()
    # elif 'செய்தியை இடை நிறுத்துங்கள்' in Vcommand or 'செய்தியை இடைநிறுத்தங்கள்' in Vcommand:
    #     media.pause()
    # elif 'செய்தியை இயக்கு' in Vcommand or 'செய்தியை இயக்குங்கள் ' in Vcommand:
    #     media.play()
    elif 'செய்தி' in Vcommand or 'செய்திகள்' in Vcommand:
        DailyThanthi(Vcommand)
    else:
        userInp = TextBlob(Vcommand)
        userInp = str(userInp.translate(from_lang='ta', to='en'))
        
        botResp = chatbot.get_response(userInp)
        botResp = TextBlob(str(botResp))
        botResp = str(botResp.translate(from_lang='en', to='ta'))

        talkTome(botResp)
        assistant(myCommand())

talkTome('வணக்கம்')

while True:
    assistant(myCommand())
