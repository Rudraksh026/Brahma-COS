import os
import smtplib
from email.message import EmailMessage


def send_email(to: str, subject: str, body: str) -> bool:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM") or username
    if not all([host, username, password, sender]):
        print(f"[SMTP] Not configured; skipped email to {to}: {subject}")
        return False
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(username, password)
            smtp.send_message(msg)
        return True
    except Exception as exc:
        print(f"[SMTP] Failed: {exc}")
        return False


def send_verification_email(email: str, name: str, token: str) -> bool:
    base = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000").rstrip("/")
    return send_email(email, "Verify your BRAHMA COS account", f"Hi {name},\n\nVerify your BRAHMA COS account:\n{base}/verify-email?token={token}\n\nIf you did not create this account, ignore this email.")


def send_reset_email(email: str, name: str, token: str) -> bool:
    base = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000").rstrip("/")
    return send_email(email, "Reset your BRAHMA COS password", f"Hi {name},\n\nReset your password here:\n{base}/reset-password?token={token}\n\nThis link expires in 30 minutes.")


def send_event_email(subject: str, body: str) -> bool:
    recipient = os.getenv("ALERT_EMAIL") or os.getenv("SMTP_FROM")
    return send_email(recipient, subject, body) if recipient else False
