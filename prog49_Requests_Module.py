# Requests Module For HTTP Requests 
# Your API key is: d48128f52a774428a589dcab2548c687

import requests

r = requests.get("https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=d48128f52a774428a589dcab2548c687")

print(r.status_code)
mydata = r.text
news_title = mydata.split(",")[5]
print(news_title)


