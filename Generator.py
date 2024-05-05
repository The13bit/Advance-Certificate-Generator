import hashlib
import json
import shutil
import threading
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import tkinter as tk

import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from Auth import api, auth
import os
from dotenv import load_dotenv

from Thread_lock import Locker
from helper.BoundedBoxer import BoundedBoxer

load_dotenv()


class Generator:
    def __init__(self, data, spreadId) -> None:
        self.Cert_path = "certificates/cert.png"
        self.data = data
        self.img = Image.open(self.Cert_path)
        self.df = pd.DataFrame.from_dict(data)
        self.EMAIL_FROM = os.environ.get("EMAIL")
        self.spreadId = spreadId
        self.EMAIL_SUBJECT = "Hello  from "
        self.EMAIL_CONTENT = "This is you certificate"
        self.Conditons = []

    def Start_Generation(self):
        print(self.df)
        event = threading.Event()

        def send_mail(message):
            port = 465  # For SSL
            gapi = auth()
            entry = api(gapi)
            mailer = entry.create_mailer()

            # Create a secure SSL context
            print(mailer.users().messages().send(userId="me", body=message).execute())

        def create_message(sender, to, subject, message_text, file):
            """Create a message for an email.
            Args:
              sender: Email address of the sender.
              to: Email address of the receiver.
              subject: The subject of the email message.
              message_text: The text of the email message.
            Returns:
              An object containing a base64url encoded email object.
            """
            message = MIMEMultipart()
            message["to"] = to
            message["from"] = sender
            message["subject"] = subject

            msg = MIMEText(message_text)
            message.attach(msg)

            with open(file, "rb") as image_file:
                image = MIMEImage(image_file.read())
                image.add_header(
                    "Content-Disposition", "attachment", filename="cert.png"
                )
                message.attach(image)
            raw_message = base64.urlsafe_b64encode(message.as_bytes())
            return {"raw": raw_message.decode("utf-8")}

        def select_columns():
            selectedCols = []
            window = tk.Tk()
            window.title("Column Selection")

            listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)

            for column in self.df.columns:
                listbox.insert(tk.END, column)

            def confirm_selection():
                nonlocal selectedCols
                selectedCols = [listbox.get(i) for i in listbox.curselection()]

                window.destroy()

            confirm_button = tk.Button(
                window, text="Confirm", command=confirm_selection
            )

            listbox.pack()
            confirm_button.pack()

            window.mainloop()
            return selectedCols

        def set_subject(instance, value):
            self.EMAIL_SUBJECT = value

        def set_message(instance, value):
            self.EMAIL_CONTENT = value

        def create__message_box(dt):
            def on_button_release(instance):
                # Dismiss the popup
                popup.dismiss()
                Add_Watch_Conditions()
                # Set the event

            layout = BoxLayout(orientation="vertical")
            subject_label = Label(text="Subject")
            subject_box = TextInput(text="Enter Subject")

            message_label = Label(text="Message")
            messgae_box = TextInput(text="Enter Message", multiline=True)

            subject_box.bind(text=set_subject)  # type: ignore
            messgae_box.bind(text=set_message)  # type: ignore
            button = Button(text="Close")
            layout.add_widget(subject_label)
            layout.add_widget(subject_box)
            layout.add_widget(message_label)
            layout.add_widget(messgae_box)
            layout.add_widget(button)
            popup = Popup(title="Add Message", content=layout, size_hint=(0.5, 0.5))
            button.bind(on_release=on_button_release)  # type: ignore
            popup.open()

        def Add_Watch_Conditions():
            Conditions = ["<", ">", "<=", ">=", "=="]

            def closer(instance):
                popup.dismiss()

                for i in outerlayout.children:
                    arr = []
                    for j in i.children:
                        if isinstance(j, Button):
                            arr.append(j.text)
                        elif isinstance(j, TextInput):
                            arr.append(j.text)

                    if arr and arr[0] != "":
                        self.Conditons.append(arr[::-1])

                event.set()

            innerlayout = BoxLayout()
            dropbox = DropDown()
            dropbox2 = DropDown()
            for i in self.seleccol:
                btn = Button(text=i, size_hint=(None, None), height=44)
                dropbox.add_widget(btn)
                btn.bind(on_release=lambda btn: dropbox.select(btn.text))  # type: ignore
            for i in Conditions:
                btn = Button(text=i, size_hint=(None, None), height=44)
                dropbox2.add_widget(btn)
                btn.bind(on_release=lambda btn: dropbox2.select(btn.text))  # type: ignore

            mainbutton = Button(text="Select", size_hint=(0.3, None), height=44)
            mainbutton.bind(on_release=dropbox.open)  # type: ignore
            mainbutton2 = Button(text="Select", size_hint=(0.3, None), height=44)
            mainbutton2.bind(on_release=dropbox2.open)  # type: ignore
            dropbox2.bind(on_select=lambda instance, x: setattr(mainbutton2, "text", x))  # type: ignore
            textinput = TextInput(
                hint_text="Enter Value", size_hint=(0.3, None), height=44
            )
            dropbox.bind(on_select=lambda instance, x: setattr(mainbutton, "text", x))  # type: ignore
            innerlayout.add_widget(mainbutton)
            innerlayout.add_widget(mainbutton2)
            innerlayout.add_widget(textinput)

            outerlayout = BoxLayout(orientation="vertical")
            outerlayout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

            popup = Popup(title="Select Conditions", content=outerlayout)

            closebtn = Button(text="Close/Skip", size_hint=(1, 0.2))
            closebtn.bind(on_release=closer)  # type: ignore

            # addbtn=Button(text="+",size_hint=(1,.2), background_color=(0, 0, 0, 0))
            # addbtn.bind(on_release=Condition_row_maker) # type: ignore

            # outerlayout.add_widget(addbtn)
            outerlayout.add_widget(innerlayout)
            outerlayout.add_widget(closebtn)

            popup.open()

        def template_selector():
            root = tk.Tk()
            root.withdraw()
            img_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
            )
            if img_path:
                digest = hashlib.sha256(str.encode(img_path)).hexdigest()[:10]
                shutil.copy(img_path, f"./certificates/{digest}.png")
                self.Cert_path = f"./certificates/{digest}.png"
                root.destroy()

        def create_and_send(rectangles, RezeidFacotr, seleccol, df_selected, df_email):
            if self.Conditons:
                df_combine = pd.concat([df_selected, df_email], axis=1)
                df_combine.columns = [
                    column.replace(" ", "_") for column in df_combine.columns
                ]
                print(df_combine)
                for condition in self.Conditons:
                    colums, operator, value = condition
                    colums = colums.replace(" ", "_")
                    if isinstance(value, str):
                        try:
                            # Try to convert the value to a number
                            value = float(value)
                        except ValueError:
                            # If the value cannot be converted to a number, keep it as a string
                            value = f"'{value}'"

                    query_str = f"{colums} {operator} {value}"
                    df_combine = df_combine.query(query_str)
                    print(df_combine)
                df_combine = df_combine.reset_index(drop=True)
                df_combine[seleccol] = df_combine[seleccol].map(str)
                df_selected = df_combine[seleccol]
                df_email = df_combine["Email_Address"]

            df_selected[seleccol] = df_selected[seleccol].map(str)

            ct = 0
            for row in df_selected.itertuples(index=False):
                img = Image.open(self.Cert_path)
                img = img.resize(RezeidFacotr)  # type: ignore
                draw = ImageDraw.Draw(img)
                for i in range(len(seleccol)):
                    draw.text(
                        (
                            (rectangles[i][0][0] + rectangles[i][1][0]) / 2,
                            (rectangles[i][0][1] + rectangles[i][1][1]) / 2,
                        ),
                        row[i],
                        font=ImageFont.truetype("arial.ttf", 20),
                        fill="black",
                        anchor="mm",
                    )
                if not os.path.exists("./output"):
                    os.mkdir("output")

                img.save(f"./output/{row[0]}.png")

                if df_email[ct]:
                    message = create_message(
                        self.EMAIL_FROM,
                        df_email[ct],
                        self.EMAIL_SUBJECT,
                        self.EMAIL_CONTENT,
                        f"./output/{row[0]}.png",
                    )
                    send_mail(message)
                ct += 1

                # os.remove(f"./output/{row[0]}.png")

        with Locker() and open("Entries.json", "r+") as file:
            content = json.load(file)
            for entry in content["Saved_settings"]:
                if entry["spreadId"] == self.spreadId:
                    seleccol = entry["Selected_columns"]
                    rectangles = entry["rectangles"]
                    ReRezeidFactor = entry["ReRezeidFactor"]
                    self.EMAIL_SUBJECT = entry["Subject"]
                    self.EMAIL_CONTENT = entry["Message"]
                    self.Cert_path = entry["Cret_path"]
                    self.Conditons = entry["Conditions"]
                    df_selected = self.df[seleccol]
                    df_email = self.df["Email Address"]
                    create_and_send(
                        rectangles, ReRezeidFactor, seleccol, df_selected, df_email
                    )
                    return True
            template_selector()
            self.seleccol = select_columns()
            df_selected = self.df[self.seleccol]
            df_email = self.df["Email Address"]
            rectangles, ReRezeidFactor = BoundedBoxer(
                self.seleccol, self.Cert_path
            ).initiator()
            Clock.schedule_once(create__message_box)
            event.wait()

            content["Saved_settings"].append(
                {
                    "Selected_columns": self.seleccol,
                    "rectangles": rectangles,
                    "ReRezeidFactor": ReRezeidFactor,
                    "spreadId": self.spreadId,
                    "Subject": self.EMAIL_SUBJECT,
                    "Message": self.EMAIL_CONTENT,
                    "Cret_path": self.Cert_path,
                    "Conditions": self.Conditons,
                }
            )
            file.seek(0)
            json.dump(content, file, indent=4)
            file.truncate()
            create_and_send(
                rectangles, ReRezeidFactor, self.seleccol, df_selected, df_email
            )
            return True
