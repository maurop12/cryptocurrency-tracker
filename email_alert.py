import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL, API_KEY
import requests

def send_email_alert(subject, body, to_email=TO_EMAIL):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print('Email sent!')
    except Exception as e:
        print(f'Error sending email: {e}')

def check_price_alert(symbol, threshold):
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"https://rest.coincap.io/v3/assets/{symbol}", headers=headers)
        response.raise_for_status()
        price = float(response.json()['data']['priceUsd'])
        if price > threshold:
            subject = f"ALERT: {symbol.upper()} price has crossed {threshold}$"
            body = f"Current price for {symbol.upper()} is ${price:.2f} (threshold: {threshold}$)"
            send_email_alert(subject, body, TO_EMAIL)
    except Exception as e:
        print(f"Error checking price alert: {e}")