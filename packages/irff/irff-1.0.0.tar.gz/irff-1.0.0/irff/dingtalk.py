import smtplib
from email.mime.text import MIMEText
from dingtalkchatbot.chatbot import DingtalkChatbot
from os import popen,getcwd
import re


webhook='https://oapi.dingtalk.com/robot/send?access_token=9a567ecf401bbd43a7b63bafe36c30f5c88b660a7831c326ad4f6291c9460cce'
dlam   = DingtalkChatbot(webhook)


def valid_ip(ip):
    if ("255" in ip) or ( ip == "127.0.0.1") or ( ip == "0.0.0.0" ) or ( ip == "127.0.1.1"):
        return False
    else:
        return True

def get_ip(valid_ip):
    ipss = ''.join(popen('ifconfig').readlines())
    match = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ips = re.findall(match, ipss, flags=re.M)
    ip = filter(valid_ip, ips)
    for i,I in enumerate(ip):
        if i==0:
           IP = I
        else:
           IP += '/'+I
    return IP

ip = get_ip(valid_ip)
hn=''.join(popen('hostname').readlines())
hostname = hn[:-1]


def send_mail(content,sub='JobMessage'):
    # hname = getfqdn(gethostname())
    # addr  = gethostbyname(hname)
    cwd = getcwd()
    content= content+'\nFrom: '+cwd
    to_list=['fenggo@dingtalk.com']         
    mail_host="smtp.163.com"  
    mail_user="birdofwander"  
    mail_pass="lcudxwl" 
    mail_postfix="163.com"  
    me="StationDriod"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list) 

    try:
       server = smtplib.SMTP()
       server.connect(mail_host)   
       # smtp.ehlo()
       # smtp.starttls()  
       server.login(mail_user,mail_pass) 
       server.sendmail(me, to_list, msg.as_string())
       server.close()
       return True
    except Exception as e:
       print(e)
       return False


def send_msg(msg):
    cwd=getcwd()
    msg = '#### MY Master:\n'+'----------------\n '+ msg
    msg += '\n\n----------------\n'
    msg += '\n From: '+hostname+'@'+ip+'\n' #\nmy master
    msg += '\n (directory: '+cwd+')'
    try:
       dlam.send_markdown(title='Master:',text=msg)
    except:
       # send_mail(msg)
       print('-  warning massage send failed.')

