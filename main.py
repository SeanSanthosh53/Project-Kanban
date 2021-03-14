from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from random import choice
from kivy.core.text import LabelBase




class ProjectContainer(MDBoxLayout):
	
	# Stuff displayed on the Project Containers
	title = StringProperty("")
	date = StringProperty("")
	wip = StringProperty("")
	wtd = StringProperty("")
	
	
	# Color Options for the Project Containers
	primary_colors = [(74/255, 73/255, 166/255, 1), (137/255, 139/255, 201/255, 1), (253/255, 143/255, 149/255, 1), (109/255, 145/255, 246/255, 1)]
	# DarkBlue, Purple, Peach, Blue 
	
	secondary_colors = [(69/255, 68/255, 151/255, 1), (127/255, 129/255, 190/255, 1), (253/255, 154/255, 162/255, 1), (127/255, 158/255, 247/255, 1)]
	
	colors = {(109/255, 145/255, 246/255, 1): (127/255, 158/255, 247/255, 1),
 (137/255, 139/255, 201/255, 1): (127/255, 129/255, 190/255, 1),
 (253/255, 143/255, 149/255, 1): (253/255, 154/255, 162/255, 1),
 (74/255, 73/255, 166/255, 1): (69/255, 68/255, 151/255, 1)}
	
	
	# Choose colors for the Containers	
	prime_bg_color =  choice(primary_colors)
	second_bg_color = colors[prime_bg_color]
	
	
	



		
class MainScreen(Screen):
	pass
	

class BoardScreen(Screen):
	pass



class Oculus(MDApp):
	def build(self):
		self.theme_cls.primary_palette = "Blue"
		
		# Register different fonts
		fonts = ['ConfessionRegular.ttf', 'CabalBold.ttf', 'AovelSans.ttf', 'Cabal.ttf', 'Nasa21.ttf', 'Paul.ttf', 'ConfessionFullRegular.ttf']
		for font in fonts:
			print(font[:-4])
			LabelBase.register(name = font[:-4], fn_regular = f"utils/{font}")
		
		self.primary_colors = {"Dark Blue": (74/255, 73/255, 166/255, 1),
"Light Blue": (109/255, 145/255, 246/255, 1),
"Light Purple": (137/255, 139/255, 201/255, 1),
"Peach": (253/255, 143/255, 149/255, 1)}
		self.secondary_colors = {"Dark Blue": (69/255, 68/255, 151/255, 1),
"Light Blue": (127/255, 158/255, 247/255, 1),
"Light Purple": (127/255, 129/255, 190/255, 1),
"Peach": (253/255, 154/255, 162/255, 1)}

		self.root = Builder.load_file("design.kv")
	
	
	# Stuff to do in the beginning
	def on_start(self):
		# Add the project containers
		self.add_container("Timathon", "14/3/21", "2", "3", times = 7)
	
	
	# Function to add a Project Container		
	def add_container(self, title, date, works_in_progress, work_to_do, times=3):
		for i in range(times):
			self.root.ids.main_screen.ids.project_library.add_widget(ProjectContainer(title = title, date = date, wip = works_in_progress, wtd = work_to_do))
		
	
	
	

	
	
if __name__ == "__main__":
	Oculus().run()