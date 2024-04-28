import json
import pandas as pd
from PIL import  Image,ImageFont,ImageDraw
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import base64
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib, ssl
from tkinter import E
from Helper import api,auth
import os
from dotenv import load_dotenv
from helper.BoundedBoxer import BoundedBoxer
load_dotenv()
class Generator:
    def __init__(self,data) -> None:
        self.Cert_path='certificates/cert.png'
        self.data=data
        self.img=Image.open(self.Cert_path)
        self.df=pd.DataFrame.from_dict(data)
        self.EMAIL_FROM=os.environ.get("EMAIL")
        
        self.EMAIL_SUBJECT = 'Hello  from '
        self.EMAIL_CONTENT = 'This is you certificate'




    def Rock_and_roll(self):
        
        self.df.drop(['!^$(x)','Flag',''],inplace=True,axis=1)
        print(self.df)


        def send_mail(message):
            port = 465  # For SSL
            gapi=auth()
            entry=api(gapi)
            mailer=entry.create_mailer()


            # Create a secure SSL context
            print(mailer.users().messages().send(userId="me", body=message).execute())


        def create_message(sender, to, subject, message_text,file):
          """Create a message for an email.
          Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.
          Returns:
            An object containing a base64url encoded email object.
          """
          message=MIMEMultipart()
          message['to']=to
          message['from']=sender
          message['subject']=subject

          msg=MIMEText(message_text)
          message.attach(msg)

          with open(file,'rb') as image_file:
            image=MIMEImage(image_file.read())
            image.add_header('Content-Disposition','attachment',filename='cert.png')
            message.attach(image)
          raw_message=base64.urlsafe_b64encode(message.as_bytes())
          return {'raw': raw_message.decode('utf-8')}





        def select_columns():
            selectedCols=[]
            window = tk.Tk()
            window.title("Column Selection")


            listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)


            for column in self.df.columns:
                listbox.insert(tk.END, column)


            def confirm_selection():
                nonlocal selectedCols
                selectedCols = [listbox.get(i) for i in listbox.curselection()]

                window.destroy()

            confirm_button = tk.Button(window, text="Confirm", command=confirm_selection)


            listbox.pack()
            confirm_button.pack()


            window.mainloop()
            return selectedCols

        def create_and_send(rectangles,RezeidFacotr,seleccol,df_selected,df_email):
        
            ct=0
            for row in df_selected.itertuples(index=False):
                img=Image.open(self.Cert_path)
                img=img.resize(RezeidFacotr) # type: ignore
                draw=ImageDraw.Draw(img)
                for i in range(len(seleccol)):
                    draw.text(((rectangles[i][0][0]+rectangles[i][1][0])/2,(rectangles[i][0][1]+rectangles[i][1][1])/2),row[i], font=ImageFont.truetype("arial.ttf", 20),fill='black',anchor='mm')
                img.save(f"./output/{row[0]}.png")

                if df_email[ct]:
                    message=create_message(self.EMAIL_FROM,df_email[ct],self.EMAIL_SUBJECT,self.EMAIL_CONTENT,f"./output/{row[0]}.png")
                    send_mail(message)
                ct+=1

                #os.remove(f"./output/{row[0]}.png")


        seleccol=select_columns()
        df_selected = self.df[seleccol]
        df_email = self.df['Email Address']
        rectangles,ReRezeidFacotr=BoundedBoxer(seleccol,self.Cert_path).initiator()
        create_and_send(rectangles,ReRezeidFacotr,seleccol,df_selected,df_email)
        return True
    
    

