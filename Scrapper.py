# TrackAzon
# Powered by KENOH

import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime
import time

URL = 'https://www.amazon.de/MWP22ZM-A-Apple-AirPods-Pro/dp/B07ZPML7NP/ref=sr_1_1_sspa?dchild=1&keywords=airpods+pro&qid=1629404730&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQlk3MDFETUdIMjhVJmVuY3J5cHRlZElkPUEwMDAzNjg1M0dSM09RTU9HQlA0QyZlbmNyeXB0ZWRBZElkPUEwMjkzODc2QzFKTVRZVUxMSjRQJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}


# def getInfo():
#     # URL = input('Input the link to the product you would like to track \n')
#     email = input('Please enter your email\n')
#
#     return email


# receiverEmail = getInfo()
# URL = response[0]

def getTitle():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').get_text()
    return title.strip()


def getPrice():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find(id='priceblock_ourprice').get_text()
    converted_price = float(price[0:5].replace(',', '.'))
    return converted_price


def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def getDate():
    date = datetime.now().date()
    return date


def priceCheck():
    ## improve this function as the code is being reused here
    f = open('logs.txt', 'r')
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='priceblock_ourprice').get_text()
    print(price)
    converted_price = float(price[0:5].replace(',', '.'))

# --------------------------------------------------------------

    readPrice = 0.0
    for line in f:
        line = line[17:]

        try:
            readPrice = float(line)
            break
        except:
            continue
    f.close()
    print(readPrice, 'Read Price')
    print(converted_price, 'Converted Price')

    if converted_price != readPrice:  # if the cost is lower than our old cost
        nf = open('logs.txt', 'a')
        nf.write('Title: ' + title.strip() + '\n  Current Price: ' + str(
            converted_price).strip() + '\n logged at ' + getTime() + '\n')
        nf.close()
        send_mailGood()
    elif converted_price == readPrice:
        # no change
        send_mailNoChnage()


def send_mailGood():
    # receiverEmail = getInfo()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('dummymagician22@gmail.com', 'itewskcoplhsmjyg')
    subject = 'PRICE CHANGE ' + getTitle() + '!  ' + str(getPrice()) + 'EUR at ' + str(getDate())
    body = 'CURRENT PRICE IS NOW ' + str(
        getPrice()) + 'EUR as of ' + getTime() + ' ' + str(
        getDate()) + '\nCheck the the product linked below for details! \n\n' + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'dummymagician22@gmail.com',
        '1Karimulmann@gmail.com',
        msg
    )
    print('email sent!')
    print(msg)          # find whats the problem with this!
    server.quit()


def send_mailNoChnage():
    # receiverEmail = getInfo()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('dummymagician22@gmail.com', 'itewskcoplhsmjyg')
    subject = 'No change on ' + getTitle() + '!  ' + str(getPrice()) + 'EUR at ' + str(getDate())
    body = 'Price remains at ' + str(
        getPrice()) + 'EUR as of ' + getTime() + ' ' + str(
        getDate()) + '\nCheck the the product linked below for details! \n\n' + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'dummymagician22@gmail.com',
        '1Karimulmann@gmail.com',
        msg
    )
    print('email sent!')
    server.quit()


while True:
    priceCheck()
    time.sleep(86400)
