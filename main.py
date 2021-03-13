from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import (ScreenManager, Screen)




class Oculus(MDApp):
	def build(self):
		self.theme_cls.primary_palette = "Blue"
		self.root = Builder.load_file("design.kv")
	
	def on_start(self):
		pass
		
class MainScreen(Screen):
	pass
	
if __name__ == "__main__":
	Oculus().run()