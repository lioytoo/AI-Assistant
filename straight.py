from datetime import datetime
import pyttsx3
from TTS.api import TTS
print(TTS.list_models())


        
engine = pyttsx3.init()    
voices = engine.getProperty("voices")

def alarm():
    now = datetime.now()

    # Format address politly, add a small prefix
    engine.setProperty('voice', voices[29].id)
    a=engine.getProperty('voice')
    print(a)
    engine.setProperty('rate', 200)  # adjust as you like
    engine.setProperty('volume', 1.0)
    if now.hour == 20 and now.minute == 46:
        message = "Alarm! Time's up!"
        engine.say(message)
        engine.runAndWait()
alarm()
