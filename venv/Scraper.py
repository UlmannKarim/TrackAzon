# TrackAzon
import ssl

import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime
import time
import os
from dotenv import load_dotenv


class TrackAzon:


    def __init__(self, URL, emailReceiver):
        self._SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
        self._SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
        self._em = EmailMessage()

        self._URL = URL
        self._emailReceiver = emailReceiver
        self._headers = {
            "User-Agent":
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

    def getSENDER_EMAIL(self):
        return self._SENDER_EMAIL

    def getSENDER_PASSWORD(self):
        return self._SENDER_PASSWORD

    def getEmailReceiver(self):
        return self._emailReceiver

    def getHeaders(self):
        return self._headers

    def getURL(self):
        return self._URL


    def getTitle(self):
        page = requests.get(self.getURL(), headers=self.getHeaders())
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id='productTitle').get_text()
        return title.strip()


    def getPrice(self):
        page = requests.get(self.getURL(), headers=self.getHeaders())
        soup = BeautifulSoup(page.content, 'html.parser')
        targetDiv = soup.find(id='attach-base-product-price')['value']

        return targetDiv


    def getTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return str(current_time)


    def getDate(self):
        date = datetime.now().date()
        return str(date)


    def priceCheck(self):
        # f = open('logs.txt', 'r')
        # title = getTitle()
        # price = getPrice()
        # print(price)

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
            self.postiveOutcome()
        elif price == readPrice:
            # no change
            self.negativeOutcome()


    # def senderLogin(self):
    #     # server = smtplib.SMTP('smtp.gmail.com', 587)
    #     # server.ehlo()
    #     # server.starttls()
    #     # server.ehlo()
    #     # return server
    #     context = ssl.create_default_context()
    #     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    #         smtp.login(self._SENDER_EMAIL, self._SENDER_PASSWORD)
    #         return smtp


        #server.login(self._SENDER_EMAIL, self._SENDER_PASSWORD)

    def composeEmail(self, template):
        with open(template) as temp:
            contents = temp.read()

            modifiedContents = contents.replace("%TITLE%", self.getTitle())
            modifiedContents = modifiedContents.replace("%PRICE%", self.getPrice())
            modifiedContents = modifiedContents.replace("%DATE%", self.getDate())
            modifiedContents = modifiedContents.replace("%TIME%", self.getTime())
            modifiedContents = modifiedContents.replace("%URL%", self.getURL())

            subject = modifiedContents.split('-----')[0]
            body = modifiedContents.split('-----')[1]

            return subject,body

    # def sendMail(self, subject, body,recepient, smtp):
        # server = self.senderLogin()
        # msg = f"Subject: {subject}\n\n{body}"
        # server.sendmail(
        #     self._SENDER_EMAIL,
        #     recepient,
        #     msg
        # )
        # server.quit()

        #smtp = self.senderLogin()
        # self._em['From'] = self._SENDER_EMAIL
        # self._em['To'] = self._emailReceiver
        # self._em['Subject'] = subject
        # self._em.set_content(body)
        # smtp.sendmail(self._SENDER_EMAIL, self._emailReceiver, self._em.as_string())
        # smtp.quit()



    def postiveOutcome(self):

        # smtp = self.senderLogin()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self._SENDER_EMAIL, self._SENDER_PASSWORD)
            mail = self.composeEmail("venv/Templates/positiveMail")

            self._em['From'] = self._SENDER_EMAIL
            self._em['To'] = self._emailReceiver
            self._em['Subject'] = mail[0]
            self._em.set_content(mail[1])
            smtp.sendmail(self._SENDER_EMAIL, self._emailReceiver, self._em.as_string())
            smtp.quit()

        #     context = ssl.create_default_context()
        #     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        #         smtp.login(self._SENDER_EMAIL, self._SENDER_PASSWORD)


    def negativeOutcome(self):

        self.senderLogin()
        self.composeEmail("venv/Templates/negativeMail")
        self.sendMail(subject, body, self.getEmailReceiver())

    # while True:
    #     priceCheck()
    #     time.sleep(86400)