from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from utils.modules.widgets import *
from kivymd.uix.button import MDFlatButton
import json
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDDatePicker
from datetime import date
from kivy.core.window import Window



class Oculus(MDApp):
	def build(self):
		self.theme_cls.primary_palette = "Blue"
		Window.bind(on_keyboard = self.events)
		
		try:
			with open("data/UserData.json", "r") as data:
				self.data = json.load(data)
		except FileNotFoundError:
			with open("data/UserData.json", "x") as file:
				self.data = {}
				json.dump(self.data, file, indent = 4)
		
		try:
			with open("data/AppData.json", "r") as file:
				self.app_data = json.load(file)
				self.screen_order = self.app_data["Screen Order"]
		except:
			with open("data/AppData.json", "x") as file:
				self.app_data = {"Screen Order" : []}
				self.screen_order = []
				json.dump(self.app_data, file, indent = 4)
		
		
		# Register different fonts
		fonts = ['ConfessionRegular.ttf', 'CabalBold.ttf', 'AovelSans.ttf', 'Cabal.ttf', 'Nasa21.ttf', 'Paul.ttf', 'ConfessionFullRegular.ttf', "Aquire.otf", "AquireBold.otf", "AquireLight.otf"]
		for font in fonts:
			LabelBase.register(name = font[:-4], fn_regular = f"utils/fonts/{font}")
			
		# Define colors
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
		# Parse app data
		self.parse_app_data()
	
	
	# Function to add a Project Container		
	def add_container(self, title, date, works_in_progress, work_to_do):
		project_library = self.root.get_screen('main').ids.project_library
		project_library.add_widget(ProjectContainer(title = title, date = date, wip = works_in_progress, wtd = work_to_do, id = title))
		self.root.add_widget(BoardScreen(name = title, title = title))
	
	
	# Add Card Categories
	def add_card_category(self, screen_name, category_name):
		category_container = self.root.get_screen(screen_name).ids.card_category_container
		category_container.add_widget(CardCategory(id = category_name))
		
	
	def calculate_days(self, due_list):
		'''
		A Function that calculates the number of days of a card from today and the due date of the card itself.
		Returns the color foe the card border.
		'''
		
		day, month, year = due_list
		
		due = date(year, month, day)
		today = date.today()
		days = due - today
		days = days.days
		
		if days >= 14:
			color = (47/255, 219/255, 24/255, 1)
		elif days >= 7:
			color = (252/255, 111/255, 3/255, 1)
		elif days >= 0:
			color = (1, 23/255, 23/255, 1)
		elif days < 0:
			color = (253/255, 154/255, 162/255, 1)
		return color
				
			

			
						
												
	# Add Kanban Cards
	def add_cards(self, screen_name, container_name, title, task, due, categories):
		card_container = self.root.get_screen(screen_name).ids.card_category_container.children
		
		color = list(map(int, due.split("-")))
		color = self.calculate_days(color)
		
		for child in card_container:
			if child.id == container_name:
				child.ids.cards.add_widget(KanbanCard(title = title, task = task, categories = categories, due_date = due, color = color))
		
	
	
	def events(self, instance, keyboard, keycode, text, modifiers):
		'''Called when buttons are pressed on the mobile device.'''
		if keyboard in (1001, 27):
			# Back
			if self.root.current != "main":
				self.root.current = "main"
			
	
		
			
				
						
	# Function to parse App data
	def parse_app_data(self):
		board_screens = 1
		for project in self.screen_order:
			self.no_of_categories = 0
			data = self.data[project]
			project_due = data["Due Date"]
			card_categories = data["Card Categories"]
			wip = str(len(card_categories["In Progress"]))
			wtd = str(len(card_categories["Backlog"]))
			
			# Add the project containers
			self.add_container(project, project_due, wip, wtd)
			for category_name, cards in card_categories.items():
				self.no_of_categories += 1
				self.add_card_category(project, category_name)
				for card in cards:
					self.add_cards(project, category_name, card["Title"], card["task"], '-'.join(list(map(str, card['due date']))), len(card_categories.keys()))

	
		
			
				
						
	# Update main screen
	def refresh_main(self):
		library = self.root.ids.main_screen.ids.project_library
		library.clear_widgets()
		with open("data/AppData.json", "w") as file:
			json.dump(self.app_data, file, indent = 4)
		for project in self.screen_order:
			data = self.data[project]
			project_due = data["Due Date"]
			card_categories = data["Card Categories"]
			wip = str(len(card_categories["In Progress"]))
			wtd = str(len(card_categories["Backlog"]))
			
			# Add the project containers
			library.add_widget(ProjectContainer(title = project, date = project_due, wip = wip, wtd = wtd, id = project))

	
		
			
				
						
	
	# Add Card Dialog Function
	def add_card_dialog(self):
		board = self.root.current
		card_categories = list(self.data[board]["Card Categories"].keys())
		dialog = MDDialog(
				title="Add Card",
				text = "In which Caegory do you want to add a card?",
				type="simple",
				items=[
					AddCardDialogItem(text="Backlog", icon="update"),
					AddCardDialogItem(text="In Progress", icon="progress-check"),
					AddCardDialogItem(text="Done", icon="check-all"),
					],
				buttons=[
					MDRaisedButton(text="DISCARD"),
				],
					)
		button = dialog.buttons[0]
		dialog.size_hint = (None, 1)
		dialog.width = 1000
		button.on_press = dialog.dismiss
		dialog.open()
	

	

		
						
				
	# New project dialog
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
		self.add_project_dialog.buttons[1].on_press = self.create_new_project
		self.add_project_dialog.open()	
		due_date = date.today()
		self.new_project_due = '-'.join(list(map(str, [due_date.day, due_date.month, due_date.year])))
	

	
		
			
				
					
							
	
	# Add Project
	def create_new_project(self):
		new_project_name = self.add_project_dialog.children[0].children[2].children[0].ids.new_project_name.text.strip()
		
		if new_project_name not in self.data.keys():
			if new_project_name.strip() != "":
				
				self.add_project_dialog.dismiss()
				self.data[new_project_name] = { "Card Categories": {"Backlog": [], "In Progress": [], "Done": []}, "Due Date": self.new_project_due, "WIP Limit": 3}
				with open("data/UserData.json", "w") as file:
					json.dump(self.data, file, indent = 4)
				self.screen_order.append(new_project_name)
				with open("data/AppData.json", "w") as file:
					json.dump(self.app_data, file, indent = 4)
				
				
				self.add_container(new_project_name, self.new_project_due, "0", "0")
				for category in self.data[new_project_name]["Card Categories"].keys():
					if category == "Backlog" or category == "In Progress" or category == "Done":
						self.add_card_category(new_project_name, category)
			else:
				Snackbar(text = "Please enter a Project Name!").show()
		else:
			Snackbar(text = "This Project already exists!").show()
			
	# Add project due date
	def add_project_due(self):
		
		def get_date(due_date):
			self.new_project_due = '-'.join(list(map(str, [due_date.day, due_date.month, due_date.year])))
			
		date_dialog = MDDatePicker(callback = get_date)
		date_dialog.open()

		
				
						
								
												
	
	
	#Add Card
	def add_card(self, instance):
		today = date.today()
		self.new_card_due = list(map(int, [today.day, today.month, today.year]))
		category = instance.text
		terminated = False
		# Check if WIP limit will be crossed
		if category == "In Progress":
			wip = len(self.data[self.root.current]["Card Categories"]["In Progress"])
			
			if wip + 1 > self.data[self.root.current]["WIP Limit"]:
				
				limit = self.data[self.root.current]["WIP Limit"]
				limit_crossed_dialog = MDDialog(
					title="WIP Limit croosed",
					text=f"You had set the 'Works in Progress' limit as {limit}. \nOne of the main rules of kanban is that you stick to the limit. Change limit to add more cards.",
					buttons=[
						MDFlatButton(text="OK", text_color=self.theme_cls.primary_color)]
				)
			
				limit_crossed_dialog.size_hint = (None, 1)
				limit_crossed_dialog.width = 1000
				
				limit_crossed_dialog.buttons[0].on_press = limit_crossed_dialog.dismiss
				terminated = True
				limit_crossed_dialog.open()
		
		if terminated:
			return
		add_card_dialog = MDDialog(
			title="Create Card",
			type="custom",
			content_cls = AddCardContent(),
			buttons=[
				MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
				MDFlatButton(text="CREATE", text_color=self.theme_cls.primary_color)
			],
		)
		add_card_dialog.size_hint = (None, 1)
		add_card_dialog.width = 1000
		add_card_dialog.buttons[0].on_press = add_card_dialog.dismiss
		add_card_dialog.open()
		
		
		def create_card():
			title_field = add_card_dialog.children[0].children[2].children[0].ids.title
			task_field = add_card_dialog.children[0].children[2].children[0].ids.task
			
			title = title_field.text.strip()
			task = task_field.text.strip()
			
			if title.strip() != "" and task.strip() != "":
				add_card_dialog.dismiss()
				
				card_in_data = {"Title": title,
				"task": task,
				"due date": self.new_card_due}
				
				self.data[self.root.current]["Card Categories"][category].append(card_in_data)
				self.add_cards(self.root.current, category, title, task, "-".join(list(map(str, self.new_card_due))), len(self.data[self.root.current]["Card Categories"].keys()))
				with open("data/UserData.json", "w") as file:
					json.dump(self.data, file, indent = 4)
				
				
			else:
				if title.strip() == "":
					Snackbar(text="Please enter a Title!").show()
				
				elif task.strip() == "":
					Snackbar(text="Please enter a Task!").show()
		
		
		add_card_dialog.buttons[1].on_press = create_card

		
				
						
										
		
	
	# Add card due date
	def add_card_due(self):
		
		def get_date(due_date):
			self.new_card_due = list(map(int, [due_date.day, due_date.month, due_date.year]))
			
		date_dialog = MDDatePicker(callback = get_date)
		date_dialog.open()
	
	
	def set_card_due(self, open_date_card):
		open_date = open_date_card[0]['due date']
		def get_time(return_date):
			self.edit_card_due = '-'.join(list(map(str, [return_date.day, return_date.month, return_date.year])))
			open_date_card[0]['due date'] = [return_date.day, return_date.month, return_date.year]
			with open("data/UserData.json", "w") as file:
				json.dump(self.data, file, indent = 4)
		try:			
			date_dialog = MDDatePicker(callback = get_time, day = open_date[0], month = open_date[1], year = open_date[2])
			date_dialog.open()
		except Exception as e:
			date_dialog = MDDatePicker(callback = get_time)
			date_dialog.open()

	

	
		
				
	
	# Kanban Card Settings
	def card_settings(self, instance, other = None):
		task = instance.text
		card_dialog = instance.parent.parent.parent.parent
		card = card_dialog.card
		cards_in_same = self.data[self.root.current]["Card Categories"][card.parent.parent.parent.id]
		card_in_data= [i for i in cards_in_same if i["Title"] == card.title]
		self.card_due = card_in_data
		
		def delete_card():
			cards = self.data[self.root.current]["Card Categories"][card.parent.parent.parent.id]
			cards = [i for i in cards if i["Title"] != card.title]
			self.data[self.root.current]["Card Categories"][card.parent.parent.parent.id] = cards
			delete_confirm_dialog.dismiss()
			with open("data/UserData.json", "w") as file:
				json.dump(self.data, file, indent = 4)
			card.parent.remove_widget(card)
		
		
		def edit_card():
			self.edit_card_due = card.due_date
			print(len(card.title))
			if len(card.title) < 10:
				display_title = card.title
				print(1)
			else:
				print(2)
				display_title = card.title[:10] + '\n' + card.title[10:]
				print(display_title)
			edit_card_dialog = MDDialog(
				title="Edit Card\n" + display_title,
				type="custom",
				content_cls=CardSettingsContent(task = card.task, title = card.title),
				buttons=[
					MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
					MDFlatButton(text="OK", text_color=self.theme_cls.primary_color)
				],
			)
			edit_card_dialog.size_hint = (None, 1)
			edit_card_dialog.width = 1000
			edit_card_dialog.buttons[0].on_press = edit_card_dialog.dismiss
			edit_card_dialog.open()
			
			def get_edit():
				new_title = edit_card_dialog.children[0].children[2].children[0].ids.new_title.text
				new_task = edit_card_dialog.children[0].children[2].children[0].ids.new_task.text
				
				# Change card properties
				card.title = new_title
				card.task = new_task
				card.due_date = self.edit_card_due
				card.color = self.calculate_days(list(map(int, card.due_date.split("-"))))
				self.move_card(card.parent.parent.parent.id, card, card.parent.parent.parent.id)
				
				edit_card_dialog.dismiss()
				
				# Change card properties in user data
				card_in_data[0]["Title"] = card.title
				card_in_data[0]["task"] = card.task
				with open("data/UserData.json", "w") as file:
					json.dump(self.data, file, indent = 4)
			
			edit_card_dialog.buttons[1].on_press = get_edit
		
		if task == "Edit Card":
			edit_card()
			
		elif task == "Delete Card":
			delete_confirm_dialog = MDDialog(
				title=f"Delete Card {card.title}?",
				text="Changes done cannot be undone.",
				buttons=[
					MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
					MDFlatButton(text="DELETE", text_color=self.theme_cls.primary_color)])
			
			delete_confirm_dialog.size_hint = (None, 1)
			delete_confirm_dialog.width = 1000
			delete_confirm_dialog.buttons[0].on_press = delete_confirm_dialog.dismiss
			delete_confirm_dialog.buttons[1].on_press = delete_card
			delete_confirm_dialog.open()





	
	
	# Move Cards to next category
	def move_card(self, instance, card, category):
		terminated = False
		# Check if the category is In progress and this transfer will cause to crosss the wip limit
		if instance == "In Progress":
			wip = len(self.data[self.root.current]["Card Categories"]["In Progress"])
			
			if wip + 1 > self.data[self.root.current]["WIP Limit"]:
				limit = self.data[self.root.current]["WIP Limit"]
				limit_crossed_dialog = MDDialog(
					title="WIP Limit croosed",
					text=f"You had set the 'Works in Progress' limit as {limit}. \nOne of the main rules of kanban is that you stick to the limit. Change limit to add more cards.",
					buttons=[
						MDFlatButton(text="OK", text_color=self.theme_cls.primary_color)]
				)
				limit_crossed_dialog.size_hint = (None, 1)
				limit_crossed_dialog.width = 1000
				
				limit_crossed_dialog.buttons[0].on_press = limit_crossed_dialog.dismiss
				limit_crossed_dialog.open()
				return
				
		
		# Move graphical card from card container to another
		self.add_cards(self.root.current, instance, card.title, card.task, card.due_date, 3)
		card.parent.remove_widget(card)
		
		# Change data
			# Delete card from current category
		card_in_category = self.data[self.root.current]["Card Categories"][category]
		self.data[self.root.current]["Card Categories"][category] = [i for i in card_in_category if i["Title"] != card.title]
			
			# Add Card to new category
		card_in_data = card_in_data = {"Title": card.title,
				"task": card.task,
				"due date": card.due_date.split("-")}
		self.data[self.root.current]["Card Categories"][instance].append(card_in_data)
		with open("data/UserData.json", "w") as file:
			json.dump(self.data, file, indent = 4)
		
	
	
	
	
	
	
	
	# Function to control board settings
	def board_settings(self, instance):
		open_project = self.root.current
		wip_num = 5
		def set_wip():
			wip_dialog.dismiss()
			def set():
				wip_confirm.dismiss()
				self.data[open_project]["WIP Limit"] = wip_num
				with open("data/UserData.json", "w") as file:
					json.dump(self.data, file, indent = 4)
				self.refresh_main()

			
			wip_num = wip_dialog.children[0].children[2].children[0].ids.text_field.text
			try:
				wip_num = int(wip_num)
				wip_confirm = MDDialog(
					title=f"Set Works in progress limit as {wip_num}?",
					buttons=[
						MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
						MDFlatButton(text="CONFIRM", text_color=self.theme_cls.primary_color)]
				)
			
				wip_confirm.size_hint = (None, 1)
				wip_confirm.width = 1000
				wip_confirm.buttons[0].on_press = wip_confirm.dismiss
				wip_confirm.buttons[1].on_press = set
				wip_confirm.open()
					
			except ValueError:
				wip_dialog.children[0].children[2].children[0].ids.text_field.error = True
				wip_dialog.children[0].children[2].children[0].ids.text_field.hint_text = "Please enter a number"
			
		
		
		def delete_project():
			delete_confirm_dialog.dismiss()
			target = open_project
			self.remove_container(target)
			self.data = {k:v for k,v in self.data.items() if k != target}
			self.screen_order.remove(target)
			with open("data/UserData.json", "w") as file:
				json.dump(self.data, file, indent = 4)
			with open("data/AppData.json", "w") as file:
				json.dump(self.app_data, file, indent = 4)
			self.root.current = 'main'
		
		def rename_project(open_project):
			
			rename_dialog = MDDialog(
				title="Rename Project",
				type="custom",
				content_cls=Content(hint = "New Project Name"),
				buttons=[
					MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
					MDFlatButton(text="RENAME", text_color=self.theme_cls.primary_color),
				],
			)
			rename_dialog.size_hint = (None, 1)
			rename_dialog.width = 1000
			rename_dialog.open()
			
				
			
			def get_text():
				text = rename_dialog.children[0].children[2].children[0].ids.text_field.text.strip()
				if len(text) <= 17:
					sample = {k:v for k,v in self.data.items() if k != open_project}		

					if text in sample.keys():
						rename_dialog.children[0].children[2].children[0].ids.text_field.error = True
						rename_dialog.children[0].children[2].children[0].ids.text_field.hint_text = "Project already exists!"
					else:
						self.data = {text if k == open_project else k:v for k,v in self.data.items()}
						with open("data/UserData.json", "w") as file:
							json.dump(self.data, file, indent = 4)
						
						self.app_data["Screen Order"] = [text if i == open_project else i for i in self.screen_order]
						self.screen_order = [text if i == open_project else i for i in self.screen_order]
						with open("data/AppData.json", "w") as file:
							json.dump(self.app_data, file, indent = 4)
						self.refresh_main()
						rename_dialog.dismiss()
						self.root.get_screen(open_project).title = text
						self.root.get_screen(open_project).name = text
							
				
			rename_dialog.buttons[1].on_press = get_text
			rename_dialog.buttons[0].on_press = rename_dialog.dismiss
		
		if instance.text == "Rename Project":
			rename_project(open_project)
		elif instance.text == "Delete Project":
			delete_confirm_dialog = MDDialog(
					title="Delete Project?",
					text="Changes done cannot be undone.",
					buttons=[
						MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
						MDFlatButton(text="CONFIRM", text_color=self.theme_cls.primary_color)]
				)
			
			delete_confirm_dialog.size_hint = (None, 1)
			delete_confirm_dialog.width = 1000
			delete_confirm_dialog.buttons[0].on_press = delete_confirm_dialog.dismiss
			delete_confirm_dialog.buttons[1].on_press = delete_project
			delete_confirm_dialog.open()
		
		elif instance.text == "Set 'Works in progress' limit":
			wip_dialog = MDDialog(
				title="Set WIP",
				type="custom",
				content_cls=Content(hint = "New 'Works in progress' limit", text = str(self.data[open_project]["WIP Limit"])),
				buttons=[
					MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color),
					MDFlatButton(text="SET", text_color=self.theme_cls.primary_color),
				],
			)
			wip_dialog.buttons[0].on_press = wip_dialog.dismiss
			wip_dialog.buttons[1].on_press = set_wip
			wip_dialog.size_hint = (None, 1)
			wip_dialog.width = 1000
			wip_dialog.open()
	
	
	# Remove project container
	def remove_container(self, title):
		lib = self.root.ids.main_screen.ids.project_library
		for container in lib.children:
			if container.title == title:
				container.remove()
		
			
		
		
	
	

	
if __name__ == "__main__":
	Oculus().run()
