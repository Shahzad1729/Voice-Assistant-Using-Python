from random import randint
import pyttsx3
import datetime
import os
from pyautogui import click,moveTo
from subprocess import run
import pyjokes
import socket
import wolframalpha

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine. setProperty("rate", 192)

def Gk_Search(question):
    app_id="PG2U4K-AW69GEQ4R2"
    client=wolframalpha.Client('R2K75H-7ELALHR35X')
    try:
        res=client.query(question)
        answer=next(res.results).text
        return answer        
    except Exception:
        speak("Error Occurred while searching")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def date_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"Sir, the time is {strTime}")

def sleep_system():
    speak("System in undergoing sleep mode")
    os.system("rundll32.exe powerof.dll.SetSuspendState 0,1,0")

def close_browser():
    speak("okay sir, closing the browser")
    os.system("taskkill /f /im chrome.exe")

def joke():
    joke = pyjokes.get_joke(language='en', category='all')
    speak("Ok")
    with open("Connect.txt", "w") as f:
        f.write(joke)
    speak(joke)

def play_music():
    music_dir = 'F:\\Songs'
    songs = os.listdir(music_dir)
    song = randint(0, 180)
    os.startfile(os.path.join(music_dir, songs[song]))

def close_media_player():
    speak("okay sir, closing VLC Media player")
    os.system("taskkill /f /im vlc.exe")

def open_vs_code():
    codePath = "C:\\Users\\SHAIKH AFFAN\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    os.startfile(codePath)

def open_notepad():
    speak("Opening notepad")
    path = "C:\\Windows\\system32\\notepad.exe"
    os.startfile(path)

def close_notepad():
    speak("okay sir, closing notepad")
    os.system("taskkill /f /im notepad.exe")

def weather():
    temp=Gk_Search("weather forecast of Jalgaon, Maharashtra")
    with open("Connect.txt","w",encoding='utf-8') as f:
        f.write(temp)
    speak(f"The temperature is in {temp}")
       
def youtubePlay(videoName):
    videoName=videoName.replace("on","")
    videoName=videoName.replace("play","")
    videoName=videoName.replace("YouTube","")
    import pywhatkit
    pywhatkit.playonyt(videoName)

def voice_change():
    engine.setProperty('voice', voices[1].id)
    speak("Voice changed successfully.")

def my_ip_address():
    ip_address = socket.gethostbyname(socket.gethostname())
    print(ip_address)
    with open("Connect.txt", "w") as f:
        f.write(ip_address)
    speak(f"Your IP address is {ip_address}")

def get_Bitcoin_Price():
    price=Gk_Search("bitcoin price")
    with open("Connect.txt","w",encoding="utf-8") as f:
            f.write(price)
    price=price.replace("(Indian rupees)","")
    speak(f"current price of bitcoin is {price}")

def brightness_control(query):
    query=query.replace("%"," ")
    value=[int(word) for word in query.split() if word.isdigit()]
    run(["powershell", "-Command", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{value[0]})"], capture_output=True)
    speak(f"Screen brightness is set to {value[0]} percent successfully")

def shift_nightLight():
    speak("Switching night night")
    run(["powershell", "-Command", "start ms-settings:nightlight"], capture_output=True)
    moveTo(68,202,1)
    click(68,202)

    moveTo(1340,15,1)
    click(1340,15)

def quit():
    speak("Thanks for giving me the chance to help you, have a good day sir")
    exit()
