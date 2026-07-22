import logging
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings
from app.schemas.contact import ContactCreate

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.is_configured = all([self.username, self.password, self.from_email])
        
        if not self.is_configured:
            logger.warning("SMTP not configured in .env file")

    async def send_owner_notification(self, contact: ContactCreate) -> bool:
        if not self.is_configured:
            logger.warning("Email service not configured")
            return False

        try:
            subject = f"Новое обращение: {contact.comment[:50]}..."
            body = self._build_owner_body(contact)
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.from_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            await self._send_email(msg)
            logger.info(f"Owner notification sent for contact: {contact.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send owner notification: {e}")
            return False

    async def send_user_confirmation(self, contact: ContactCreate) -> bool:
        if not self.is_configured:
            logger.warning("Email service not configured")
            return False

        try:
            subject = "Ваше обращение получено"
            body = self._build_user_body(contact)
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = contact.email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            await self._send_email(msg)
            logger.info(f"User confirmation sent to: {contact.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send user confirmation: {e}")
            return False

    async def _send_email(self, msg: MIMEMultipart):
        try:
            await aiosmtplib.send(
                msg,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                start_tls=True
            )
        except Exception as e:
            logger.error(f"SMTP send error: {e}")
            raise

    def _build_owner_body(self, contact: ContactCreate) -> str:
        return f"""
        <html>
        <body>
            <h2>Новое обращение с формы обратной связи</h2>
            <table border="1" cellpadding="5">
                <tr><td><strong>Имя:</strong></td><td>{contact.name}</td></tr>
                <tr><td><strong>Email:</strong></td><td>{contact.email}</td></tr>
                <tr><td><strong>Телефон:</strong></td><td>{contact.phone or 'Не указан'}</td></tr>
                <tr><td><strong>Комментарий:</strong></td><td>{contact.comment}</td></tr>
            </table>
        </body>
        </html>
        """

    def _build_user_body(self, contact: ContactCreate) -> str:
        return f"""
        <html>
        <body>
            <h2>Спасибо за обращение, {contact.name}!</h2>
            <p>Мы получили ваше сообщение:</p>
            <blockquote>{contact.comment}</blockquote>
            <p>Наша команда свяжется с вами в ближайшее время.</p>
            <p>С уважением,<br>Команда поддержки</p>
        </body>
        </html>
        """

email_service = EmailService()
