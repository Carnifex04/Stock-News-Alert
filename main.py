import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = "YBDK7TU0AAWLDXX4"
NEWS_API = "a973819fe5ba4950a70ea9f9464d7ef5"
ACCOUNT_SID = "AC17eeb730a355831240d5fea5497854eb"
AUTH_TOKEN = "53e8124c7ed5e253f9912255ce5a2db4"

INCREASE = "🔺"
DECREASE = "🔻"


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

def change(stocks):
    return round((float(stocks[0]) - float(stocks[1])) / float(stocks[0]) * 100, 2)


def send_update(news, fluctuation):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for data in news:
        message = client.messages.create(
            body=f"{STOCK}: {INCREASE if fluctuation >= 5 else DECREASE}{fluctuation}%\n"
                 f"Headline: {data['title']}\nBrief: {data['description']}",
            from_='+15073386265',
            to='+918699578106'
        )
        print(message.status)


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API
}

stock_response = requests.get(url="https://www.alphavantage.co/query?", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [details["4. close"] for date, details in stock_data.items()][:2]

if change(stock_data_list) >= 5 or change(stock_data_list) <= 5:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything?", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    news_data_list = [{"title": details["title"],
                       "description": details["description"]} for details in news_data]

    send_update(news_data_list, change(stock_data_list))

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
