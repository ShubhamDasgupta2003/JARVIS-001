import pyttsx3 as pt
import datetime as dt
import speech_recognition as sr
import os
import wikipedia as wkp
import webbrowser as web
import requests as rqst
import re
import atmosphere as atm
import WeatherForecast as weather_cast
from geopy.geocoders import ArcGIS

newsApiKey = ''         # Put your API Key here
newsurl = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={}".format(newsApiKey)

engine = pt.init("sapi5");
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)

def speak(audio):
    """This function converts text to speech"""
    
    engine.say(audio)
    engine.runAndWait()

def wishme():
    """This function wish the user and tells the date and time"""
    month_names = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

    time = dt.datetime.now()
    date = dt.datetime.today()
    hour = int(time.hour)
    timestr = "The time is {}:{}".format(str(time.hour),str(time.minute))   #Current time to
                                                                                    #speak
    datestr = "Today is {}-{}-{}".format(str(date.day),str(month_names[date.month]),str(date.year))
    if hour >=0 and hour <= 12:                                                     
        speak("Good Morning master Shubham..")
        timestr+= "AM"
    elif hour>12 and hour <= 17:
        speak("Good Afternoon master Shubham..")
        timestr+= "PM"
    elif hour>17 and hour <=24:
        speak("Good Evening master Shubham..")
        timestr+= "PM"
    speak(timestr+" and "+datestr)
    speak("I'm JARVIS, How can I help you?")

def readNews(num):

    news = rqst.get(newsurl).json()
    article = news["articles"]
    newslist = []
    for arti in article:
        newslist.append(arti['title'])
    for i in range(0,num):
        print(str(i+1) +"."+newslist[i])
        speak(newslist[i])

def readTemp(place):
    clouds,temp,feel_temp = atm.showTemp(place)
    aqi,rating,comps = atm.showAirQuality(place)
    return "The current temperature at {} is {:.2f} degree celsius with {}. Air quality is {}".format(place,temp,clouds,rating)

def makeToDoList():
    filename = "F:\\myfolder\\To_do_list.txt"
    fileobj = open(filename,"w+")
    choice = 'yes'
    sl_no = 0
    while choice == 'yes':
        sl_no +=1
        speak("Please tell the task to add..")
        task = takeCommand().lower()
        fileobj.write("{}. {}\n".format(sl_no,task.upper()))
        speak("Task added succesfully.. Do you want to add more task?")
        choice = takeCommand().lower()
    fileobj.close()

def readToDoList():
    """It reads out the tasks in to-do list"""
    
    filename = "F:\\myfolder\\To_do_list.txt"
    fileobj = open(filename,"r") 
    for lines in fileobj:
        say = lines.strip()
        print(say)
        speak(say)
    fileobj.close()
    speak("  That's all in the list.")

def getPlace(cmnd):
    """To extract name of place from query"""
    
    pattern = r'( at| in| of)'
    res = re.search(pattern,cmnd)
    dest = cmnd[res.end()+1:]
    return(dest) 

def takeCommand():
    """It converts speech to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='eng-in')
        return query
    except Exception as e:
        print("Please say that again...")
        return "none"

                                            #Main Function starts here
if __name__ == "__main__":
    wishme()
    while (True):
        query = takeCommand().lower()

        if("about" in query or "who is" in query):
            speak("Searching wikipedia...")
            try:
                results = wkp.summary(query,sentences=2)
            except Exception as e:
                speak("Sorry no information found!...")
                continue
            speak("According to wikipedia ")
            speak(results)

        elif("open youtube" in query):
            web.open("www.youtube.com",0)

        elif("news" in query):
            print(query)
            pattern = r'[0-9]+'
            result = re.search(pattern,query)
            if result == None:
                speak("Here is top 5 news.")
                readNews(5)
                continue
            else:
                readNews(int(result.group(0)))

        elif("weather condition" in query or 'temperature' in query):
            dest = getPlace(query)
            if dest == "":
                speak("Cannot find the requested place.")
                continue
            speak(readTemp(dest))

        elif("weather forecast" in query or 'forecast' in query):
            dest = getPlace(query)
            if dest == "":
                speak("Cannot find the requested place.")
                continue
            speak(weather_cast.WeatherForecast(dest))
            print("\nWeather forecast for 5 Days")
            weather_cast.Weather5Days(dest)

        elif("make" in query and "to do list" in query):
            speak("Making your to do list")
            makeToDoList()

        elif("read" in query or "show" in query and "to do list" in query):
            speak("Reading your to do list.")
            readToDoList()

        elif("who are you" in query):
            speak("I'm JARVIS developed by Shubham.. I'm a personal desktop assistant.")
            speak("How can I help you?")

        elif("how are you" in query):
            speak("I'm fine.. Hope you are well and good.")
            
        elif("sleep" in query):
            speak("Ok shubham. Always at your service.")
            break
