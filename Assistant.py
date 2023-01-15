from matplotlib.pyplot import close
import pyttsx3 
import speech_recognition as sr 
import datetime 
import wikipedia
import webbrowser
import os
import time  
import smtplib
import Email
import ShowNews
import pyautogui
from psutil import virtual_memory
from gtts import gTTS
from playsound import playsound
from googletrans import Translator
import sys
import processor
import functions
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from User_Interface import Ui_Dialog

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine. setProperty("rate", 192)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def Intro_Assistant():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")   

    else:
        speak("Good Evening Sir!")  

    speak("Allow me to introduce myself. I am Jarvis, A virtual artificial intelligence and I am here to assist you with the variety of tasks as best as I can. System is now fully operational.")    

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(Email.username, Email.password)
    server.sendmail(Email.username, to, content)
    server.close()
 
def webBrowerOpen(site_name):
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    speak("Opening the browser")
    webbrowser.get('chrome').open_new_tab(site_name)

def fileOrganizer(Loc):
    def creatFolderIfNotExist(folder,Loc):
        if not os.path.exists(Loc+folder):
           os.makedirs(Loc+folder)
    def Move(folderName,files,Loc):
        for file in files:
           os.replace(Loc+file,f"{Loc+folderName}/{file}")
    Loc=="C:\\Users\\Syd.Shahzad\\Downloads\\"
    files=os.listdir(Loc)
    creatFolderIfNotExist("Images",Loc)
    creatFolderIfNotExist("Media",Loc)
    creatFolderIfNotExist("Docs",Loc)
    creatFolderIfNotExist("Others",Loc)

    ImgExt=[".png",".jpg",".jpeg","bmp"]
    DocExt=[".doc",".docx",".pdf",".ppt",".txt",".csv"]
    MediaExt=[".mp4",".mp3",".mkv",".ogg",".m4r",".flv"]
    Images=[file for file in files if os.path.splitext(file)[1].lower() in ImgExt ]
    Media=[file for file in files if os.path.splitext(file)[1].lower() in MediaExt ]
    Doc=[file for file in files if os.path.splitext(file)[1].lower() in DocExt ]
    others=[]
    for file in files:
      ext=os.path.splitext(file)[1].lower()
    if (ext not in ImgExt) and (ext not in MediaExt) and  (ext not in DocExt):
        others.append(file)
    Move("Images",Images,Loc)
    Move("Media",Media,Loc)
    Move("Docs",Doc,Loc)
    Move("Others",others,Loc)
   
