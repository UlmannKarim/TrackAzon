# TrackAzon
# Powered by KENOH

import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime
import time
import os
from dotenv import load_dotenv


# URL = 'https://www.amazon.de/MWP22ZM-A-Apple-AirPods-Pro/dp/B07ZPML7NP/ref=sr_1_1_sspa?dchild=1&keywords=airpods+pro&qid=1629404730&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQlk3MDFETUdIMjhVJmVuY3J5cHRlZElkPUEwMDAzNjg1M0dSM09RTU9HQlA0QyZlbmNyeXB0ZWRBZElkPUEwMjkzODc2QzFKTVRZVUxMSjRQJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
# headers = {
#         "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}


class WebParser:

    load_dotenv()
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    def __init__(self, URL, emailReceiver):
        self._URL = URL
        self._emailReceiver = emailReceiver

    def getEmailReceiver(self):
        return self._emailReceiver

    def getURL(self):
        return self._URL


    def getTitle(self):
        page = requests.get(self.getURL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id='productTitle').get_text()
        return title.strip()


    def getPrice(self):
        page = requests.get(self.getURL(), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        price = soup.find(id='priceblock_ourprice').get_text()
        converted_price = float(price[0:5].replace(',', '.'))
        return converted_price


    def getTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time


    def getDate(self):
        date = datetime.now().date()
        return date


    def priceCheck(self):
        f = open('logs.txt', 'r')
        title = getTitle()
        price = getPrice()
        print(price)

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
        print(price, 'Converted Price')

        if price != readPrice:  # if the cost is lower than our old cost
            nf = open('logs.txt', 'a')
            nf.write('Title: ' + title.strip() + '\n  Current Price: ' + str(
                price).strip() + '\n logged at ' + getTime() + '\n \n')
            nf.close()
            self.compose_positive_mail()
        elif price == readPrice:
            # no change
            self.compose_negative_mail()


    def senderLogin(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(SENDER_EMAIL, SENDER_PASSWORD)

    def sendMail(self, subject, body,recepient):
        self.senderLogin()
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(
            SENDER_EMAIL,
            recepient,
            msg
        )
        server.quit()

    def compose_positive_mail(self):

        self.senderLogin()

        subject = 'PRICE CHANGE ' + getTitle() + '!  ' + str(getPrice()) + 'EUR at ' + str(getDate())
        body = 'CURRENT PRICE IS NOW ' + str(
            getPrice()) + 'EUR as of ' + getTime() + ' ' + str(
            getDate()) + '\nCheck the the product linked below for details! \n\n' + URL

        self.sendMail(subject,body,self.getEmailReceiver())


    def compose_negative_mail(self):

        self.senderLogin()

        subject = 'No change on ' + getTitle() + '!  ' + str(getPrice()) + 'EUR at ' + str(getDate())
        body = 'Price remains at ' + str(
            getPrice()) + 'EUR as of ' + getTime() + ' ' + str(
            getDate()) + '\nCheck the the product linked below for details! \n\n' + URL

        self.sendMail(subject, body, self.getEmailReceiver())



    # while True:
    #     priceCheck()
    #     time.sleep(86400)

# enums
# hold sensitive vars in a .properties file like in java
# class around this file
# body of request, name of item
# API will search


# talk about what i worked on in internship
# cleaning up this project
# screenshots last resort show code

# talk a lot about EMBL, docker kubernetes, web dev vaadin springbooth

# what does Ericsson do?
# why wanna work for them.
# interested in their work and technologies, how its improving the future
# 5g
# I would love to work for a company which contributes to improving people's lives
# 5G remote surgery.
# i saw an example of this surgery carreid out over 5G, how about the future? I want to be part of it,
# that's why i want to join Ericsson.
# what is cloud native?
# full stack application in the cloud high availability of application because of cloud native 0 down time
# easier to scale in the cloud
# easier to automate

# microservices way to develop application, each function is a microservice.
# Slicing pieces of the application into own container. usally each container is a docker image
# k8's manage the containers
# manage and stored by cloud native

# plan to make it an API more dynamic rather than static at the moment
# willing to learn, any new technologies
# prefer bak end due to placement but open to the possibility of exploring more into front end

