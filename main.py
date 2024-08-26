from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from playsound import playsound
import csv
from logging import exception
from nturl2path import url2pathname
import pyttsx3 as pt
import speech_recognition as s_r
import time
import bs4
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import os
r=s_r.Recognizer()
with s_r.Microphone() as source:
 r.energy_threshold=10000
 r.adjust_for_ambient_noise(source,1.2)
 print("listening")
#audio=r.listen(source)
#text=r.recognize_google(audio)
#print(text)
 root = tk.Tk()
 root.title('Web scraping from flipkart')
 root.geometry('1080x720')
 Frame(root, width=1080, height=720, relief=RIDGE, borderwidth=5, bg='#2ef8e5').place(x=0, y=0)
 l1 = Label(root, text='Web scraping from flipkart', font=("ArialGreek 20 bold"), bg='#2ef8e5')
 l1.place(x=390, y=260)
 l2 = Label(root, text='Enter Product', font="ArialGreek 10", bg='#2ef8e5')
 l2.place(x=400, y=360)


 def listen():
   r = s_r.Recognizer()
   mic = s_r.Microphone(device_index=1)
   with mic as source:
     print("say")
     audio = r.listen(source, phrase_time_limit=5)
   text = r.recognize_google(audio).lower()
   print(text)
   return text
 v_url='http://flipkart.com'
 r = requests.get(v_url)
 page_source = r.content
 def listendata():
  t=time.localtime()
  cur=time. strftime("%H", t)
  cur=int(cur)
  engine=pt.init()
  rate=engine.getProperty('rate')
  engine.setProperty('rate', 180)
  voice=engine.getProperty('voices')
  engine.setProperty('voices', voice[0].id)
  if(cur>0 and cur<12):
    engine.say("good morning sir, welcome to webscraping project. please tell me the item name,so that i can scrap the website and produce the result.")
  elif (cur > 12 and cur < 16):
    engine.say("good afternoon sir, welcome to web scrapping project. please tell me the item name,so that i can scrap the website and produce the result.")
  else:
    engine.say("good evening sir , welcome to web scrapping project. please tell me the item name,so that i can scrap the website and produce the result.")
    engine.runAndWait()
    listdata = listen()
    product_name1.delete(1.0, 'end')
    product_name1.insert('end', listdata)
    product_name1 = Text(root, width=10, height=0, borderwidth=1, relief=RIDGE, font=('verdana',15))
    product_name1.place(x=500, y=360)
    Button(text="say", width=20, height=0, command=listendata).place(x=660, y=360)

def get_url():
        search_item = product_name1.get(1.0, 'end')
        template = "https://www.flipkart.com/search?q={}&as=on&asshow=on&otracker=AS_Query_HistoryAutoSuggest_1_4_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_4_na_na_na&as-pos=1&astype=HISTORY&suggestionId=mobile+phones&requestId=e625b409-ca2a-456a-b53c0fdb7618b658&as-backfill=on"
        search_item = search_item.replace(" ", "+")
        return template.format(search_item)
