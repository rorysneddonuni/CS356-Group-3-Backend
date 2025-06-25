import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import email_conf


class EmailService:
    @staticmethod
    def send_reset_password_email(to_email: str, reset_link: str):
        subject = "Your Password Reset Request"
        body = f"""
        <p>Hello,</p>
        <p>You requested a password reset. Click the link below to reset your password:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>If you didn't request this, you can safely ignore this email.</p>
        <br>
        <p>– {email_conf.EMAIL_FROM_NAME}</p>
        """

        EmailService._send_email(to_email, subject, body)

    @staticmethod
    def _send_email(to_email: str, subject: str, html_body: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{email_conf.EMAIL_FROM_NAME} <{email_conf.EMAIL_FROM}>"
        message["To"] = to_email

        part = MIMEText(html_body, "html")
        message.attach(part)

        try:
            with smtplib.SMTP(email_conf.SMTP_SERVER, email_conf.SMTP_PORT) as server:
                server.starttls()
                server.login(email_conf.SMTP_USERNAME, email_conf.SMTP_PASSWORD)
                server.sendmail(email_conf.EMAIL_FROM, to_email, message.as_string())
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")
