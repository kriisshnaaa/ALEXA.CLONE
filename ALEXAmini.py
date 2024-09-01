import win32com.client as hehe
import speech_recognition as sr
import webbrowser
import pywhatkit as music
import datetime
from AppOpener import open,close
import os
from groq import Groq
import requests as temp
import json
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 50
        audio=r.listen(source)
        try:
            query=r.recognize_google(audio)
            print(f"your command is : {query}")
            return query 
        except Exception as e:
            return "sorry unable to recognize speech try speaking again"
mychat=""
def chat(query):
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": query,
        }
    ],
    model="llama3-8b-8192",
    )
    try:
        if "without speaking".lower() in query.lower():
            print(chat_completion.choices[0].message.content)
        else:
            print(chat_completion.choices[0].message.content)
            say(chat_completion.choices[0].message.content)
    except Exception as e:
        say("error")

def weather(query):
    b=f"https://api.weatherapi.com/v1/current.json?key=dbbb003b93064bc18c092710240806&q={query}"
    c=temp.get(b)
    d=json.loads(c.text)
    e=[d["current"]["temp_c"],d["current"]["temp_f"],d["location"]["localtime"]]
    say(f"the current weather of {query} at {e[2]} is {e[0]} degrees in celcius and {e[1]} in fahrenheit")
    print(e[0],"in celcius\n",e[1],"in fahrenheit")

    
def ai(prompt):
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama3-8b-8192",
    )
    try:
        print(chat_completion.choices[0].message.content) 
    except Exception as e:
        say("error")


speaker=hehe.Dispatch("SAPI.spVoice")
def say(t):
    speaker.speak(t)
def socialmedia_opener(platform,username):
    url=f"https://www.{platform}.com/{username}"
    webbrowser.open(url)
say("hey i am listening ")
while True:
    print("LISTENING...")
    query=takecommand()
    sites=[["youtube","https://youtube.com"],["facebook","https://facebook.com"],["google","https://google.com"],["books","https://en.wikipedia.org/wiki/Book"]]
        
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"opening {site[0]} sir")
            webbrowser.open(site[1])
    
    if "exit" in query:
        say("thanks for calling me  ")
        mychat=""
        break
    elif "play" in query:
        d=query.split("play")
        e=d[-1]
        music.playonyt(e)
    elif "tell me about" in query:
        c=query.split("about")
        topic=c[-1]
        link = f"https://www.google.com/search?q={topic}"
        webbrowser.open(link)

    elif "the time" in query:
        time=datetime.datetime.now().strftime("%H : %M : %S")
        say(f"sir the time is {time}")
    elif "open".lower() in query.lower():
        f=query.split("open")
        open(f[1],match_closest=True,output=False)
    elif "close" in query:
        f=query.split("close")
        close(f[1],match_closest=True,output=False)
    elif "artificial intelligence".lower() in query.lower():
        ai(prompt=query)
    elif "weather".lower() in query.lower():
        a=query.split("of")
        weather(a[-1])
    elif "social media".lower() in query.lower():
        say("tell the name of platform ")
        platform=takecommand()
        say("enter the username of the user ")
        a=input("enter the username of the user : ")
        socialmedia_opener(platform,a)

    else:
        chat(query)
    
    