def start():
        url = get_url()
        print(type(url))
        # print(url,"\n\n\n")
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        # print(soup.prettify().translate(non_bmp_map))
        name = soup.find_all('a', class_="_1fQZEK")
        # print(len(name))
        # print(name[0].text)
        model = soup.find_all('div', class_="_4rR01T")
        # print(len(model))
        # print(model[0].text)
        rate = soup.find_all('div', class_="_3LWZlK")
        # print(rate[0].text)
        def extract(item):
          name = soup.find_all('a', class_="_1fQZEK")
          # extracting model name
          model = soup.find_all('div', class_="_4rR01T")
          model = model[item].text
          # stars
          try:
              star = soup.find_all('div', class_="_3LWZlK")
              star = star[item].text
          except IndexError:
              star = None
              # number of ratings
          try:
              num_rating = soup.find_all('span', class_='_2_R_DZ')
              num = str(num_rating[item].text)
              num = (num.split('&'))
              rating = num[0]
              # number of reviews
              num_review = num[1]
          except IndexError:
              num_review = None
              rating = None
              # specifications
          try:
              res = name[item]

              available_apps = res.find('li', {'class': "rgWa7D"}).text[0:res.find('li', {'class': "rgWa7D"}).text.find(' ')]
          except IndexError:
              res = None
              # features
              features = soup.find_all('ul', class_='_1xgFaf')
              feat = features[item]
              apps = feat.find_all('li', class_='rgWa7D')
              # system apps
          try:
              sys_apps = apps[0].t
              sys_apps = apps[0].text
          except IndexError:
              sys_apps = None
              # operating system
          try:
              os = apps[1].text
          except IndexError:
              os = None
              # display

          try:

             display = apps[2].text
          except IndexError:
             display = None
             # speaker
          try:
              speaker = apps[3].text
          except IndexError:
              speaker = None

              # refresh rate
          try:
              ref_rate = apps[4].text
          except IndexError:
              ref_rate = None
              # modes
          try:
              modes = apps[5].text
          except IndexError:
              modes = None
              # warranty
              warranty = apps[-1].text
              # price
              price = soup.find_all('div', class_='_30jeq3 _1_WHN1')
              price = price[item].text
              result = (model, star, rating, num_review, sys_apps, os, display, speaker, ref_rate, modes, warranty, price)
              return result

        def extract_phone_model_info(item):
              """ This function extracts model, price, ram, storage, stars , number of ratings, number of reviews, storage expandable option, display option, camera quality, battery , processor, warranty of a phone model at flipkart"""
              # Extracting the model of the phone from the 1st card
              model = item.find('div', {'class': "_4rR01T"}).text
              # Extracting Stars from 1st card
              star = item.find('div', {'class': "_3LWZlK"}).text
              # Extracting Number of Ratings from 1st card
              num_ratings = item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ")[0:item.find('span',{'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ").find(';')].strip()
              # Extracting Number of Reviews from 1st card
              reviews = item.find('span', {'class': "_2_R_DZ"}).text.replace('\xa0&\xa0', " ; ")[item.find('span',{'class':"_2_R_DZ"}).text.replace('\xa0&\xa0'," ; ").find(';')+1:].strip()
              # Extracting RAM from the 1st card
              ram = item.find('li',{'class':"rgWa7D"}).text[0:item.find('li',{'class':"rgWa7D"}).text.find(' ')]
              # Extracting Storage/ROM from 1st card
              storage = item.find('li',{'class':"rgWa7D"}).text[item.find('li',{'class':"rgWa7D"}).text.find(' ')+1:][0:10].strip()
              # Extracting whether there is an option of expanding the storage or not
              expandable = item.find('li',{'class':"rgWa7D"}).text[item.find('li',{'class':"rgWa7D"}).text.find('|')+1:][13:]
              # Extracting the display option from the 1st card
              display = item.find_all('li')[1].text.strip()
              # Extracting camera options from the 1st card
              camera = item.find_all('li')[2].text.strip()
              # Extracting the battery option from the 1st card
              battery = item.find_all('li')[3].text
              # Extracting the processor option from the 1st card
              processor = item.find_all('li')[4].text.strip()
              # Extracting Warranty from the 1st card
              warranty = item.find_all('li')[-1].text.strip()
              # Extracting price of the model from the 1st card
              price = item.find('div', {'class': '_30jeq3 _1_WHN1'}).text
              result = (model, star, num_ratings, reviews, ram, storage, expandable, display, camera, battery, processor, warranty, price)
              return result
              records_list = []
              results = soup.find_all('a', class_="_1fQZEK")
              item = len(results)
              for i in range(item):
                records_list.append(extract(i))
              pd.DataFrame(records_list, columns=['model', 'star', 'number of ratings', 'number of reviews','system apps','operating system','display','speaker','refreshrate','modes','warranty','price'])
              with open('Flipkart_results.csv', 'w', newline='', encoding='utf-8') as f:
                  writer = csv.writer(f)
                  writer.writerow(['model', 'star', 'number of ratings', 'number of reviews', 'system apps','operating system','display','speaker','refresh rate','modes','warranty','price'])
                  writer.writerows(records_list)
              scraped = pd.read_csv("Flipkart_results.csv")
              print(scraped.tail())

def openf():a
os.startfile("C:\\Users\\sitharam\\PycharmProjects\\p1\\Flipkart_results.csv")
enterbut = Button(text="Enter", width=20, height=0, command=start)
enterbut.place(x=550, y=400)
Button(text="Open File", width=20, height=0, command=openf).place(x=550, y=500)
root.mainloop()
