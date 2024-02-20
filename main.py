import requests
from twilio.rest import Client
STOCK_NAME= "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "8375FIQXUVSX2TY7"
NEWS_API_KEY = "f600c685ba2d4025901b852a60a703df"
STOCK_END_POINT = "https://www.alphavantage.co/query"
NEWS_END_POINT = "https://newsapi.org/v2/everything"

TWILIO_SID = "AC85929387276a310d7b4564179d3b8994"
TWILIO_AUTH_TOKEN = "89df744c16e5967d20307e707e7698bd"
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY

}

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(STOCK_END_POINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
before_yesterday_data = data_list[1]
before_yesterday_closing_price = before_yesterday_data["4. close"]
difference = float(yesterday_closing_price) - float(before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percent = round(difference/  float(yesterday_closing_price) * 100,1)
if diff_percent < 5:
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    response = requests.get(NEWS_END_POINT, params=news_params)
    response.raise_for_status()
    articles = response.json()["articles"]
    three_articles = articles[:3]
    formated_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {articles['title']}, \nBrief: {articles['description']}" for articles in three_articles]
    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formated_articles:
        message = client.messages.create(
            body=article,
            from_="+16592465627",
            to="+918091766903"
        )


#Optional: Format the SMS message like
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5% 
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
