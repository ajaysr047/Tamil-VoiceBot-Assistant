# Tamil-VoiceBot-Assistant
Simple Tamil voicebot/assistant using python 

## Packages used :
    chatterbot
    textblob
    pickle
    base64
    mimetypes
    os
    apiclient
    speech_recognition
    gtts
    
   python version:3.7.3

   pip version: 19.X

## Installtion 
    Run the shell script
    ./installPackages

## Starting the assistant
    python voice.py - for the voicebot
    python gmailTamil.py - for the gmail Module

## Known issues/bugs
    Voice commands not being recognized
    Package installation errors
        PortAudio - https://medium.com/@niveditha.itengineer/learn-how-to-setup-portaudio-and-pyaudio-in-ubuntu-to-play-with-speech-recognition-8d2fff660e94
    Playing Video - Some youtube videos aren't accessible through google custom search, Thus can lead to error.
    Live news - If Live stream is down the program will throw an error
    Parallel dataset for chitchat(Translation is employed)
    
  
## API enabling for gmail module
    https://developers.google.com/gmail/api/quickstart/python
    click on enable api, and download the credentials.json file. Put the credentials file in the same directory of the gmailTamil.py
    

## Useful Commands for Package installations
    pip install chatterbot
    pip install chatterbot-corpus
    pip install -U textblob
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    pip install gTTS
    pip install SpeechRecognition 
              https://pypi.org/project/SpeechRecognition/
   
    sudo apt-get install python-pyaudio python3-pyaudio  (-- For microphone)
              http://people.csail.mit.edu/hubert/pyaudio/#downloads
              
    sudo apt-get install mpg321
    pip install python-vlc
    pip install pafy
    pip install google-search
 
## Voicebot
    command for songs(video songs) - The initiating command is பாடல் or பாடல்கள் (examples: அனிருத் பாடல்கள் or அனிருத் பாடல் )
                      - stop the song - நிறுத்தவும் or நிறுத்துங்கள்
                      - pause the song - இடைநிறுத்து் or இடைநிறுத்தங்கள்
                      - play the paused song - இயக்கு or இயக்குங்கள்
                      
    command for news - The initiating command is செய்தி or செய்திகள் (examples: விளையாட்டு செய்திகள் or விளையாட்டு செய்தி )
                        (Opens news website in defaut browser)
                        
    command for live news - Initiating command - தமிழ் நேரலை செய்திகள்
    
    Normal chit-chat works as per the dataset.
    
    Time - Initiating command - நேரம் 
    
 ## Gmail module
 
    Gmail - Initiaiting command - மின்னஞ்சல்
            For verifications use - சரி for yes
                                
