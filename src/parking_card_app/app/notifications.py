import os
import smtplib
from email.mime.text import MIMEText

class UserNotifier:
    def __init__(self, smtp_server='smtp.example.com', port=587):
        self.smtp_server = smtp_server
        self.port = port

    def send_renewal_reminder(self, user_email, card_id, expiry_date):
        msg = MIMEText(
            f"""Your parking card (ID: {card_id}) will expire on {expiry_date}.\n
            Please renew it within 30 days to avoid service interruption."""
        )
        msg['Subject'] = f'Parking Card Expiration Notice: {card_id}'
        msg['From'] = os.getenv("SMTP_USER", 'noreply@parkingsystem.com')
        msg['To'] = user_email
        
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)
