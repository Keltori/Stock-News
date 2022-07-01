import requests
import datetime
import os
from twilio.rest import Client
#### GLOBAL VARIABLES
COMPANY_NAME = "Tesla Inc"
STOCK = "TSLA"

#TIME
NOW = datetime.datetime.now()
YESTERDAY = datetime.datetime.now() - datetime.timedelta(1)
yes_day = YESTERDAY.day
yes_month = YESTERDAY.month
now_day = NOW.day
now_month = NOW.month
TIME_LIMIT = datetime.datetime.now() - datetime.timedelta(3)
TIME_LIMIT_DAY =  TIME_LIMIT.day
TIME_LIMIT_MONTH = TIME_LIMIT.month
if TIME_LIMIT_DAY < 10:
	TIME_LIMIT_DAY = f"0{TIME_LIMIT_DAY}"

if TIME_LIMIT_MONTH < 10:
	TIME_LIMIT_MONTH = f"0{TIME_LIMIT_MONTH}"

if int(now_day) < 10:
	now_day = f"0{now_day}"

if int(now_month) < 10:
	now_month = f"0{now_month}"

if int(yes_month) < 10:
	yes_month = f"0{yes_month}"

if int(yes_day) < 10:
	yes_day = f"0{yes_day}"

#API INFO

client = Client(TW_ACCOUNT_SID, TW_AUTH_TOKEN)


MORNING_PARAMETER = {"function": "TIME_SERIES_INTRADAY",
                     "interval": "1min",
                     "symbol": STOCK,
                     "apikey": STOCK_API_KEY
                     }

EVENING_PARAMETER = {"function": "TIME_SERIES_DAILY",
                     "symbol": STOCK,
                     "apikey": STOCK_API_KEY
                     }

NEWS_PARAMETER = {"q":COMPANY_NAME,
                  "from":f"{TIME_LIMIT.year}-{TIME_LIMIT_MONTH}-{TIME_LIMIT_DAY}",
                  "sortBy":"popularity",
                  "apiKey":NEWS_API_KEY
                  }

####Requests
EVENING_RESPONSE = requests.get("https://www.alphavantage.co/query", params=EVENING_PARAMETER)
close = float(EVENING_RESPONSE.json()['Time Series (Daily)'][f"{YESTERDAY.year}-{yes_month}-{yes_day}"]["4. close"])

MORNING_RESPONSE = requests.get("https://www.alphavantage.co/query", params=EVENING_PARAMETER)
open = float(MORNING_RESPONSE.json()["Time Series (Daily)"][f"{NOW.year}-{now_month}-{now_day}"]["1. open"])
MORNING_RESPONSE.json()["Time Series (Daily)"]

NEWS_RESPONSE = requests.get("https://newsapi.org/v2/everything", params= NEWS_PARAMETER)
news = NEWS_RESPONSE.json()
titles = [(news["articles"][i]["source"]["name"], i) for i in range(0,100)]
print(titles)
interesting_titles = ["Bloomberg", "BNNBloomberg.ca", "Forbes"]
selected_articles =  [title[1] for title in titles if title[0] in interesting_titles]
print(selected_articles)

news_alert = [[news["articles"][article]["title"],news["articles"][article]["url"]] for article in selected_articles]

delta = abs((open-close)/close)
if delta>0.01:
	message = f"{STOCK} growth = {round(delta,4)}!\nHere are the latest news\n"
	for item in news_alert:
		message += item[0]
		message += "\n"
		message += item[1]
		message += "\n"
message_sent = client.messages \
	.create(
	body=message,
	from_=TWILIO_NB,
	to=MY_NUMBER
)

print(message_sent.status)

####