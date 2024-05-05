import asyncio
from cProfile import label
from cgitb import text
from concurrent.futures import thread
from itertools import tee
from os import name
import threading
from turtle import title
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.app import async_runTouchApp
import json
from kivy.core.window import Window
from kivy.clock import Clock
import webbrowser
from apis import Get_Json, Remove_entry
import re
from Generator import Generator
class FormDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form_name = ""
        self.Spread_id=""
        self.formId=""
    def on_pre_enter(self, *args):
        self.clear_widgets()
        print(self.manager.get_screen('form_list').entries)
        print(self.form_name)
        form = next((entry for entry in self.manager.get_screen('form_list').entries if entry['Form_Name'] == self.form_name), None)
        
        
        layout = FloatLayout(size=(300, 300))
        if form:
            self.formId=form["formId"]
            self.Spread_id=form['spreadsheetId']
            self.index=form["index"]
            lable1=Label(text=f"Form: {form['Form_Name']}",size_hint=(.25, .25),pos=(10, 500))
            btn1=Button(text="Modify",size_hint=(.25, .05),pos=(10, 300))
            btn2=Button(text="Generate",size_hint=(.25, .05),pos=(300, 300))
            btn3=Button(text="Back",size_hint=(.25, .05),pos=(10, 700))
            btn4=Button(text="Delete",size_hint=(.25, .05),pos=(10, 400))
            btn4.bind(on_release=self.initiate_deletion) # type: ignore
            btn2.bind(on_release=self.Schedule_generation)# type: ignore
            btn3.bind(on_release=self.go_to_form_initial)# type: ignore
            btn1.bind(on_release=lambda instance:webbrowser.open(f"https://docs.google.com/spreadsheets/d/{form['spreadsheetId']}"))# type: ignore
            layout.add_widget(btn4)
            layout.add_widget(btn1)
            layout.add_widget(btn3)
            layout.add_widget(btn2)
            layout.add_widget(lable1)
            
        self.add_widget(layout)

    def Schedule_generation(self,instance):
        thread=threading.Thread(target=self.Start_Generation)
        thread.start()
        
        

    def Start_Generation(self):
        if self.Spread_id!="":
            data=Get_Json(self.Spread_id,self.index)
            print(data)
            
            if data and data!='[]':
                data=json.loads(data)
                Generator(data,self.Spread_id).Start_Generation()
            else:
                def display_message(dt):
                    layout=BoxLayout(orientation="vertical")
                    lable=Label(text="Form Doesn't have any submission")
                    btn=Button(text="close")
                    layout.add_widget(lable)
                    layout.add_widget(btn)
                    popup=Popup(title="No content",content=layout,size_hint=(.7,.3))
                    btn.bind(on_press=popup.dismiss) # type: ignore
                    popup.open()
                Clock.schedule_once(display_message)
        return True
    def initiate_deletion(self,instance):
        layout=BoxLayout(orientation="vertical")
        lable=Label(text="The form and Sheet will Be deleted")
        btn=Button(text="Close")
        btn2=Button(text="Confirm")
        layout.add_widget(lable)
        layout.add_widget(btn2)
        layout.add_widget(btn)
        
        popup=Popup(title="Confirm",content=layout,size_hint=(.7,.3))
        btn.bind(on_release=popup.dismiss) # type: ignore
        btn2.bind(on_release=self.finalize_deletion) # type: ignore
        popup.open()
    def finalize_deletion(self,instance):
        Remove_entry(self.Spread_id,self.formId)


            

    def go_to_form_initial(self,instance):
        self.manager.current="form_list"