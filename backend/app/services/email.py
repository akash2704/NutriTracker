import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_username)
        
    def send_otp_email(self, to_email: str, otp: str, first_name: str) -> bool:
        """Send OTP verification email"""
        if not all([self.smtp_username, self.smtp_password]):
            print(f"SMTP not configured. OTP for {to_email}: {otp}")
            return True  # Return True for development
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = "Verify Your NutriTracker Account"
            
            body = f"""
            Hi {first_name},
            
            Welcome to NutriTracker! Please verify your account using the OTP below:
            
            Your OTP: {otp}
            
            This OTP will expire in 10 minutes.
            
            Best regards,
            NutriTracker Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

email_service = EmailService()
