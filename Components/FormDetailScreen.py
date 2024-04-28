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
from test import Get_Json
import re
from Generator import Generator
class FormDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form_name = ""
        self.Spread_id=""
    def on_pre_enter(self, *args):
        self.clear_widgets()
        print(self.manager.get_screen('form_list').entries)
        print(self.form_name)
        form = next((entry for entry in self.manager.get_screen('form_list').entries if entry['Form_Name'] == self.form_name), None)
        
        layout = FloatLayout(size=(300, 300))
        if form:
            self.Spread_id=form['spreadsheetId']
            lable1=Label(text=f"Form: {form['Form_Name']}",size_hint=(.25, .25),pos=(10, 500))
            btn1=Button(text="Modify",size_hint=(.25, .05),pos=(10, 300))
            btn2=Button(text="Generate",size_hint=(.25, .05),pos=(300, 300))
            btn3=Button(text="Back",size_hint=(.25, .05),pos=(10, 700))
            btn2.bind(on_release=self.HellDive)# type: ignore
            btn3.bind(on_release=self.go_to_form_initial)# type: ignore
            btn1.bind(on_release=lambda instance:webbrowser.open(f"https://docs.google.com/spreadsheets/d/{form['spreadsheetId']}"))# type: ignore
            #layout.add_widget(btn1)
            layout.add_widget(btn3)
            layout.add_widget(btn2)
            layout.add_widget(lable1)
            
        self.add_widget(layout)
    def HellDive(self,instance):
        if self.Spread_id!="":
            data=Get_Json(self.Spread_id)
            data=json.loads(data)
            Generator(data).Rock_and_roll()

    def go_to_form_initial(self,instance):
        self.manager.current="form_list"