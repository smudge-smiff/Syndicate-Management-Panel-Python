import smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr
import threading

class mymail:
    toEmail = None
    msg = None
    subject = None
    mailSendThread=None

    def __init__(self):
        self.mailSendThread = threading.Thread(target=self.sendAsync, args=())

    def setToEmail(self, email):
        self.toEmail = email

    def setMessage(self, message):
        self.msg = message

    def setSubject(self, subject):
        self.subject = subject
    
    def send(self):
        self.mailSendThread.start()

    def sendAsync(self):
        port = 465  # For SSL
        password = ""
        sender_email = ""
        receiver_email = self.toEmail
        message = MIMEText(self.msg)
        message['Subject'] = self.subject;
        message['From'] = formataddr(('', sender_email))
        message['To'] = self.toEmail

        server = smtplib.SMTP_SSL("mail.privateemail.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, [receiver_email], message.as_string())
        server.quit()
        print("Email send", flush=True)
