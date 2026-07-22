import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.schemas.contact import ContactCreate

logger = logging.getLogger(__name__)

class SMTPService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.is_configured = all([self.username, self.password, self.from_email])

    async def send_contact_notification(self, contact: ContactCreate) -> bool:
        if not self.is_configured:
            logger.warning("SMTP not configured, skipping notification")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.from_email
            msg['Subject'] = f"Новое сообщение: {contact.subject}"
            
            body = f"""
            <html>
            <body>
                <h2>Новое сообщение с формы обратной связи</h2>
                <p><strong>Имя:</strong> {contact.name}</p>
                <p><strong>Email:</strong> {contact.email}</p>
                <p><strong>Тема:</strong> {contact.subject}</p>
                <p><strong>Сообщение:</strong></p>
                <p>{contact.message}</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Notification sent for contact: {contact.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False

smtp_service = SMTPService()
