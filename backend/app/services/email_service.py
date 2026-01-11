import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_complaint_email(to_email: str, subject: str, body: str):
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("SMTP not configured, skipping email.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = settings.SMTP_FROM
    msg['To'] = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def notify_new_complaint(complaint_id: int, plate: str, description: str, incident_time, user_email: str):
    subject = f"New Complaint Created - {plate} - #{complaint_id}"
    body = f"""
    A new complaint has been submitted.
    
    Complaint ID: {complaint_id}
    Plate: {plate}
    User Email: {user_email}
    Incident Time: {incident_time}
    
    Description:
    {description}
    """
    send_complaint_email(settings.COMPLAINT_EMAIL_TO, subject, body)
