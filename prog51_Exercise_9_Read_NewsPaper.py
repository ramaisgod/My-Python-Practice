# Exercise 9: Akhbaar Padhke Sunaao

import requests
import json
apikey = "d48128f52a774428a589dcab2548c687"

def speak_my_text(mytext):
    from win32com.client import Dispatch
    mystring = Dispatch("SAPI.SpVoice")
    mystring.Speak(mytext)

news_data = requests.get("https://newsapi.org/v2/sources?apiKey=" + apikey)
#print(news_data.text)
news = json.loads(news_data.text)
news_source = news['sources']
#--- List of country -----
s = set()
l = set()
c = set()
n = set()
for source in news_source:
    s.add(source['country'])
    l.add(source['language'])
    c.add(source['category'])
    n.add(source['name'])

country_list = [i for i in s]
language_list = [i for i in l]
category_list = [i for i in c]
news_paper_list = [i for i in n]

print("Available Languages are : ")
print(language_list)
print("Select Language : ")

print("Available Countries are : ")
print(country_list)
print("Select Country : ")

print("News Category are : ")
print(category_list)
print("Select News Category : ")

# print("News Papers are : ")
# print(news_paper_list)
# print("Select News Paper : ")


print("------- Welcome to My News Channel ------------")

if __name__ == "__main__":
    for nw in news_source:
        if nw['country'] == 'us' and nw['language'] == 'en' and nw['category'] == 'general':
            print("------ Today's Headlines -------")
            headline = nw['description']
            print(headline)
            print(nw['url'])
            speak_my_text(headline)




