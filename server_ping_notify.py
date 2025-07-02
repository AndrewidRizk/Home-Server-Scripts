import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_server_status(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def send_email_notification(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Notification email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Configuration
    SERVER_URL = "http://174.92.129.230:5000/"
    
    # Fetch credentials from environment variables
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # Set this in GitHub Actions
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # Set this in GitHub Actions
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Set this in GitHub Actions

    server_status = check_server_status(SERVER_URL)
    if not server_status:
        print("Server is down. Sending notification...")
        subject = "Server Down Alert"
        body = f"The server at {SERVER_URL} is not responding. Please check immediately."
        send_email_notification(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, subject, body)
    else:
        print("Server is up.")