class MainThread(QThread):
       
       def __init__(self):
           super(MainThread,self).__init__()
         
       def run(self):
           self.TaskExecution()     
      
       def takeCommand(self):
            with open("Connect.txt","w") as f:
                f.write("Listening...")       
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 0.84  #0.83
                audio = r.listen(source)
                with open("Connect.txt","w") as f:
                    f.write("Recognizing...")   
            try:
                query = r.recognize_google(audio, language='en-us')
                with open("Connect.txt","w") as f:
                    f.write(f"User said: {query}")
        
            except Exception as e:
                print("Say that again please...")  
                return "None"
            # if query!="None":
            #     playsound("Sounds\\Recognize.mp3")
            return query
                
       def TaskExecution(self):

        while True:
            self.query=self.takeCommand().lower()
            reply=processor.assistant_response(self.query)
            
            if "on wikipedia" in self.query:
                speak("Searching on Wikipedia...")
                try:
                    self.query = self.query.replace("on wikipedia", "")
                    results = wikipedia.summary(self.query, sentences=2,auto_suggest=False,redirect=True)
                    speak("According to Wikipedia")
                    with open("Connect.txt","w") as f:
                        f.write(results)
                    speak(results)
                except Exception:
                    speak("Error occurred while searching")
        
            elif "open_youtube"==reply:
                speak("What you want search on YouTube")
                response=self.takeCommand()
                speak(f"Okay, Searching {response} on YouTube")
                webBrowerOpen(f"https://www.youtube.com/results?search_query={response}")     
            
            elif "time"==reply:
                functions.date_time()
            
            elif "sleep"==reply:
                functions.sleep_system()

            elif "close_browser"==reply:
                functions.close_browser()
            
            elif "joke"==reply:
                functions.joke()
            
            elif "play_music"==reply:
                functions.play_music()

            elif "close_media_player"==reply:
                functions.close_media_player()
            
            elif "open_vs_code"==reply:
                functions.open_vs_code()
            
            elif "open_notepad"==reply:
                functions.open_notepad()
            
            elif "close_notepad"==reply:
                functions.close_notepad()
            
            elif "close_browser"==reply:
                functions.close_browser()
            
            elif "weather"==reply:
                functions.weather()
            
            elif "voice_change"==reply:
                functions.voice_change()
            
            elif "my_ip_address"==reply:
                functions.my_ip_address()

            elif "quite"==reply:
                functions.quit()

            elif "open_google"==reply:   
                speak("sir,what should i search on google")
                try:
                    cm=self.takeCommand()
                    webBrowerOpen(f"www.google.com/search?q={cm}")     
                except Exception as e:
                    speak("please say again I didn't hear anything")
        
            elif "open_stackoverflow"==reply:
                speak("opening stackoverflow.com")
                webBrowerOpen("www.stackoverflow.com")
                
            elif "NoteDown"==reply:
                speak("Ok, sir. Say the sentence.")
                sentence=self.takeCommand()
                Date=datetime.datetime.now().date()
                Time=datetime.datetime.now().time()
                with open("Notes.txt","w") as f:
                    f.write(sentence)
                speak("Done sir. Would you like to add Date and Time for this notes?")
                user_said=self.takeCommand()
                if "yes" in user_said or "ok" in user_said:
                    with open("Notes.txt","a") as f:
                        f.write("\n\nTime: "+str(Time)+"\n"+"Date: "+str(Date))
                speak("This is what I have written.")
                os.startfile("Notes.txt")

            elif "GK_question"==reply:
                speak("ok,what is your question")
                question=self.takeCommand()
                try:
                    answer=functions.Gk_Search(question)
                    with open("Connect.txt","w") as f:
                        f.write(answer)
                    speak(answer)
                except Exception:
                    speak("Error Occurred while searching")
            
            elif "send_email"==reply:
                try:
                    speak("What should I say?")
                    content = self.takeCommand()
                    to = "yourmail@gmail.com"    
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry , I am not able to send this email")  
            
            elif "whatsapp"==reply:
                import pywhatkit
                speak("Say the mobile number")
                number=self.takeCommand()
                speak("Say your message ")
                pywhatkit.sendwhatmsg(number,"Message",15,20)
                time.sleep(120)
                speak("message has been sent")
            
            elif "organize_files"==reply:
                speak("In which directory Sir.")
                user=self.takeCommand().lower()
                if "download" in user or "downloads" in user:
                    location="C:\\Users\\Syd.Shahzad\\Downloads\\"
                    fileOrganizer(location)
                    speak("Operation completed successfully")
                elif "document" in user or "documents" in user:
                    location="C:\\Users\\Syd.Shahzad\\Documents\\"
                    fileOrganizer(location)
                    speak("Operation completed successfully")
                else:
                    speak("Sorry sir, It's not available for this directory")
            
            elif "news_headlines"==reply:
                speak("Which category are you interested in?")
                with open("Connect.txt","w") as f:
                    f.write("1.Business\n2.Entertainment\n3.General\n4.Health\n5.Science\n6.Technology\n\n")
                time.sleep(1)
                try:
                    news_category=self.takeCommand().lower()
                    ShowNews.NewsHeadlines("India",news_category)
                    with open("news.txt","r") as f:
                        news=f.read()
                    with open("Connect.txt","w") as f:
                        f.write(news)
                    speak(news)
                    os.remove("news.txt")
                except Exception:
                    speak("Invalid category.")
                
            elif "take_screenshot"==reply:
                speak("Sir, please tell me the name for this screenshot file")
                name=self.takeCommand()
                speak("Please hold the screen for few seconds, I am taking screenshot")
                time.sleep(3)
                img=pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("I am done sir, The screenshot is saved in our main folder. Ready for next command")

            elif "hide_files"==reply:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition=self.takeCommand()
                if "hide" in condition:
                    os.system("attrib +h /s /d")
                    speak("Sir, all the files in this folder are now hidden.")
                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("Sir, all the files in this folder are now visible to everyone.")
                elif "leave it" in condition or "leave for now" in condition :
                    speak("Ok sir")

            elif "instagram_profile"==reply:
                speak("sir please enter the user name correctly")
                name=input("Enter username here : ")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Here is the profile of the user {name}")
            
            elif "calculation"==reply:
                speak("Say the expression")
                user_in=self.takeCommand().lower()
                operands=[int(word) for word in user_in.split() if word.isdigit()]
                if "+" in user_in:
                    speak(operands[0]+operands[1])
                elif "-" in user_in:
                    speak(operands[0]-operands[1])
                elif "*" in user_in or "x" in user_in:
                    speak(operands[0]*operands[1])
                elif "/" in user_in:
                    speak(float(operands[0]/operands[1]))
                elif "%" in user_in or "modulus" in user_in:
                    try:
                        speak(f"The remainder is {operands[0]%operands[1]}")
                    except Exception:
                        speak("Error : Index out of range.")
                             
            elif "translate"==reply:
                speak("Say the sentence")
                to_translate=self.takeCommand()
                speak("in which language do want to translate it.")
                lang_choice=self.takeCommand().lower()
                translator = Translator()
                if "urdu" in lang_choice:
                    translated_sen=translator.translate(to_translate, dest='ur')
                    obj=gTTS(text=translated_sen.text,slow=False,lang='ur')
                    obj.save('urdu.mp3')
                    playsound('urdu.mp3')
                    os.remove("urdu.mp3")
                    
                elif "hindi" in lang_choice:
                    translated_sen=translator.translate(to_translate, dest='hi')
                    obj=gTTS(text=translated_sen.text,slow=False,lang='hi')
                    obj.save('hindi.mp3')
                    playsound('hindi.mp3')
                    os.remove("hindi.mp3")
                elif "marathi" in lang_choice:
                    translated_sen=translator.translate(to_translate, dest='mr')
                    obj=gTTS(text=translated_sen.text,slow=False,lang='mr')
                    obj.save('marathi.mp3')
                    playsound('marathi.mp3')
                    os.remove("marathi.mp3")

            elif "brightness_control"==reply:
                functions.brightness_control(self.query)
       
            elif "shift_nightLight"==reply:
                functions.shift_nightLight()
            
            elif "amazon_search"==reply:
                speak("What product do you want to search?")
                p=self.takeCommand()
                link=f"https://www.amazon.in/s?k={p}&crid=3ICDTMJJY1EFA&sprefix=smart+p%2Caps%2C802&ref=nb_sb_noss_2"
                webBrowerOpen(link)

            elif "youtubePlay"==reply:
                functions.youtubePlay(self.query)

            elif "bitcoin_price"==reply:
                functions.get_Bitcoin_Price()
            
            else:
                if "none"!=self.query:
                    speak(reply)
                       
