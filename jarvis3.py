from tkinter import *
import random
import os
import vlc
import pyttsx3
import webbrowser
import speech_recognition as sr
import wikipedia
import datetime
import threading

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def intro():
    global cnt,txt
    if cnt>=len(logo):
        cnt = 0
        txt = ''
        Lbl.config(text=txt)
    else:
        txt = txt+logo[cnt]
        Lbl.config(text=txt)
        cnt += 1
    Lbl.after(150,intro)

def intro_color():
    color = random.choice(colour)
    Lbl.config(fg=color)
    Lbl.after(20,intro_color)

def temp(e):
    query_entry.delete(0,"end")

def speak(audio):
    if audio!=None:
        print('Nova: '+audio)
        engine.say(audio)
        engine.runAndWait()

def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning!')

    if hour >= 12 and hour < 18:
        speak('Good Afternoon!')

    if hour >= 18 and hour !=0:
        speak('Good Evening!')

greetMe()

speak('Hello Sir, I am your digital assistant Nova!')
speak('How may I help you?')

def myCommand():
    def recognize_audio():
        
        
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Listening...")
            r.pause_threshold =  1
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')
            query_entry.delete(0, END)
            query_entry.insert(0, query)
            result = get_result(query)
            speak(result)
            
        except sr.UnknownValueError:
            speak("Sorry sir! I didn't get that! Please type your command.")
            query_entry.focus_set()

    threading.Thread(target=recognize_audio, daemon=True).start()
    
def get_result(query):
    query=query.lower()

    if 'open youtube' in query:
        speak('Opening Youtube...')
        webbrowser.open('www.youtube.com')

    elif 'open google' in query:
        speak('Opening Google...')
        webbrowser.open('www.google.co.in')

    elif 'open whatsapp' in query:
        speak('Opening WhatsApp Web...')
        webbrowser.open('https://web.whatsapp.com/')    

    elif 'open gmail' in query:
        speak('Opening Gmail...')
        webbrowser.open('www.gmail.com')

    elif "what\'s up" in query or 'how are you' in query:
        stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
        return random.choice(stMsgs)

    elif 'hello' in query or 'hi' in query:
        stMsgs = ['Hello Sir!', 'Hi there!', 'Hello!', 'Hi!']
        return 'Hello Sir!'

    elif 'bye' in query or 'exit' in query:
        speak('Bye Sir, have a good day.')
        quit()

    elif 'search for' in query:
        query = query.replace('search for', '')
        speak(f'Searching for {query}...')
        webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")

    else:
        return "Sorry, I didn't understand that."

def click():
    query = query_entry.get()
    result = get_result(query)
    speak(result)

root=Tk()
root.title("Nova")
root.geometry('920x660')
root.iconbitmap("nova_icon.ico")

nova_img=PhotoImage(file='nova_pic.png')
nova_imge=Label(root,image=nova_img)
nova_imge.pack()

logo='NOVA'
cnt = 0
txt = ''
colour = ['royalblue','blue','goldenrod2','gray25']    
Lbl=Label(root,text=logo,relief='flat',font=('micro 5',30,'bold'),bg='#021f65',width=6,height=1)
Lbl.place(x=400,y=130)
intro()
intro_color()

query_entry=Entry(root,font=('Cascadia Code Light',20),fg='dark slate gray',width=45)
query_entry.insert(0,"Type something...")
query_entry.place(x=100,y=600)
query_entry.bind("<FocusIn>", temp)

send_icon=PhotoImage(file="send_icon.png")
send_btn=Button(root,image=send_icon,command=click)
send_btn.place(x=840,y=600)

voice_icon=PhotoImage(file="mic_ico.png")
voice_btn=Button(root,image=voice_icon,command=myCommand)
voice_btn.place(x=50,y=600)

root.resizable(0,0)

root.mainloop()
