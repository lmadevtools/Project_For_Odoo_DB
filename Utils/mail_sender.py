#class not used. I just put it in case we would like to implement an automatic order for low stock products.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
smtp_server = 'smtp.server.com'
smtp_port = 25  # 25 is The default SMTP port for unauthenticated sending
sender_email = 'your_email@server.com'
recipient_email = 'supplier@example.com'
subject = 'Restock necessary for low stock product'
message = 'List of product where a restock is necessary :'

# Create the email message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject

# Attach the message body
msg.attach(MIMEText(message, 'plain'))

try:
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Send the email without authentication
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print('Email sent successfully!')
except Exception as e:
    print('Email sending failed:', str(e))
else:
    server.quit()