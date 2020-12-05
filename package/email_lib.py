import smtplib, ssl
import urllib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen
import s3_lib

def generateEmail(addr, url):
    sender_email = "artsy.backend@gmail.com"
    receiver_email = addr
    password = "eecs495backend"
    message_alternative = MIMEMultipart("alternative")
    message = MIMEMultipart("mixed")
    message["Subject"] = "Your Artsy Drawing"
    message["From"] = f'Artsy! <sender_email>'
    message["To"] = receiver_email

    image = MIMEBase('image', 'png', filename='drawing.png')
    with urlopen(url) as resource:
        image.set_payload(resource.read())
    
    encoders.encode_base64(image)
    
    
    # Create the plain-text and HTML version of your message
    text = """\
        Hello,
        
        Thanks for using the Artsy drawing app!
        
        Your amazing drawing is attached to this email. You can save it to your device and keep it forever!
        """
    
    html = """\

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>Your Artsy Drawing!</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        
        <style type="text/css">
            a[x-apple-data-detectors] {color: inherit !important;}
            </style>
    </head>
    <body style="margin: 0; padding: 0;">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 20px 0 30px 0;">
                    
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #cccccc;">
                        <tr>
                            <td align="center" bgcolor="#0a274a" style="padding: 10px 0 0 0;" style="color: #153643; font-family: Arial, sans-serif;">
                                <h1 style="font-size: 28px; margin-top: 10px; color: #ffffff; font-family: Comic Sans MS, sans-serif">Your Artsy Masterpiece Has Arrived!</h1>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" bgcolor="#0a274a" style="padding: 10px 0 30px 0;">
                                <img src="https://artsy-bucket.s3.amazonaws.com/email_assets/artsy.png" alt="Artsy Logo" width="230" height="230" style="display: block;" />
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#eeeeee" style="padding: 40px 30px 10px 30px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                                    <tr>
                                        <td style="color: #153643; font-family: Arial, sans-serif;">
                                            <h1 style="font-size: 24px; margin: 0;">Thank you for using the Artsy drawing app!</h1>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 24px; padding: 20px 0 30px 0;">
                                            <p style="margin: 0;"> We hope you enjoyed your time using Artsy! Your amazing drawing is attached to this email. You can save it to your device and keep it forever!</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#0a274a" style="padding: 30px 30px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;">
                                    <tr>
                                        <td align="left">
                                            <img src="https://artsy-bucket.s3.amazonaws.com/email_assets/MM.png" alt="Artsy Logo"  height="30" style="display: block;" />
                                        </td>
                                        <td align="right" style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;">
                                            <p style="margin: 0;">&reg; Artsy, Ann Arbor 2020<br/>
                                        </td>
                            
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
"""
    
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message_alternative.attach(part1)
    message_alternative.attach(part2)
    message.attach(message_alternative)
    message.attach(image)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
