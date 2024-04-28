import base64
from cgitb import text
import io
from itertools import tee
import mimetypes
from os import name
import os
from turtle import onclick, title
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import json
from kivy.core.window import Window
import webbrowser
from test import HandleImageData
import tkinter as tk
from tkinter import filedialog
import re
from PIL import Image

class ImageHandler(Screen):
   
    def on_pre_enter(self, *args):
        self.clear_widgets()
        layout=BoxLayout(orientation="vertical")
        
        select_btn=Button(text="Select Image", size_hint_y=None, height=50)
        back_btn=Button(text="Back", size_hint_y=None, height=50)
        select_btn.bind(on_release=self.select_image) # type: ignore 
        back_btn.bind(on_release=self.go_back) # type: ignore
       
        layout.add_widget(select_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)
    def select_image(self,instance):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        imgPath = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
        if imgPath:
            with Image.open(imgPath) as img:
                img.resize((128,128))
                imgBytes=io.BytesIO()
                img.save(imgBytes,format='PNG')
                imgBytes=imgBytes.getvalue()
                encoded_image=base64.b64encode(imgBytes).decode('utf-8')
                image_json={'image':encoded_image,
                            'filename':os.path.basename(imgPath),
                            'contentType':mimetypes.guess_type(imgPath)[0]
                            }
                HandleImageData(json.dumps(image_json))
    def go_back(self,instance):
        self.manager.current='form_list'

