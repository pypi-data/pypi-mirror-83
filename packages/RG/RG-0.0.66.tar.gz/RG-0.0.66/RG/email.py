# email: send email via Python

from email.mime.text import MIMEText
from email.header import Header
import smtplib

def email(user,pwd,to,title,text):
    """
    email: send email via Python
    
    INPUT
    user (string) : enter sender email
    pwd (string): enter sender email password
    to (string) : enter reciever email
    title (string) : title of the email
    text (string) : body of the email
    
    OUTPUT
    None
    
    EXAMPLE
    
    user='ryan.gosselin@usherbrooke.ca'
    pwd=input('Input Outlook password: ')
    to = 'ryan.gosselin@gmail.com'
    title = 'Test title'
    
    name = 'John'
    g1 = 5
    g2 = 6
    
    text = '\nBonjour {},'\
    '\n\nVoici un survol de tes résultats à l\'examen 1.'\
    '\n\nQuestion 1: {:.2f} /5.'\
    '\nQuestion 2: {:.2f} /5.'\
    '\n\nRyan'.format(name,g1,g2)
    
    """
    
    server = smtplib.SMTP('smtp.office365.com', 587) #to work with outlook
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    
    body = MIMEText(text, 'plain', 'utf-8')
    body['From'] = user
    body['To'] = to
    body['Subject'] = Header(title, 'utf-8')
    try:
        server.sendmail(user, [to], body.as_string())
        print('\nemail was sent')
    except:
        print('\nerror')
    server.quit()