#Ref: https://github.com/NijatZeynalov/Scraper-Chatbot?tab=readme-ov-file 
#
# REMEMBER to pip install everything below from the terminal
# pip install pyttsx3 SpeechRecognition datetime wikipedia requests bs4 google-api-python-client oauth2client httplib2 googletrans

import pyttsx3
import speech_recognition
import datetime
import wikipedia
import webbrowser
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import random
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from googletrans import Translator

translator = Translator(service_urls=['translate.google.com','https://www.deepl.com/en/translator',])

b="Spartan: "
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def get_news():
    
    try:
        # Construct the API request URL with my API key
        url = f'https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=rFeYWmi9G3zSxcsv9dTnFlIJGtDPjFEv'
        response = requests.get(url)
        stories = response.json().get('results', [])[:3]  # Fetches top 3 news stories from the specified section
        
        if not stories:
            print(b, "I couldn't find any news stories.")
            speak("I couldn't find any news stories.")
            return

        for i, story in enumerate(stories, 1):
            # Each story's title and a brief summary (abstract) is printed
            print(b, f"News {i}: {story['title']}. Summary: {story['abstract']}")
            speak(f"News {i}: {story['title']}.")
    except Exception as e:
        print(b, "Sorry, I couldn't fetch the news from The New York Times.")
        speak("Sorry, I couldn't fetch the news from The New York Times.")


def open_file():
    print(b, "Which file or application would you like to open?")
    speak("Which file or application would you like to open?")
    path = input("EE104: Enter the file path or application name: ")
    try:
        os.startfile(path)
        print(b, f"Opening {path}...")
        speak(f"Opening {path}...")
    except Exception as e:
        print(b, "Sorry, I couldn't open the file or application.")
        speak("Sorry, I couldn't open the file or application.")

def translate_text():
    print(b, "What text do you want to translate, and to what language?")
    speak("What text do you want to translate, and to what language?")
    text = input("EE104: Text to translate: ")
    lang = input("EE104: Target language (e.g., 'fr' for French): ")
    try:
        translation = translator.translate(text, dest=lang)
        print(b, f"Translation: {translation.text}")
        speak(f"Translation: {translation.text}")
    except Exception as e:
        print(b, "Sorry, I couldn't perform the translation.")
        speak("Sorry, I couldn't perform the translation.")


def speak(text):
    engine.say(text)
    engine.runAndWait()

def greetings():
    h=int(datetime.datetime.now().hour)
    if h>8 and h<12:
        print(b,'Good Morning. My name is Spartan. Version 1.00')
        speak('Good morning. My name is Spartan. Version 1.00')
    elif h>=12 and h<17:
        print(b,"Good afternoon. My name is Spartan. Version 1.00")
        speak('Good afternoon. My name is Spartan. Version 1.00')
    else:
        print(b,'Good evening! My name is Spartan. Version 1.00')
        speak('Good evening My name is Spartan. Version 1.00')
    print(b,'How can I help you, EE104?')
    speak('How can I help you, EE104?')

motiv=["Sometimes later becomes never. Do it now. EE104, I believe you, you have made me."]
need_list=['EE104, what can I do for you?', 'Do you want something else?', 'EE104, give me questions or tasks', 'I want to take time with you, do you want to know something else?','EE104, what is on your mind?', 'I can not think like you-humans, but can give answer your all questions',"Let's discover this world! What do you want to learn today?" ]
sorry_list=['EE104, I am sorry I dont know the answer', 'I dont have an idea about it, EE104','Sorry, EE104! try again']
bye_list=['Good bye, EE104. I will miss you','See you EE104','Bye, dont forget I will always be here']
comic_list=['It is not a joke, EE104. I was serious','Do you think that it is a joke? Be nice!']
greet_list=['Hi EE104', 'Hi my dear']


# https://www.geeksforgeeks.org/how-to-extract-weather-data-from-google-in-python/ 
def weather_Spartan(city):
    import requests
    from bs4 import BeautifulSoup

    city=city.replace('weather','')

    try:

        # creating url and requests instance
        url = "https://www.google.com/search?q="+"weather"+city
        html = requests.get(url).content

        # getting raw data
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        # formatting data
        data = str.split('\n')
        time = data[0]
        sky = data[1]

        # getting all div tag
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text

        # getting other required data
        pos = strd.find('Wind')
        other_data = strd[pos:]

        # printing all data
        print("At ", city)
        print("Temperature is", temp)
        print("Time: ", time)
        print("Sky Description: ", sky)
        print(other_data)



    except:
        sorry=random.choice(sorry_list)
        print(b, sorry)
        speak(sorry)