startExecution=MainThread()

class Main(QDialog):
       
       def __init__(self):
           super().__init__()
           self.ui=Ui_Dialog()
           self.ui.setupUi(self) 
           self.setWindowTitle("Assistant")
           self.ui.pushButtonStart.clicked.connect(self.startTask)
           self.ui.pushButtonExit.clicked.connect(self.Exit)

       def Exit(self):
           playsound("Sounds\\Exit.mp3")
           exit()

       def startTask(self):
           with open("Connect.txt","w") as f:
             f.write(" ")
           self.ui.movie=QtGui.QMovie(":/Images/Image/background.jpg")
           self.ui.labelMain.setMovie(self.ui.movie)
           self.ui.movie.start()
           self.ui.movie=QtGui.QMovie(":/Images/Image/RoundAnim.gif")
           self.ui.labelJarvisStart.setMovie(self.ui.movie)
           self.ui.movie.start()
           self.ui.movie=QtGui.QMovie(":/Images/Image/SideAnimation.gif")
           self.ui.labelSideAnim.setMovie(self.ui.movie)
           self.ui.movie.start()
           self.ui.movie=QtGui.QMovie(":/Images/Image/Ram.gif")
           self.ui.labelRam.setMovie(self.ui.movie)
           self.ui.movie.start()
           
           timer = QTimer(self)
           timer.timeout.connect(self.startTime)
           timer.start(1000)
           Ctimer=QTimer(self)
           Ctimer.timeout.connect(self.startConsole)
           Ctimer.start(500)     
           Ctimer.timeout.connect(self.RamUsage)
           Ctimer.start(100) 
           playsound("Sounds\\Start.mp3")    
           startExecution.start()
 
       def startConsole(self):
           f=open('Connect.txt','r',encoding="utf-8")
           self.ui.textBrowserConsole.setText(str(f.read()))
       
       def RamUsage(self):
            self.ui.textBrowserRam.setText(f'{virtual_memory()[2]} %')

       def startTime(self):
            current_time =time.strftime("%I:%M %p")
            self.ui.labelTime.setText(str(current_time))
   
app=QApplication(sys.argv)
jarvis=Main()
jarvis.show()
sys.exit(app.exec_())


           
            
           
