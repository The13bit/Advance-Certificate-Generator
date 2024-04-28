
from os import name
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window

from Components.CreateLink import CreateLink
from Components.FormDetailScreen import FormDetailScreen
from Components.FormListScreen import FormListScreen
from Components.TemplateAdder import TemplateAdder
from Components.ImageHandler import ImageHandler

# Set the size of the window
Window.size = (500, 600)






            
            

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FormListScreen(name='form_list'))
        sm.add_widget(FormDetailScreen(name='form_detail'))
        sm.add_widget(CreateLink(name='entry_slide'))
        sm.add_widget(TemplateAdder(name='template_adder'))
        sm.add_widget(ImageHandler(name='Image_hanldler'))
        return sm

MyApp().run()