import sys
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, results, sender_email, sender_password, recipient_email):
    # 🔹 Build HTML table rows from results string (supports \n and real newlines)
    clean_lines = re.split(r'(?:\\n|\n)', results.strip())
    rows = ""

    for line in clean_lines:
        if not line.strip():
            continue
        status = "✅" in line
        try:
            message = line.split("✅")[1] if status else line.split("❌")[1]
        except IndexError:
            message = line
        rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ccc;">{message.strip()}</td>
            <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">
                {"<span style='color:green;'>✔ Success</span>" if status else "<span style='color:red;'>✘ Failed</span>"}
            </td>
        </tr>
        """

    # 🔹 Construct full HTML email body
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>🔔 Server Update Summary</h2>
        <p><strong>Public IP:</strong> {subject}</p>
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr>
                    <th style="padding: 8px; border: 1px solid #ccc; background-color: #f9f9f9;">Task</th>
                    <th style="padding: 8px; border: 1px solid #ccc; background-color: #f9f9f9;">Status</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </body>
    </html>
    """

    # 🔹 Setup MIME message
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = f"🔔 Server Update Report – {subject}"

    msg.attach(MIMEText(html_body, "html"))

    # 🔹 Send via Gmail SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("✅ Email notification sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# 🔹 Entry point
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python send_email.py <subject> <results_text> <sender_email> <sender_pass> <recipient_email>")
        sys.exit(1)

    subject = sys.argv[1]
    results = sys.argv[2]
    sender = sys.argv[3]
    password = sys.argv[4]
    recipient = sys.argv[5]

    send_email(subject, results, sender, password, recipient)
