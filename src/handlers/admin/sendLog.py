import smtplib
from email.message import EmailMessage
from src.settings.config import *

def sendLog(timestamp, error):
    email = EmailMessage()
    email['Subject'] = 'ChatGPT Log'
    email['From'] = EMAIL_ADDRESS
    email['To'] = TO_EMAIL_ADRESS
    email.set_content(f'''
    <!DOCTYPE html>
    <html>
        <body>
            <div style="text-align: center;">
                <h1 style="font-family: 'Lato', sans-serif;color#454349;">An error was occured ‼️</h1>
                <p style="font-family: 'Lato', sans-serif;color#39383b;"><italik>Solve it as soon as possible</italik></p>
                <h4 style="text-align: left;">🕐 Timestamp: <code>{timestamp}</code></h4>
                <h4 style="text-align: left;">🪲 Error description: <code>{error}</code></h4>
                <h4 style="text-align: left;">💡 Possible solution: <code>{solution}</code></h4>
            </div>
        </body>
    </html>
    ''', subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
        smtp.send_message(email)