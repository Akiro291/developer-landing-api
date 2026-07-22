import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def send_email_smtp(
    host: str,
    port: int,
    username: str,
    password: str,
    from_email: str,
    to_email: str,
    subject: str,
    body: str,
    is_html: bool = False
) -> bool:
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        mime_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, mime_type))
        
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
