"""
Simple CLI script to send test emails for verifying the Gmail to Todoist ALERT Automation.
Can be used with any SMTP provider (Gmail App Password, Mailtrap, Sendgrid, etc.).
"""

import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SAMPLE_ALERT_SUBJECT = "ALERT: Production Database High CPU Load [CRITICAL]"
SAMPLE_ALERT_BODY = """Hello Team,

This is an automated alert from the Infrastructure Monitoring Service.

Incident Details:
- Server: prod-db-replica-02
- Metric: CPU Utilization exceeded 98% for 5 consecutive minutes.
- Timestamp: 2026-11-21 03:15:00 UTC
- Action Required: Please check long-running database queries and connection pool immediately.

Best regards,
DevOps Alert System
"""

SAMPLE_NORMAL_SUBJECT = "Weekly Team Sync Notes - Review Required"
SAMPLE_NORMAL_BODY = """Hi team,

Attached are the notes from today's weekly sync meeting.
Please review the action items when you have a moment.

Thanks,
Management
"""


def send_email(smtp_server, port, sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    print(f"Connecting to SMTP server {smtp_server}:{port}...")
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    print(f"Email sent successfully to {recipient_email} with subject: '{subject}'")


def main():
    parser = argparse.ArgumentParser(description="Send test emails for Gmail -> Todoist ALERT workflow.")
    parser.add_argument("--smtp", default="smtp.gmail.com", help="SMTP server host (default: smtp.gmail.com)")
    parser.add_argument("--port", type=int, default=465, help="SMTP port (default: 465 for SSL)")
    parser.add_argument("--sender", required=True, help="Sender email address")
    parser.add_argument("--password", required=True, help="Sender password or App Password")
    parser.add_argument("--recipient", required=True, help="Recipient email address (the connected Gmail account)")
    parser.add_argument("--type", choices=["alert", "normal"], default="alert", help="Email type to send ('alert' or 'normal')")

    args = parser.parse_args()

    if args.type == "alert":
        subject = SAMPLE_ALERT_SUBJECT
        body = SAMPLE_ALERT_BODY
    else:
        subject = SAMPLE_NORMAL_SUBJECT
        body = SAMPLE_NORMAL_BODY

    send_email(
        smtp_server=args.smtp,
        port=args.port,
        sender_email=args.sender,
        sender_password=args.password,
        recipient_email=args.recipient,
        subject=subject,
        body=body
    )


if __name__ == "__main__":
    main()