def takeCommand():
    while True:
        print(" ")
        query=input("EE104: ")
        if 'who is' in query.lower():
            try:
                query=query.replace('who is','')
                result=wikipedia.summary(query, sentences=2)  #see more here https://www.geeksforgeeks.org/wikipedia-module-in-python/ 
                print(b,result)
                speak(result)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
        elif 'hello'==query:
            greet=random.choice(greet_list)
            print(b, greet)
            speak(greet)
            
        elif 'play' in query.lower():
            query=query.replace('play','')
            url='https://www.youtube.com/results?search_query='+query
            webbrowser.open(url)
            time.sleep(2)
            speak('There are a lot of music, select one.')
            time.sleep(3)
            need=random.choice(need_list)
            print(b, need)
            speak(need)
        elif query=='exit' or query=="bye":
            bye=random.choice(bye_list)
            print(b, bye)
            speak(bye)
            break
        elif 'haha' in query:
            comic=random.choice(comic_list)
            print(b, comic)
            speak(comic)
        elif 'motivate' in query:
            print(b, motiv)
            speak(motiv)
        elif 'facebook' in query:
            url2='https://www.facebook.com/friends/requests/?fcref=jwl'
            webbrowser.open(url2)
        elif 'weather' in query.lower():
            weather_Spartan(query)
            need=random.choice(need_list)
            print(b, need)
            speak(need)
        elif 'translate' in query:
            translate_text()  # Call your translation function here
        
        elif 'open file' in query or 'start application' in query:
            open_file()  # Call your file/application opening function here
        
        elif 'news' in query or 'give me the news' in query:
                get_news()  # Call your news fetching function here
        elif 'shutdown laptop' in query.lower():
            os.system("shutdown /s /t 1");
        elif 'what is' in query.lower():
            try:
                query=query.replace('what is','')
                result=wikipedia.summary(query, sentences=2)  #see more here https://www.geeksforgeeks.org/wikipedia-module-in-python/ 
                print(b,result)
                speak(result)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
            # Check if the query contains any of the specified words
        elif any(word in query for word in ["when", "how", "is", "are"]):
            # Remove specific question-related words from the query to clean it for the search
            query = query.replace('when', '')
            query = query.replace('how', '')
            query = query.replace('who', '')
            query = query.replace('is', '')
            query = query.replace('are', '')
        
            # Send a GET request to a Yahoo search page with the cleaned query
            page2 = requests.get("https://search.yahoo.com/search;_ylt=AwrOqlzV2QFmRC05hTpDDWVH;_ylc=X1MDMTE5NzgwNDg2NwRfcgMyBGZyAwRmcjIDcDpzLHY6c2ZwLG06c2Esc2FfbWs6MTMEZ3ByaWQDUHVRUDZTT09URU93TEEuVEpVV0Y1QQRuX3JzbHQDMARuX3N1Z2cDMTAEb3JpZ2luA3NlYXJjaC55YWhvby5jb20EcG9zAzEEcHFzdHIDZ2UEcHFzdHJsAzIEcXN0cmwDMTcEcXVlcnkDZ2VvcmdlJTIwd2FzaGluZ3RvbgR0X3N0bXADMTcxMTM5NzM1NAR1c2VfY2FzZQM-?p={search}&fr=sfp&fr2=p%3As%2Cv%3Asfp%2Cm%3Asa%2Csa_mk%3A13&iscqry=&mkr=13", query)
            
            # Parse the HTML content of the page
            soup = BeautifulSoup(page2.content, "html.parser")
            
            # Find the first div element that matches the class (looking for a specific container that holds the links to answers)
            name = soup.find("div", {"class": "dd fst lst algo algo-sr relsrch richAlgo"})
            
            try:
                # Look for all 'a' elements within 'name' that have a href attribute matching a Yahoo Answers question link
                for link in name.findAll('a', attrs={'href': re.compile("^https://answers.yahoo.com/question")}):
                    a = (link.get('href'))  # Extract the href value (URL) from the link
                
                # Send a GET request to the first Yahoo Answers question link found
                page1 = requests.get(a)
                
                # Parse the HTML content of the Yahoo Answers page
                soup = BeautifulSoup(page1.content, "html.parser")
                
                # Find the div element that contains the answers, then clean and split the text to prepare for speaking/reading
                name = soup.find("div", {"class": "AnswersList__container___3vQdv"}).text.replace("\n", "").strip()
                temp = name.rsplit("Favorite Answer", 1)
                temp = temp[1].split('.')
                
                # Read out the first two sentences of the favorite answer
                for i in temp[:2]:
                    print(b, i)
                    speak(i)
                
                # Randomly select a follow-up message from 'need_list' and present it to the user
                need = random.choice(need_list)
                print(b, need)
                speak(need)
            except Exception as e:
                # If any error occurs (e.g., element not found, network issue), inform the user
                sorry = random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
        
                
time.sleep(.5)
print('Initializing...')
time.sleep(.5)
print('Spartan is preparing...')
time.sleep(.5)
print('Environment is building...')
time.sleep(.5)
greetings()
takeCommand()
  
