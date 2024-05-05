import asyncio
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from kivy.core.window import Window

from Components.CreateLink import CreateLink
from Components.FormDetailScreen import FormDetailScreen
from Components.FormListScreen import FormListScreen
# from Components.TemplateAdder import TemplateAdder
# from Components.ImageHandler import ImageHandler

# Set the size of the window
Window.size = (500, 600)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FormListScreen(name="form_list"))
        sm.add_widget(FormDetailScreen(name="form_detail"))
        sm.add_widget(CreateLink(name="entry_slide"))
        
        return sm

    async def kivyCorout(self):
        await self.async_run(async_lib="asyncio") # type: ignore

    async def base(self):
        await asyncio.wait({self.kivyCorout()}, return_when="FIRST_COMPLETED")


instance = MyApp()
asyncio.run(instance.base())
