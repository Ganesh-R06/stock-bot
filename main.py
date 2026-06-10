import os
import requests
from twilio.rest import Client

# Fetching hidden variables from the environment
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_API_KEY = os.environ.get("STOCK_API_KEY")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_API_KEY = os.environ.get("NEWS_API_KEY")

stock_parameter={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_API_KEY
}
response=requests.get(STOCK_ENDPOINT, params=stock_parameter)
response.raise_for_status()
data=response.json()["Time Series (Daily)"]

data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_date=yesterday_data["4. close"]

day_before_yesterday=data_list[1]
day_before_yesterday_closing_date=day_before_yesterday["4. close"]

difference=float(yesterday_closing_date)-float(day_before_yesterday_closing_date)
up_down=None
if difference>0:
    up_down="🔺"
else:
    up_down="🔻"

percentage_difference = round((difference / float(day_before_yesterday_closing_date)) * 100)
if abs(percentage_difference)>1:

    news_parameter={
        "apikey":news_API_KEY,
        "qInTitle":COMPANY_NAME
    }
    news_response=requests.get(NEWS_ENDPOINT, params=news_parameter)
    news_response.raise_for_status()
    news_data=news_response.json()["articles"]

    three_article=news_data[:4]

    formatted_article=[f"{STOCK_NAME}: {up_down}{percentage_difference} %\n Headline:{article['title']}. \n Brief:{article['description']}"for article in three_article]

    # Fetching hidden phone numbers
    TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
    MY_PHONE = os.environ.get("MY_PHONE")

    for article in formatted_article:
        message=client.messages.create(
            from_=TWILIO_PHONE,
            body=article,
            to=MY_PHONE
    )
    print("Message sent!")
