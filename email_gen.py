import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string

# Configuration for SMTP
from_email = "amitytechtitans@gmail.com"
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Common port for SMTP with TLS
smtp_user = 'amitytechtitans@gmail.com'
smtp_password = 'sih@2024'  # Ensure you use a secure method for storing passwords

# List of characters for generating random key
characters = string.ascii_uppercase + string.digits

def register(to_email):
    # Email content
    subject = 'AAPNAME Access Key'
    body1 = 'Greetings,\nYour UID is as follows\n'
    body2 = 'Follow this link to create a password\n'
    body3 = 'Thank You, from Tech Titans'
    pass_set = '/link for pass set/\n'
    
    # Generate a random key
    access_key = generate_key()

    # Create a MIMEMultipart object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body1, 'plain'))
    msg.attach(MIMEText(access_key, 'plain'))
    msg.attach(MIMEText(body2, 'plain'))
    msg.attach(MIMEText(pass_set, 'plain'))
    msg.attach(MIMEText(body3, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f'Email sent to {to_email}')
    except Exception as e:
        print(f'Error: {e}')

def generate_key(length=8):
    """Generate a random key with the specified length."""
    return ''.join(random.choice(characters) for _ in range(length))

# Example usage
to_email = 'harkirankaur.0606@gmail.com'
register(to_email)

#def forgot_password(to_email):