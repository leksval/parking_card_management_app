import smtplib
from email.mime.text import MIMEText
from .models import User
from .database import DatabaseHandler

class UserNotifier:
    def __init__(self, smtp_server='smtp.example.com', port=587):
        self.smtp_server = smtp_server
        self.port = port

    def send_renewal_reminder(self, user_email):
        msg = MIMEText("Please renew your parking card")
        msg['Subject'] = 'Parking Card Renewal'
        msg['From'] = 'noreply@parkingsystem.com'
        msg['To'] = user_email
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.send_message(msg)
