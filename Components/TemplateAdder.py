from cgitb import text
from itertools import tee
from os import name
from turtle import title
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import json
from kivy.core.window import Window
import webbrowser
from test import createSpreadsheetAndLinkForm
from test import LoadAndSaveCertTemplate
import re
# Set the size of the window
Window.size = (500, 600)

class TemplateAdder(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def on_Enter(self,instance):
        print(instance.text)
        spreadId=re.search(r"/d/(.*?)/edit",instance.text)
       
        if spreadId:
            with open('Entries.json',"r") as f:
                content=json.load(f)
                for i in content["certificates"]:
                    if i["spId"]==spreadId.group(1):
                        print("Already Exists")
                        layout=BoxLayout(orientation="vertical")
                        lable=Label(text="Ceritficate already exist")
                        btn=Button(text="close")
                        layout.add_widget(lable)
                        layout.add_widget(btn)
                        popup=Popup(title="Duplicate error",content=layout,size_hint=(.7,.3))
                        btn.bind(on_press=popup.dismiss) # type: ignore
                        popup.open()

                        return
            sid=spreadId.group(1)
            print(sid)
            if LoadAndSaveCertTemplate(sid):
                self.manager.current="form_list"
    
    def on_pre_enter(self, *args):
        self.clear_widgets()
        layout = FloatLayout(size=(300, 300))
        text=TextInput(hint_text="Enter the Certificate Template Url",multiline=False,size_hint=(.5, .05),pos=(10, 600))
        text.bind(on_text_validate=self.on_Enter)# type: ignore
        btn3=Button(text="Back",size_hint=(.25, .05),pos=(10, 700))
        btn3.bind(on_release=self.go_to_form_initial)# type: ignore
        layout.add_widget(btn3)
        layout.add_widget(text)
        self.add_widget(layout)
    def go_to_form_initial(self,instance):
        self.manager.current="form_list"