import smtplib,os,sys,socket
import datetime
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

emailfrom = "freelfeelmcla@gmail.com"
emailto = ["js5986@mcla.edu","emilly.ailing@mcla.edu","library@mcla.edu"]
fileToSend = "data.csv"
username = "freelfeelmcla@gmail.com"
password = "ckjmjftdglchefve"

def get_device_ip_address():

    try: 
        if os.name == "nt":
            # On Windows
            result = "Running on Windows"
            hostname = socket.gethostname()
            result += "\nHostname:  " + hostname
            host = socket.gethostbyname(hostname)
            result += "\nHost-IP-Address:" + host
            return result

        elif os.name == "posix":
            gw = os.popen("ip -4 route show default").read().split()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((gw[2], 0))
            ipaddr = s.getsockname()[0]
            gateway = gw[2]
            host = socket.gethostname()
            result = "Freel feel rebooted...\n\nOS:\t\tRaspbian\nIP:\t\t" + ipaddr + "\nGateway:\t\t" + gateway + "\nHost:\t\t" + host+"\n\nHere is yesterday's CSV log as well"
            return result
        
        else:
            result = os.name + " not supported yet."
            return result
    except:
        return "Could not detect ip address"
global body
body = get_device_ip_address() + '\n\n'
body = MIMEText(body)
for email in emailto:
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = email
    msg["Subject"] = "Daily CSV --> " + str(datetime.datetime.now())
    msg.attach(body)

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, email, msg.as_string())
    server.quit()