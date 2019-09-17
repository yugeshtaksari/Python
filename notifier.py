import requests
from bs4 import BeautifulSoup # can parse the information we got from the site
import smtplib
import time


URL = 'https://finance.yahoo.com/quote/AMZN/'
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

class Count:
    n = 1


count = Count()

def check_price():
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find('h1', attrs={'class':'D(ib) Fz(18px)'}).text
    price = soup2.find('span', attrs = {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    title = title.strip()
    converted_price = float(price.strip().replace(',',''))

    print(title.strip())
    print(converted_price)

    if (converted_price > 59):
        send_email(converted_price)


def send_email(cost):

    server = smtplib.SMTP('smtp.mail.yahoo.com', 587) # your email in use to send notification
    server.ehlo() #ehlo is a command sent by an email to identify itself to another  email
    server.starttls() # encrypt
    server.ehlo()

    server.login('xxxxxxxxxxxxxx','xxxxxxxxxxxxxx') # your email and app password (email, passowrd)

    subject = "PRICE Drop Notification " + str(count.n)

    count.n += 1

    body = "Hi ! Updated Price is " + str(cost) + "\nKeep Smiling"

    msg = "Subject: " + subject + "\n\n" + body
    #msg = body

    server.sendmail('Sendersemail@email.com',
                    'receiversemai@gmail.com',
                    msg)
  
    print("Email has been sent")
    server.quit()


while(True):
    check_price()
    time.sleep(60) # for every 2 minute
