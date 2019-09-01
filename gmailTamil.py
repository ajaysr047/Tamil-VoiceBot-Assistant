import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
import mimetypes
import os
from apiclient import errors
import speech_recognition as sr
from gtts import gTTS
from textblob import TextBlob

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://mail.google.com/']

def main():
    creds = ''
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    #Connect to API
    service = build('gmail', 'v1', credentials=creds)
  
    return service

def senderMailId(service):
  profile = (service.users().getProfile(userId='me').execute())
  senderMail = profile['emailAddress'] 
  
  return senderMail


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    #API Call
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print( 'Message Id: %s' % message['id'])
    return message
  except errors.HttpError:
    print ('An error occurred:')

def tamil2English(keyword):
    text = TextBlob(keyword)
    text = str(text.translate(from_lang='ta', to='en'))
    print(text)
    return text

def verifyCommon(part,data):
  talkTome(part+' '+data+' சரியானதா?')
  yesORno = ''
  yesORno = myCommand()
  if 'சரி' in yesORno:
    return True
  else :
    return False


def talkTome(audio):
    print(audio)
    tts = gTTS(text=audio, lang='ta')
    tts.save('GmailAudioTamil.mp3')
    os.system('mpg321 GmailAudioTamil.mp3')

def RecipientEmailDomain():
  domainInfo = 'பெறுநரின் மெயில் ஐடி டொமைனைத் தேர்வுசெய்க, கிடைக்கக்கூடிய விருப்பங்கள்: gmail.com, outlook.com, hotmail.com, yahoo.com'

  talkTome(domainInfo)

  domainAddress = 'gmail.com'
  domainID = ''
  domainID = myCommand()

  
  domainID = tamil2English(domainID)
  
  if  'Gmail' in domainID or 'gmail.com' in domainID:
    domainAddress = '@gmail.com'
    return domainAddress
  elif 'Outlook' in domainID or 'outlook.com' in domainID:
    domainAddress = '@outlook.com' 
    return domainAddress
  elif 'Yahoo' in  domainID or 'yahoo.com' in domainID:
    domainAddress = '@yahoo.com'   
    return domainAddress
  elif 'Hotmail' in domainID or 'hotmail.com' in domainID:
    domainAddress = '@hotmail.com' 
    return domainAddress   
  else:
    return domainAddress
  

def RecipientEmailUsername():
  talkTome('தயவுசெய்து பெறுநரின் மின்னஞ்சல் பயனர்பெயரைத் தட்டச்சு செய்க')
  print('Type now:')
  username = input()
  return username

def CombineEmailID(username,domain):
  return username+domain
  
def myCommand():
    command = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration= 1)
        print("Talk now")
        audio = r.listen(source, timeout=10)
    
    try:
        command = r.recognize_google(audio, language='ta')
        print('you said: '+ command + '\n')        
    #loop back to continue 
    except (sr.UnknownValueError):
        print('Error Recognizing the command')
        
    return command

def gAssist(command):
  domain = ''
  usrname = ''
  if command == 'மின்னஞ்சல்':
 
    domain = RecipientEmailDomain()
    verify = verifyCommon('டொமைன்', domain)

    while not verify:
      domain = RecipientEmailDomain()
      verify = verifyCommon('டொமைன்', domain)

    usrname = RecipientEmailUsername()
    verify = verifyCommon('பயனர்பெயர்', usrname)

    while not verify:
      usrname = RecipientEmailUsername()
      verify = verifyCommon('பயனர்பெயர்', usrname)
  
  return CombineEmailID(usrname, domain)


def getSubject():
  talkTome('தயவுசெய்து மின்னஞ்சல் பொருளை சொல்லுங்கள்')
  subject = myCommand()
  verify =  verifyCommon('பொருள்', subject)
  while not verify:
    talkTome('தயவுசெய்து மின்னஞ்சல் பொருளை சொல்லுங்கள்')
    subject = myCommand()
    verify =  verifyCommon('பொருள்', subject)

  return subject


def getMessage():
  talkTome('தயவுசெய்து செய்தியைச் சொல்லுங்கள்')
  message = myCommand()

  verify = verifyCommon('செய்தி', message)
  while not verify:
    talkTome('தயவுசெய்து செய்தியைச் சொல்லுங்கள்')
    message = myCommand()
    verify = verifyCommon('செய்தி', message)

  return message

if __name__ == '__main__':
    serviceObj = main()
    SenderMailID = senderMailId(serviceObj)
    RecipientMailID =  gAssist(myCommand())
    mailSubject = getSubject()
    mailMessage = getMessage()
    print(SenderMailID)
    print(RecipientMailID)
    print(mailSubject)
    messageObj =  CreateMessage(SenderMailID,RecipientMailID,mailSubject,mailMessage)
    messageSend = SendMessage(serviceObj,'me',messageObj)