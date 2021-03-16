from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty
from random import choice
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDRaisedButton


class ProjectContainer(MDBoxLayout, Button):
	
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
	

class DialogItem(OneLineIconListItem):
	divider = None
	icon = StringProperty()


	
class CardCategory(MDBoxLayout):
	id = StringProperty("")


class KanbanCard(AnchorLayout):
	
	title = StringProperty("")
	task = StringProperty("")
	
	def on_touch_down(self, touch):
		if touch.is_double_tap:
			print(dir(self))
			#toast(self.title)
			toast("You touched the card twice!")
		if touch.is_triple_tap:
			toast(self.title)
			toast("You touched the card thrice!")
		
		
class MainScreen(Screen):
	pass
	

class BoardScreen(Screen):
	dialog = None
	title = StringProperty("")
	name = StringProperty("")
	
	def show_settings_dialog(self):
		if not self.dialog:
			self.dialog = MDDialog(
				title="Kanaban Board Settings",
				type="simple",
				items=[
					DialogItem(text="Set 'Works in progress' limit", icon="worker"),
					DialogItem(text="Rename Project", icon="rename-box"),
					DialogItem(text="Delete Project", icon="delete"),
					],
				buttons=[
					MDRaisedButton(text="DISCARD", id = 'b'),
				],
					)
		button = [i for i in self.dialog.buttons if i.id == 'b']
		button = button[0]
		button.on_press = self.dialog.dismiss
		self.dialog.open()