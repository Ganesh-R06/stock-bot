import os
import requests
from smtplib import SMTP
from email.message import EmailMessage

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_API_KEY = os.environ["ALPHAVANTAGE_API_KEY"]
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_API_KEY = os.environ["NEWS_API_KEY"]

stock_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameter)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_date = yesterday_data["4. close"]

day_before_yesterday = data_list[1]
day_before_yesterday_closing_date = day_before_yesterday["4. close"]

difference = float(yesterday_closing_date) - float(day_before_yesterday_closing_date)
up_down = None

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_difference = round(
    (difference / float(day_before_yesterday_closing_date)) * 100
)

if abs(percentage_difference) > 1:

    news_parameter = {
        "apikey": news_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(
        NEWS_ENDPOINT,
        params=news_parameter
    )
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]

    
    three_article = news_data[:3]

    formatted_article = [
        f"{STOCK_NAME}: {up_down}{percentage_difference} %\n"
        f"Headline:{article['title']}.\n"
        f"Brief:{article['description']}"
        for article in three_article
    ]

    for article in formatted_article:
        myemail = os.environ["EMAIL_ADDRESS"]
        passw1 = os.environ["EMAIL_PASSWORD"]

        msg = EmailMessage()
        msg["Subject"] = "Stock Market Alert 📈"
        msg["From"] = myemail
        msg["To"] = os.environ["TO_EMAIL"]

        msg.set_content(article)

        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(
                user=myemail,
                password=passw1
            )
            connection.send_message(msg)

        print("Message sent!")


