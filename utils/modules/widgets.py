from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from random import choice
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivymd.toast import toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.behaviors.ripplebehavior import *
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton



class ProjectContainer(MDBoxLayout, Button, CircularRippleBehavior):
	id = StringProperty()
	# Stuff displayed on the Project Containers
	title = StringProperty("")
	date = StringProperty("")
	wip = StringProperty("")
	wtd = StringProperty("")
	
	
	def remove(self):
		self.parent.remove_widget(self)
	
	
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
	

class BoardDialogItem(OneLineIconListItem):
	divider = None
	icon = StringProperty()


class CardDialogItem(OneLineIconListItem):
	divider = None
	icon = StringProperty()

class MoveCardDialogItem(OneLineIconListItem):
	divider = None
	icon = StringProperty()


class AddCardDialogItem(OneLineIconListItem):
	divider = None
	icon = StringProperty("")
	
	
class CardCategory(MDBoxLayout):
	
	id = StringProperty("")

class CardContainer(MDBoxLayout):
	pass





class KanbanCard(AnchorLayout):
	
	title = StringProperty("")
	task = StringProperty("")
	categories = NumericProperty(0)
	due_date = StringProperty("")
	color = ObjectProperty()
	settings_open = False
	
	
	
	def move_card(self):
		if not self.settings_open:
			self.move_dialog = MDDialog(
				title="Change card:\n" + self.title + "\nto which category?" ,
				type="simple",
				items=[
					MoveCardDialogItem(text="Backlog", icon="update"),
					MoveCardDialogItem(text="In Progress", icon="progress-check"),
					MoveCardDialogItem(text="Done", icon="check-all"),
					],
				buttons=[
					MDRaisedButton(text="CANCEL"),
				],
					)
			self.move_dialog.buttons[0].on_press = self.move_dialog.dismiss
			self.move_dialog.size_hint = (None, 1)
			self.move_dialog.card = self
			self.move_dialog.card_category = self.parent.parent.parent.id
			self.move_dialog.width = 1000
			self.move_dialog.open()
		
	
		
	
	def show_settings(self):
		self.settings_open = True
		self.dialog = MDDialog(
			title="Kanaban Card Settings:\n" + self.title,
			type="simple",
			items=[
				CardDialogItem(text="Edit Card", icon="square-edit-outline"),
				CardDialogItem(text="Delete Card", icon="delete"),
				],
			buttons=[
				MDRaisedButton(text="DISCARD"),
			],
				)
		button = self.dialog.buttons[0]
		self.dialog.size_hint = (None, 1)
		self.dialog.width = 1000
		self.dialog.card = self
		
		def set_to_false():
			self.settings_open = False
			
		self.dialog.on_dismiss = set_to_false
		button.on_press = self.dialog.dismiss
		self.dialog.open()
	
	
	
	
		
class MainScreen(Screen):
	# Add New project
	def make_project_dialog(self):
		self.add_project_dialog = MDDialog(
			title="Create Project",
			type="custom",
			content_cls = AddProjectContent(),
			buttons=[
				MDFlatButton(text="CANCEL", text_color=(109/255, 145/255, 246/255, 1)),
				MDFlatButton(text="CREATE", text_color=(109/255, 145/255, 246/255, 1))
			],
		)
		self.add_project_dialog.size_hint = (None, 1)
		self.add_project_dialog.width = 1000
		self.add_project_dialog.buttons[0].on_press = self.add_project_dialog.dismiss
		self.add_project_dialog.open()
	

class BoardScreen(Screen):
	#dialog = None
	title = StringProperty("")
	name = StringProperty("")
	
	def show_settings_dialog(self):
		if not False:
			self.dialog = MDDialog(
				title="Kanaban Board Settings",
				type="simple",
				items=[
					BoardDialogItem(text="Set 'Works in progress' limit", icon="worker"),
					BoardDialogItem(text="Rename Project", icon="rename-box"),
					BoardDialogItem(text="Delete Project", icon="delete"),
					],
				buttons=[
					MDRaisedButton(text="DISCARD"),
				],
					)
		button = self.dialog.buttons[0]
		self.dialog.size_hint = (None, 1)
		self.dialog.width = 1000
		button.on_press = self.dialog.dismiss
		self.dialog.open()
		
	
		
class Content(MDBoxLayout):
	text = StringProperty()
	hint = StringProperty("")


class CardSettingsContent(MDBoxLayout):
	task = StringProperty()
	title = StringProperty()


class AddCardContent(MDBoxLayout):
	pass
	
class AddProjectContent(MDBoxLayout):
	pass

class HelpScreen(Screen):
	pass	
