import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "megharanjanir@gmail.com"
SENDER_PASSWORD = "wgoe vxpo pbbl ravh"
RECEIVER_EMAIL = "rudhramegha9506@gmail.com"


def send_email(subject, message):

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        print("[EMAIL] Sent successfully")

    except Exception as e:
        print("[EMAIL ERROR]", e)