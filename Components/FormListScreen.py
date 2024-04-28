
from cgitb import text
from itertools import tee
from os import name
from turtle import onclick, title
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
class FormListScreen(Screen):
    def on_enter(self, *args):
        with open('Entries.json') as f:
            self.entries = json.load(f)
        self.entries=self.entries["Entry"]
        layout = BoxLayout(orientation='vertical', size_hint_y=None, pos_hint={'top': 1})
        layout.bind(minimum_height=layout.setter('height'))#type: ignore
        for entry in self.entries:
            btn = Button(text=entry['Form_Name'], size_hint_y=None, height=50)
            btn.bind(on_release=self.go_to_details)  # type: ignore
            layout.add_widget(btn)
        
    
        layout.add_widget(Label(size_hint_y=None, height=50))
    
        bottom_button = Button(text='Create Entry', size_hint_y=None, height=50)
        bottom_button.bind(on_release=self.go_to_FormId) # type: ignore

        add_templat_btn=Button(text="Add Template",size_hint_y=None,height=50)
        add_templat_btn.bind(on_release=self.go_to_template_adder)# type: ignore

        ImageHandle_btn=Button(text="add Signature",size_hint_y=None,height=50)
        ImageHandle_btn.bind(on_release=self.go_to_image_handler)# type: ignore


        layout.add_widget(add_templat_btn)
        layout.add_widget(bottom_button)
        layout.add_widget(ImageHandle_btn)

        self.add_widget(layout)
    def go_to_template_adder(self,instance):
        self.manager.current="template_adder"
    
    def go_to_image_handler(self,instance):
        self.manager.current="Image_hanldler"
    
    def go_to_FormId(self,instance):
        self.manager.current='entry_slide'
    def go_to_details(self, instance):
        self.manager.get_screen('form_detail').form_name = instance.text
        print(instance.text)
        self.manager.current = 'form_detail'