from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import equations
def check_float(checkfloat):
		try:
			float(checkfloat)
			return True
		except ValueError:
			return False

class main_window_class:
	def __init__(self, master, conn):
		#Setting up tkinter window
		self.master = master
		self.conn = conn
		self.master.geometry('900x900')
		self.master.title('Hudsen System')
		#self.master.resizable(height = False, width = False)


		#Sqlite3 database configurations
		self.c = self.conn.cursor()
		self.c.execute('CREATE TABLE IF NOT EXISTS saveList(tableName TEXT, value INT, description TEXT)')
		self.c.execute('CREATE TABLE IF NOT EXISTS settings(settingName TEXT, settingValue INT, settingText TEXT)')

		#savelist check
		self.c.execute('SELECT * FROM saveList WHERE value = ?', [1])

		if self.c.fetchall() == []:
			self.c.execute('INSERT INTO saveList(tableName, value, description) VALUES(?, ?, ?)', ["rating_data", 1, "Default location where players and their ratings are stored"])
			self.c.execute('CREATE TABLE IF NOT EXISTS rating_data(tableName TEXT, tableNum INT, nametype1 TEXT, nametype2 TEXT, teamtype1 TEXT, teamtype2 TEXT, description TEXT, rating TEXT)')
			self.c.execute('INSERT INTO rating_data(tableName, tableNum, nametype1, nametype2, teamtype1, teamtype2,description, rating) VALUES (?,?,?,?,?,?,?,?)', ["autosave.tb", 1, "Table", "Table", "Table","Table","Table","Table"])
			self.conn.commit()
		else:
			pass

		#settings check
		self.c.execute('SELECT * FROM settings WHERE settingName = ?', ["a_value"])

		if self.c.fetchall() == []:
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["a_value", 0.0065, ""])
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["selected_table", 1, ""])
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["name_type_1_title", 1, "UUID"])
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["name_type_2_title", 1, "Name"])
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["team_type_1_title", 1, "House"])
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["team_type_2_title", 1, "Grade"])
			self.c.execute('INSERT INTO settings(settingName, settingValue, settingText) VALUES(?, ?, ?)', ["startingrating", 1000, ""])
			self.conn.commit()
		else:
			pass

		#changes depending on settings
		self.c.execute('SELECT settingValue FROM settings WHERE settingName = "selected_table"')
		self.c.execute('SELECT tableName FROM rating_data WHERE  tableNum= ?', [self.c.fetchall()[0][0]])
		self.current_table = f"{self.c.fetchall()[0][0]}"
		self.master.title(f"Hudsen System - file: {self.current_table}")

		self.c.execute('SELECT settingText FROM settings WHERE settingName = "name_type_1_title"')
		self.name_type_1_title = self.c.fetchall()[0][0]
		self.c.execute('SELECT settingText FROM settings WHERE settingName = "name_type_2_title"')
		self.name_type_2_title = self.c.fetchall()[0][0]
		self.c.execute('SELECT settingText FROM settings WHERE settingName = "team_type_1_title"')
		self.team_type_1_title = self.c.fetchall()[0][0]
		self.c.execute('SELECT settingText FROM settings WHERE settingName = "team_type_2_title"')
		self.team_type_2_title = self.c.fetchall()[0][0]
		self.c.execute('SELECT settingValue FROM settings WHERE settingName = "a_value"')
		self.a = self.c.fetchall()[0][0]
		self.c.execute('SELECT settingValue FROM settings WHERE settingName = "startingrating"')
		self.startingrating = self.c.fetchall()[0][0]


		#Defining variables
		self.mode_options = ["Competitors", "Enter Scores", "Database", "Settings"]
		self.current_selection = -1
		self.e = 2.71828
		

		
		
		#Defining elements of window
		self.separator = ttk.Separator(self.master, orient="horizontal")
		self.separator.place(rely = 0.06, relwidth = 1)

		self.scrollbar = Scrollbar(self.master)
		self.scrollbar.pack(side=RIGHT, fill = BOTH)

		self.business_title = Label(self.master, text = "Chess Rating Ranker", font = ("Arial",35))
		self.business_title.place(anchor = W, relx = 0.01, rely = 0.025)


		self.mode_label = Label(self.master, text = "Mode:", font=("Arial", 25))
		self.mode_label.place(anchor = CENTER, relx = 0.75, rely=0.025)

		self.mode_variable = StringVar(self.master)
		self.mode_variable.set("<Choose Mode>")
		self.window_mode = OptionMenu(self.master, self.mode_variable, *self.mode_options)
		self.window_mode.place(anchor=E, relx = 0.98, rely = 0.025)
		self.window_mode.config(font=("Arial", 17))
		self.mode_variable.trace("w", self.change_mode)

	
		self.table_button = Button(self.master, text = f'{self.current_table}', font=("Arial", 25))
		self.table_button.place(anchor = CENTER, relx = 0.6, rely=0.025)

		

		#Competitors Elements
		self.competitors_frame = LabelFrame(self.master, text = "Competitors", width = 850, height = 830, font=("Arial",30))

		self.competitors_frame_nametype1_label1 = Label(self.competitors_frame, text = self.name_type_1_title, font='Courier 18 bold')
		self.competitors_frame_nametype1_label1.place(anchor= CENTER, relx =0.1, rely=0.01)

		self.competitors_frame_nametype2_label1 = Label(self.competitors_frame, text = self.name_type_2_title, font='Courier 18 bold')
		self.competitors_frame_nametype2_label1.place(anchor= CENTER, relx =0.3, rely=0.01)

		self.competitors_frame_teamtype1_label1 = Label(self.competitors_frame, text = self.team_type_1_title, font='Courier 18 bold')
		self.competitors_frame_teamtype1_label1.place(anchor= CENTER, relx =0.5, rely=0.01)

		self.competitors_frame_teamtype2_label1 = Label(self.competitors_frame, text = self.team_type_2_title, font='Courier 18 bold')
		self.competitors_frame_teamtype2_label1.place(anchor= CENTER, relx =0.7, rely=0.01)

		self.competitors_frame_nametype1_entrybox1 = Entry(self.competitors_frame, text = self.name_type_1_title, font='Courier 15', width=17)
		self.competitors_frame_nametype1_entrybox1.place(anchor= CENTER, relx =0.1, rely=0.05)
		self.competitors_frame_ignore_nametype1 = False

		self.competitors_frame_nametype2_entrybox1 = Entry(self.competitors_frame, text = self.name_type_2_title, font='Courier 15', width=17)
		self.competitors_frame_nametype2_entrybox1.place(anchor= CENTER, relx =0.3, rely=0.05)

		self.competitors_frame_teamtype1_entrybox1 = Entry(self.competitors_frame, text = self.team_type_1_title, font='Courier 15', width=17)
		self.competitors_frame_teamtype1_entrybox1.place(anchor= CENTER, relx =0.5, rely=0.05)

		self.competitors_frame_teamtype2_entrybox1 = Entry(self.competitors_frame, text = self.team_type_2_title, font='Courier 15', width=17)
		self.competitors_frame_teamtype2_entrybox1.place(anchor= CENTER, relx =0.7, rely=0.05)

		self.competitors_frame_nametype2_entrybox1.config(state = DISABLED)
		self.competitors_frame_teamtype1_entrybox1.config(state = DISABLED)
		self.competitors_frame_teamtype2_entrybox1.config(state = DISABLED)

		self.competitors_frame_save_button = Button(self.competitors_frame, text = "Save",font='Courier 15 bold', command = self.competitors_frame_save_button_command)
		self.competitors_frame_save_button.place(anchor= CENTER, relx =0.85, rely=0.05)

		self.competitors_frame_remove_button = Button(self.competitors_frame, text = "Remove",font='Courier 15 bold', command = self.competitors_frame_delete)
		self.competitors_frame_remove_button.place(anchor= CENTER, relx =0.9425, rely=0.05)



		self.competitors_frame_nametype1_label2 = Label(self.competitors_frame, text = self.name_type_1_title, font='Courier 18 bold')
		self.competitors_frame_nametype1_label2.place(anchor= CENTER, relx =0.1, rely=0.1)

		self.competitors_frame_nametype2_label2 = Label(self.competitors_frame, text = self.name_type_2_title, font='Courier 18 bold')
		self.competitors_frame_nametype2_label2.place(anchor= CENTER, relx =0.3, rely=0.1)

		self.competitors_frame_teamtype1_label2 = Label(self.competitors_frame, text = self.team_type_1_title, font='Courier 18 bold')
		self.competitors_frame_teamtype1_label2.place(anchor= CENTER, relx =0.5, rely=0.1)

		self.competitors_frame_teamtype2_label2 = Label(self.competitors_frame, text = self.team_type_2_title, font='Courier 18 bold')
		self.competitors_frame_teamtype2_label2.place(anchor= CENTER, relx =0.7, rely=0.1)

		self.competitors_frame_rating_label = Label(self.competitors_frame, text = "Rating", font='Courier 18 bold')
		self.competitors_frame_rating_label.place(anchor= CENTER, relx =0.9, rely=0.1)

		self.competitors_frame_nametype1_listbox = Listbox(self.competitors_frame, font='Courier 12 bold', height=48, width = 23)
		self.competitors_frame_nametype1_listbox.place(anchor= N, relx =0.1, rely=0.12)
		self.competitors_frame_nametype1_listbox.config(justify = CENTER)

		self.competitors_frame_nametype2_listbox = Listbox(self.competitors_frame, font='Courier 12 bold', height=48, width = 23)
		self.competitors_frame_nametype2_listbox.place(anchor= N, relx =0.3, rely=0.12)
		self.competitors_frame_nametype2_listbox.config(justify = CENTER)

		self.competitors_frame_teamtype1_listbox = Listbox(self.competitors_frame, font='Courier 12 bold', height=48, width = 23)
		self.competitors_frame_teamtype1_listbox.place(anchor= N, relx =0.5, rely=0.12)
		self.competitors_frame_teamtype1_listbox.config(justify = CENTER)

		self.competitors_frame_teamtype2_listbox = Listbox(self.competitors_frame, font='Courier 12 bold', height=48, width = 23)
		self.competitors_frame_teamtype2_listbox.place(anchor= N, relx =0.7, rely=0.12)
		self.competitors_frame_teamtype2_listbox.config(justify = CENTER)

		self.competitors_frame_rating_listbox = Listbox(self.competitors_frame, font='Courier 12 bold', height=48, width = 23)
		self.competitors_frame_rating_listbox.place(anchor= N, relx =0.9, rely=0.12)
		self.competitors_frame_rating_listbox.config(justify = CENTER)


		#Enter Scores Elements
		self.enter_scores_frame = LabelFrame(self.master, text = "Enter Scores", width = 875, height = 830, font=("Arial", 30))

		self.enter_scores_frame_label1 = Label(self.enter_scores_frame, text = 'Player A', font=("Arial", 25))
		self.enter_scores_frame_label1.place(anchor = CENTER, relx = 1/6, rely= 0.05)
		self.enter_scores_frame_label2 = Label(self.enter_scores_frame, text = 'Player B', font=("Arial", 25))
		self.enter_scores_frame_label2.place(anchor = CENTER, relx = 1/2, rely= 0.05)
		self.enter_scores_frame_label3 = Label(self.enter_scores_frame, text = 'Outcome', font=("Arial", 25))
		self.enter_scores_frame_label3.place(anchor = CENTER, relx = 5/6, rely= 0.05)
		self.enter_scores_frame_label4 = Label(self.enter_scores_frame, text = 'VS', font=("Arial", 25))
		self.enter_scores_frame_label4.place(anchor = CENTER, relx = 1/3, rely= 0.05)

		self.enter_scores_frame_playerA_entry = Entry(self.enter_scores_frame, width = 25, font = ("Arial", 18))
		self.enter_scores_frame_playerA_entry.place(anchor=CENTER, relx = 1/6, rely = 0.1)
		self.enter_scores_frame_playerB_entry = Entry(self.enter_scores_frame, width = 25, font = ("Arial", 18))
		self.enter_scores_frame_playerB_entry.place(anchor=CENTER, relx = 1/2, rely = 0.1)
		self.enter_scores_frame_playerB_entry.config(state=DISABLED)
		self.enter_scores_frame_outcome_button = Button(self.enter_scores_frame, width = 20, font = ("Arial", 18))
		self.enter_scores_frame_outcome_button.place(anchor=CENTER, relx = 5/6, rely = 0.1)

		self.enter_scores_frame_playerA_labelframe = LabelFrame(self.enter_scores_frame,text="Player A", width = 275, height= 600, font = ("Arial", 18))
		self.enter_scores_frame_playerA_labelframe.place(anchor = N, relx = 1/6, rely = 0.13)
		self.enter_scores_frame_playerB_labelframe = LabelFrame(self.enter_scores_frame,text="Player B", width = 275, height= 600, font = ("Arial", 18))
		self.enter_scores_frame_playerB_labelframe.place(anchor = N, relx = 1/2, rely = 0.13)
		self.enter_scores_frame_outcomeframe = LabelFrame(self.enter_scores_frame,text="Outcome", width = 275, height= 600, font = ("Arial", 18))
		self.enter_scores_frame_outcomeframe.place(anchor = N, relx = 5/6, rely = 0.13)

		self.enter_scores_frame_playerA_nametype1 = Label(self.enter_scores_frame_playerA_labelframe, text = f'{self.name_type_1_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerA_nametype1.place(anchor=CENTER, relx = 0.5, rely = 0.05)

		self.enter_scores_frame_playerA_nametype1_value=Button(self.enter_scores_frame_playerA_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerA_nametype1_value.place(anchor = CENTER, relx = 0.5, rely = 0.11)

		self.enter_scores_frame_playerA_nametype2 = Label(self.enter_scores_frame_playerA_labelframe, text = f'{self.name_type_2_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerA_nametype2.place(anchor=CENTER, relx = 0.5, rely = 0.2)

		self.enter_scores_frame_playerA_nametype2_value=Button(self.enter_scores_frame_playerA_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerA_nametype2_value.place(anchor = CENTER, relx = 0.5, rely = 0.26)

		self.enter_scores_frame_playerA_teamtype1 = Label(self.enter_scores_frame_playerA_labelframe, text = f'{self.team_type_1_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerA_teamtype1.place(anchor=CENTER, relx = 0.5, rely = 0.35)

		self.enter_scores_frame_playerA_teamtype1_value=Button(self.enter_scores_frame_playerA_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerA_teamtype1_value.place(anchor = CENTER, relx = 0.5, rely = 0.41)

		self.enter_scores_frame_playerA_teamtype2 = Label(self.enter_scores_frame_playerA_labelframe, text = f'{self.team_type_2_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerA_teamtype2.place(anchor=CENTER, relx = 0.5, rely = 0.5)

		self.enter_scores_frame_playerA_teamtype2_value=Button(self.enter_scores_frame_playerA_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerA_teamtype2_value.place(anchor = CENTER, relx = 0.5, rely = 0.56)

		self.enter_scores_frame_playerA_oldrating = Label(self.enter_scores_frame_playerA_labelframe, text = f'Current Rating:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerA_oldrating.place(anchor=CENTER, relx = 0.5, rely = 0.65)

		self.enter_scores_frame_playerA_oldrating_value=Button(self.enter_scores_frame_playerA_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerA_oldrating_value.place(anchor = CENTER, relx = 0.5, rely = 0.71)

		self.enter_scores_frame_playerA_newrating = Label(self.enter_scores_frame_playerA_labelframe, text = f'New Rating:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerA_newrating.place(anchor=CENTER, relx = 0.5, rely = 0.8)

		self.enter_scores_frame_playerA_newrating_value=Button(self.enter_scores_frame_playerA_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerA_newrating_value.place(anchor = CENTER, relx = 0.5, rely = 0.86)



		self.enter_scores_frame_playerB_nametype1 = Label(self.enter_scores_frame_playerB_labelframe, text = f'{self.name_type_1_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerB_nametype1.place(anchor=CENTER, relx = 0.5, rely = 0.05)

		self.enter_scores_frame_playerB_nametype1_value=Button(self.enter_scores_frame_playerB_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerB_nametype1_value.place(anchor = CENTER, relx = 0.5, rely = 0.11)

		self.enter_scores_frame_playerB_nametype2 = Label(self.enter_scores_frame_playerB_labelframe, text = f'{self.name_type_2_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerB_nametype2.place(anchor=CENTER, relx = 0.5, rely = 0.2)

		self.enter_scores_frame_playerB_nametype2_value=Button(self.enter_scores_frame_playerB_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerB_nametype2_value.place(anchor = CENTER, relx = 0.5, rely = 0.26)

		self.enter_scores_frame_playerB_teamtype1 = Label(self.enter_scores_frame_playerB_labelframe, text = f'{self.team_type_1_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerB_teamtype1.place(anchor=CENTER, relx = 0.5, rely = 0.35)

		self.enter_scores_frame_playerB_teamtype1_value=Button(self.enter_scores_frame_playerB_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerB_teamtype1_value.place(anchor = CENTER, relx = 0.5, rely = 0.41)

		self.enter_scores_frame_playerB_teamtype2 = Label(self.enter_scores_frame_playerB_labelframe, text = f'{self.team_type_2_title}:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerB_teamtype2.place(anchor=CENTER, relx = 0.5, rely = 0.5)

		self.enter_scores_frame_playerB_teamtype2_value=Button(self.enter_scores_frame_playerB_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerB_teamtype2_value.place(anchor = CENTER, relx = 0.5, rely = 0.56)

		self.enter_scores_frame_playerB_oldrating = Label(self.enter_scores_frame_playerB_labelframe, text = f'Current Rating:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerB_oldrating.place(anchor=CENTER, relx = 0.5, rely = 0.65)

		self.enter_scores_frame_playerB_oldrating_value=Button(self.enter_scores_frame_playerB_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerB_oldrating_value.place(anchor = CENTER, relx = 0.5, rely = 0.71)

		self.enter_scores_frame_playerB_newrating = Label(self.enter_scores_frame_playerB_labelframe, text = f'New Rating:', font=("Arial BOLD", 24))
		self.enter_scores_frame_playerB_newrating.place(anchor=CENTER, relx = 0.5, rely = 0.8)

		self.enter_scores_frame_playerB_newrating_value=Button(self.enter_scores_frame_playerB_labelframe, text = "", font = ("Arial", 20))
		self.enter_scores_frame_playerB_newrating_value.place(anchor = CENTER, relx = 0.5, rely = 0.86)



		self.enter_scores_frame_playerA_win_button = Button(self.enter_scores_frame_outcomeframe, text="Player A\nWon", width=15, height =5, font = ("Arial", 20), command = self.enter_scores_frame_playerA_win_command)
		self.enter_scores_frame_playerA_win_button.place(anchor=CENTER, relx = 0.5, rely = 0.15)
		self.enter_scores_frame_draw_button = Button(self.enter_scores_frame_outcomeframe, text="Draw", width=15, height =5, font = ("Arial", 20), command = self.enter_scores_frame_draw_command)
		self.enter_scores_frame_draw_button.place(anchor=CENTER, relx = 0.5, rely = 0.375)
		self.enter_scores_frame_playerB_win_button = Button(self.enter_scores_frame_outcomeframe, text="Player B\nWon", width=15, height =5, font = ("Arial", 20), command = self.enter_scores_frame_playerB_win_command)
		self.enter_scores_frame_playerB_win_button.place(anchor=CENTER, relx = 0.5, rely = 0.6)
		self.enter_scores_frame_playerB_win_button = Button(self.enter_scores_frame_outcomeframe, text="Submit", width=15, height =5, font = ("Arial", 20), command = self.enter_scores_frame_submit_command)
		self.enter_scores_frame_playerB_win_button.place(anchor=CENTER, relx = 0.5, rely = 0.825)
		



		

		#Database Elements
		self.database_frame = LabelFrame(self.master, text = "Database", width = 875, height = 830, font=("Arial", 30))

		self.database_frame_current_save = Label(self.database_frame, text=f"Current Save: {self.current_table}", font=("Arial", 25))
		self.database_frame_current_save.place(anchor=W, relx = 0.015, rely = 0.02)

		self.database_frame_list_box = Listbox(self.database_frame, width = 60, heigh = 25, font=("Arial", 25), yscrollcommand = self.scrollbar.set)
		self.database_frame_list_box.place(anchor=CENTER, relx = 0.5, rely = 0.51)

		self.database_frame_open_selected = Button(self.database_frame, text = "Open Selected", font=("Arial", 15), command = self.database_frame_open)
		self.database_frame_open_selected.place(anchor=W, relx = 0.35, rely = 0.02)

		self.database_frame_delete_selected = Button(self.database_frame, text = "Delete Selected", font=("Arial", 15), command = self.database_frame_delete)
		self.database_frame_delete_selected.place(anchor=W, relx = 0.51, rely = 0.02)

		self.database_frame_entry_box = Entry(self.database_frame, width = 20, font=("Arial", 15))
		self.database_frame_entry_box.place(anchor=W, relx = 0.67, rely = 0.02)

		self.database_frame_create_button = Button(self.database_frame, text="Create", font=("Arial", 15), command = self.bind_return)
		self.database_frame_create_button.place(anchor=W, relx = 0.89, rely = 0.02)
		self.database_frame_check_autosave()

		
		self.scrollbar.config(command=self.database_frame_list_box.yview)


		#Settings Elements
		self.settings_frame = LabelFrame(self.master, text = "Settings", width = 875, height = 830, font=("Arial", 30))

		self.settings_frame_label_avalue = Label(self.settings_frame, text = "A value", font = ("Arial", 20))
		self.settings_frame_label_avalue.place(anchor=W, relx = 0.05, rely = 0.05)
		self.settings_frame_label_nametype1 = Label(self.settings_frame, text = "Name Type 1", font = ("Arial", 20))
		self.settings_frame_label_nametype1.place(anchor=W, relx = 0.05, rely = 0.1)
		self.settings_frame_label_nametype2 = Label(self.settings_frame, text = "Name Type 2", font = ("Arial", 20))
		self.settings_frame_label_nametype2.place(anchor=W, relx = 0.05, rely = 0.15)
		self.settings_frame_label_teamtype1 = Label(self.settings_frame, text = "Team Type 1", font = ("Arial", 20))
		self.settings_frame_label_teamtype1.place(anchor=W, relx = 0.05, rely = 0.2)
		self.settings_frame_label_teamtype2 = Label(self.settings_frame, text = "Team Type 2", font = ("Arial", 20))
		self.settings_frame_label_teamtype2.place(anchor=W, relx = 0.05, rely = 0.25)
		self.settings_frame_label_startingrating = Label(self.settings_frame, text = "Starting Rating", font = ("Arial", 20))
		self.settings_frame_label_startingrating.place(anchor=W, relx = 0.05, rely = 0.3)

		self.settings_frame_entry_avalue = Entry(self.settings_frame, font = ("Arial", 18))
		self.settings_frame_entry_avalue.place(anchor =W, relx = 0.3, rely=0.05)
		self.settings_frame_entry_nametype1 = Entry(self.settings_frame, font = ("Arial", 18))
		self.settings_frame_entry_nametype1.place(anchor =W, relx = 0.3, rely=0.1)
		self.settings_frame_entry_nametype2 = Entry(self.settings_frame, font = ("Arial", 18))
		self.settings_frame_entry_nametype2.place(anchor =W, relx = 0.3, rely=0.15)
		self.settings_frame_entry_teamtype1 = Entry(self.settings_frame, font = ("Arial", 18))
		self.settings_frame_entry_teamtype1.place(anchor =W, relx = 0.3, rely=0.2)
		self.settings_frame_entry_teamtype2 = Entry(self.settings_frame, font = ("Arial", 18))
		self.settings_frame_entry_teamtype2.place(anchor =W, relx = 0.3, rely=0.25)
		self.settings_frame_entry_startingrating = Entry(self.settings_frame, font = ("Arial", 18))
		self.settings_frame_entry_startingrating.place(anchor =W, relx = 0.3, rely=0.3)

		self.settings_frame_submit_button = Button(self.settings_frame, text ="Submit/Save/Apply", command = self.settings_frame_submit_command, font = ("Arial", 20))
		self.settings_frame_submit_button.place(anchor = CENTER, relx = 0.5, rely = 0.9)

		self.settings_frame_label_success = Label(self.settings_frame, text = "Success!", font = ("Arial", 40), fg = 'red')
		

		#key binds
		self.master.bind("<Return>", lambda a:self.bind_return())
		
		self.master.bind("<Escape>", lambda a:self.bind_escape())
		self.master.bind("<ButtonRelease>", lambda a:self.bind_mouse_up())

		self.master.bind("<Up>", lambda a:self.bind_uparrow())
		self.master.bind("<Down>", lambda a:self.bind_downarrow())
		self.master.bind("<KeyRelease>", lambda a:self.bind_keyup())







	def enter_scores_frame_playerA_win_command(self):
		if self.enter_scores_frame_playerA_nametype1_value.cget("text") != "" and self.enter_scores_frame_playerB_nametype1_value.cget("text") != "":
			self.enter_scores_frame_outcome_button.config(text=f'{self.enter_scores_frame_playerA_nametype1_value.cget("text")} won')
			self.enter_scores_frame_playerA_newrating_value.config(text = equations.calculate_score(self.enter_scores_frame_playerA_oldrating_value.cget("text"), self.enter_scores_frame_playerB_oldrating_value.cget("text"), 1, self.a, self.e)[0])
			self.enter_scores_frame_playerB_newrating_value.config(text = equations.calculate_score(self.enter_scores_frame_playerA_oldrating_value.cget("text"), self.enter_scores_frame_playerB_oldrating_value.cget("text"), 1, self.a, self.e)[1])
		return True

	def enter_scores_frame_playerB_win_command(self):
		if self.enter_scores_frame_playerA_nametype1_value.cget("text") != "" and self.enter_scores_frame_playerB_nametype1_value.cget("text") != "":
			self.enter_scores_frame_outcome_button.config(text=f'{self.enter_scores_frame_playerB_nametype1_value.cget("text")} won')
			self.enter_scores_frame_playerA_newrating_value.config(text = equations.calculate_score(self.enter_scores_frame_playerA_oldrating_value.cget("text"), self.enter_scores_frame_playerB_oldrating_value.cget("text"), 2, self.a, self.e)[0])
			self.enter_scores_frame_playerB_newrating_value.config(text = equations.calculate_score(self.enter_scores_frame_playerA_oldrating_value.cget("text"), self.enter_scores_frame_playerB_oldrating_value.cget("text"), 2, self.a, self.e)[1])
		return True

	def enter_scores_frame_draw_command(self):
		if self.enter_scores_frame_playerA_nametype1_value.cget("text") != "" and self.enter_scores_frame_playerB_nametype1_value.cget("text") != "":
			self.enter_scores_frame_outcome_button.config(text=f'Draw')
			self.enter_scores_frame_playerA_newrating_value.config(text = equations.calculate_score(self.enter_scores_frame_playerA_oldrating_value.cget("text"), self.enter_scores_frame_playerB_oldrating_value.cget("text"), 0, self.a, self.e)[0])
			self.enter_scores_frame_playerB_newrating_value.config(text = equations.calculate_score(self.enter_scores_frame_playerA_oldrating_value.cget("text"), self.enter_scores_frame_playerB_oldrating_value.cget("text"), 0, self.a, self.e)[1])
		return True

	def enter_scores_frame_submit_command(self):
		if self.enter_scores_frame_playerA_newrating_value.cget("text") != "":
			self.c.execute('UPDATE rating_data SET rating = ? WHERE tableName = ? AND nametype1 = ?', [self.enter_scores_frame_playerA_newrating_value.cget("text"), self.current_table, self.enter_scores_frame_playerA_nametype1_value.cget("text")])
			self.c.execute('UPDATE rating_data SET rating = ? WHERE tableName = ? AND nametype1 = ?', [self.enter_scores_frame_playerB_newrating_value.cget("text"), self.current_table, self.enter_scores_frame_playerB_nametype1_value.cget("text")])
			self.conn.commit()
			self.bind_escape()

			self.enter_scores_frame_playerA_nametype1_value.config(text = "")
			self.enter_scores_frame_playerA_nametype2_value.config(text = "")
			self.enter_scores_frame_playerA_teamtype1_value.config(text = "")
			self.enter_scores_frame_playerA_teamtype2_value.config(text = "")
			self.enter_scores_frame_playerA_oldrating_value.config(text = "")
			self.enter_scores_frame_playerB_nametype1_value.config(text = "")
			self.enter_scores_frame_playerB_nametype2_value.config(text = "")
			self.enter_scores_frame_playerB_teamtype1_value.config(text = "")
			self.enter_scores_frame_playerB_teamtype2_value.config(text = "")
			self.enter_scores_frame_playerB_oldrating_value.config(text = "")

		return True


	

	def settings_frame_submit_command(self):
		self.success_words = ""
		self.randomnum = 0
		if check_float(self.settings_frame_entry_avalue.get()) == True:

			self.c.execute('UPDATE settings SET settingValue = ? WHERE settingName = ?', [self.settings_frame_entry_avalue.get(), "a_value"])
			self.a = float(self.settings_frame_entry_avalue.get())


		else:
			self.settings_frame_entry_avalue.delete(0, END)
			self.settings_frame_entry_avalue.insert(END, self.a)
			self.success_words = "Change a-value unsuccessful\n"
			self.randomnum = 1

		if check_float(self.settings_frame_entry_startingrating.get()) == True:

			self.c.execute('UPDATE settings SET settingValue = ? WHERE settingName = ?', [self.settings_frame_entry_startingrating.get(), "startingrating"])
			self.startingrating = self.settings_frame_entry_startingrating.get()

		else:
			self.settings_frame_entry_startingrating.delete(0, END)
			self.settings_frame_entry_startingrating.insert(END, self.startingrating)
			self.success_words = self.success_words + "Change in start rating unsuccessful\n"
			self.randomnum = self.randomnum + 1

		self.c.execute('UPDATE settings SET settingText = ? WHERE settingName = ?', [self.settings_frame_entry_nametype1.get(), "name_type_1_title"])
		self.c.execute('UPDATE settings SET settingText = ? WHERE settingName = ?', [self.settings_frame_entry_nametype2.get(), "name_type_2_title"])
		self.c.execute('UPDATE settings SET settingText = ? WHERE settingName = ?', [self.settings_frame_entry_teamtype1.get(), "team_type_1_title"])
		self.c.execute('UPDATE settings SET settingText = ? WHERE settingName = ?', [self.settings_frame_entry_teamtype2.get(), "team_type_2_title"])
		if self.randomnum == 0:

			self.success_words = 'All Successfull'

		else:
			self.success_words = self.success_words + "All else Successfull"


		
		self.name_type_1_title = self.settings_frame_entry_nametype1.get()
		self.name_type_2_title = self.settings_frame_entry_nametype2.get()
		self.team_type_1_title = self.settings_frame_entry_teamtype1.get()
		self.team_type_2_title = self.settings_frame_entry_teamtype2.get()
		

		self.conn.commit()
		self.settings_frame_label_success.config(text = self.success_words)
		self.settings_frame_label_success.place(anchor = CENTER, relx = 0.5, rely = 0.75)

		return True


	def database_frame_check_autosave(self):
		
		if self.database_frame_list_box.get(ACTIVE) == "autosave.tb" or self.database_frame_list_box.get(ACTIVE) == self.current_table:
			self.database_frame_delete_selected.config(state = DISABLED)
		else:
			self.database_frame_delete_selected.config(state = NORMAL)

		if self.current_table == self.database_frame_list_box.get(ACTIVE):
			self.database_frame_open_selected.config(state = DISABLED)
		else:
			self.database_frame_open_selected.config(state = NORMAL)
		
		self.master.after(1, self.database_frame_check_autosave)
		self.database_frame_entry_box.focus()

	def bind_mouse_up(self):
		if self.mode_variable.get() == "Competitors":
			self.competitors_frame_highlight_colours(self.current_selection)

	def bind_downarrow(self):
		self.current_selection = self.current_selection + 1
		self.competitors_frame_highlight_colours(self.current_selection)
		if self.current_selection > self.competitors_frame_nametype2_listbox.size():
			self.current_selection = self.competitors_frame_nametype2_listbox.size()

		return True

	def bind_uparrow(self):
		self.current_selection = self.current_selection - 1
		self.competitors_frame_highlight_colours(self.current_selection)
		if self.current_selection < -1:
			self.current_selection = -1
		return True

	def competitors_frame_highlight_colours(self, current_selection):
		
		for i in range(self.competitors_frame_nametype2_listbox.size()):
			if i == current_selection:
				self.competitors_frame_nametype1_listbox.itemconfig(i,{'bg':'light blue'})
				self.competitors_frame_nametype2_listbox.itemconfig(i,{'bg':'light blue'})
				self.competitors_frame_teamtype1_listbox.itemconfig(i,{'bg':'light blue'})
				self.competitors_frame_teamtype2_listbox.itemconfig(i,{'bg':'light blue'})
				self.competitors_frame_rating_listbox.itemconfig(i,{'bg':'light blue'})
			else:
				self.competitors_frame_nametype1_listbox.itemconfig(i,{'bg':'white'})
				self.competitors_frame_nametype2_listbox.itemconfig(i,{'bg':'white'})
				self.competitors_frame_teamtype1_listbox.itemconfig(i,{'bg':'white'})
				self.competitors_frame_teamtype2_listbox.itemconfig(i,{'bg':'white'})
				self.competitors_frame_rating_listbox.itemconfig(i,{'bg':'white'})

	def competitors_frame_check_auto(self):



		self.master.after(1, self.competitors_frame_check_auto)

	def bind_return(self):
			
			if self.mode_variable.get() == "Database" and self.database_frame_entry_box.get()!="" and self.database_frame_entry_box.get()!=" "and self.database_frame_entry_box.get()!="  ":
				self.database_frame_submit_button_command()
				

			elif self.mode_variable.get() == "Competitors":
				

				
				self.c.execute('SELECT * FROM rating_data WHERE tableName = ?', [self.current_table])
				self.competitors_frame_competitors = self.c.fetchall()
				self.competitors_frame_competitors.pop(0)
				for i in range(len(self.competitors_frame_competitors)):
					if self.competitors_frame_competitors[i][2] == self.competitors_frame_nametype1_entrybox1.get():
						
						self.competitors_frame_ignore_nametype1 = True


						

				
				if self.competitors_frame_ignore_nametype1 == True:
					self.competitors_frame_nametype2_entrybox1.config(state = NORMAL)
					self.competitors_frame_teamtype1_entrybox1.config(state = NORMAL)
					self.competitors_frame_teamtype2_entrybox1.config(state = NORMAL)
					self.competitors_frame_nametype1_entrybox1.config(state = DISABLED)
					self.counter = self.counter + 1
					if self.counter == 1:

						self.competitors_frame_nametype2_entrybox1.focus()

					elif self.counter == 2:
						self.competitors_frame_teamtype1_entrybox1.focus()

					elif self.counter == 3:
						self.competitors_frame_teamtype2_entrybox1.focus()
					else:

						self.competitors_frame_save_button_command()
					
					#correct nametype 1

				else:
					#incorrect nametype 1
					if self.current_selection == -1 or self.current_selection == self.competitors_frame_nametype2_listbox.size()-1:
						self.competitors_frame_nametype2_entrybox1.config(state = NORMAL)
						self.competitors_frame_teamtype1_entrybox1.config(state = NORMAL)
						self.competitors_frame_teamtype2_entrybox1.config(state = NORMAL)
						if self.competitors_frame_nametype1_entrybox1.get() == "":
							self.competitors_frame_nametype1_entrybox1.focus()
						
						elif self.competitors_frame_nametype2_entrybox1.get() == "":
							self.competitors_frame_nametype2_entrybox1.focus()
							
						elif self.competitors_frame_teamtype1_entrybox1.get() == "":
							self.competitors_frame_teamtype1_entrybox1.focus()
						elif self.competitors_frame_teamtype2_entrybox1.get() == "":
							self.competitors_frame_teamtype2_entrybox1.focus()
						else:
							
							self.competitors_frame_save_button_command()


					else:

						self.c.execute('SELECT * FROM rating_data WHERE nametype1 = ? AND tableName = ?', [self.competitors_frame_nametype1_listbox.get(self.current_selection), self.current_table])
						self.dbFetch = self.c.fetchall()[0]
						self.competitors_frame_nametype1_entrybox1.config(state = NORMAL)
						self.competitors_frame_nametype2_entrybox1.config(state = NORMAL)
						self.competitors_frame_teamtype1_entrybox1.config(state = NORMAL)
						self.competitors_frame_teamtype2_entrybox1.config(state = NORMAL)
						self.competitors_frame_nametype1_entrybox1.delete(0,END)
						self.competitors_frame_nametype2_entrybox1.delete(0,END)
						self.competitors_frame_teamtype1_entrybox1.delete(0,END)
						self.competitors_frame_teamtype2_entrybox1.delete(0,END)
						self.competitors_frame_nametype1_entrybox1.insert(END,self.dbFetch[2])
						self.competitors_frame_nametype2_entrybox1.insert(END,self.dbFetch[3])
						self.competitors_frame_teamtype1_entrybox1.insert(END,self.dbFetch[4])
						self.competitors_frame_teamtype2_entrybox1.insert(END,self.dbFetch[5])
						self.competitors_frame_nametype1_entrybox1.config(state = DISABLED)
						self.competitors_frame_nametype2_entrybox1.focus()
						self.counter = 1
						self.competitors_frame_ignore_nametype1 = True
			elif self.mode_variable.get() == "Enter Scores":
				if self.enter_scores_frame_playerA_entry.get() != "":
					self.enter_scores_frame_playerB_entry.config(state=NORMAL)
					self.enter_scores_frame_playerB_entry.focus()
				else:
					self.enter_scores_frame_playerA_entry.focus()

	def bind_escape(self):
		if self.mode_variable.get() == "Competitors":
			self.current_selection = -1
			self.competitors_frame_nametype1_entrybox1.config(state = NORMAL)
			self.competitors_frame_nametype2_entrybox1.config(state = NORMAL)
			self.competitors_frame_teamtype1_entrybox1.config(state = NORMAL)
			self.competitors_frame_teamtype2_entrybox1.config(state = NORMAL)

			self.competitors_frame_nametype1_entrybox1.delete(0, END)
			self.competitors_frame_nametype2_entrybox1.delete(0,END)
			self.competitors_frame_teamtype1_entrybox1.delete(0,END)
			self.competitors_frame_teamtype2_entrybox1.delete(0,END)
			self.competitors_frame_ignore_nametype1 = False
			self.competitors_frame_nametype1_entrybox1.focus()
			self.competitors_frame_nametype2_entrybox1.config(state = DISABLED)
			self.competitors_frame_teamtype1_entrybox1.config(state = DISABLED)
			self.competitors_frame_teamtype2_entrybox1.config(state = DISABLED)

		elif self.mode_variable.get() == "Enter Scores":
			self.enter_scores_frame_playerB_entry.delete(0, END)
			self.enter_scores_frame_playerA_entry.delete(0, END)
			self.enter_scores_frame_playerB_entry.config(state=DISABLED)
			self.enter_scores_frame_playerA_entry.focus()
			self.enter_scores_frame_playerA_newrating_value.config(text = "")
			self.enter_scores_frame_playerB_newrating_value.config(text = "")
			self.enter_scores_frame_outcome_button.config(text = "")

	def bind_keyup(self):
		if self.mode_variable.get() == "Competitors":
			
			self.c.execute('SELECT * FROM rating_data WHERE tableName = ?', [self.current_table])
			self.competitors_frame_competitors = self.c.fetchall()
			self.competitors_frame_competitors.pop(0)
			for i in range(len(self.competitors_frame_competitors)):
				
				if self.competitors_frame_competitors[i][2] == self.competitors_frame_nametype1_entrybox1.get(): 
					if self.competitors_frame_ignore_nametype1 == False:

						
						self.c.execute('SELECT * FROM rating_data WHERE nametype1 = ? AND tableName = ?', [self.competitors_frame_competitors[i][2], self.current_table])

						self.dbFetch = self.c.fetchall()[0]
						self.competitors_frame_nametype2_entrybox1.config(state = NORMAL)
						self.competitors_frame_teamtype1_entrybox1.config(state = NORMAL)
						self.competitors_frame_teamtype2_entrybox1.config(state = NORMAL)
						self.competitors_frame_nametype2_entrybox1.delete(0,END)
						self.competitors_frame_teamtype1_entrybox1.delete(0,END)
						self.competitors_frame_teamtype2_entrybox1.delete(0,END)
						self.competitors_frame_nametype2_entrybox1.insert(END,self.dbFetch[3])
						self.competitors_frame_teamtype1_entrybox1.insert(END,self.dbFetch[4])
						self.competitors_frame_teamtype2_entrybox1.insert(END,self.dbFetch[5])

						self.competitors_frame_nametype1_entrybox1.config(state = NORMAL)
						self.competitors_frame_nametype2_entrybox1.config(state = DISABLED)
						self.competitors_frame_teamtype1_entrybox1.config(state = DISABLED)
						self.competitors_frame_teamtype2_entrybox1.config(state = DISABLED)
						self.counter = 0
						self.competitors_frame_ignore_nametype1=True

							

				else:
					pass
		elif self.mode_variable.get() == "Enter Scores":
			self.c.execute('SELECT * FROM rating_data WHERE tableName = ?', [self.current_table])
			self.enter_scores_frame_competitorlist = self.c.fetchall()
			if self.enter_scores_frame_competitorlist == []:
				pass
			else:
				self.enter_scores_frame_playerA_correct = [False, 0]
				self.enter_scores_frame_playerB_correct = [False, 0]
				for i in range(len(self.enter_scores_frame_competitorlist)):
					if self.enter_scores_frame_playerA_entry.get() == self.enter_scores_frame_competitorlist[i][2]:
						self.enter_scores_frame_playerA_correct = [True, i]
					elif self.enter_scores_frame_playerB_entry.get() == self.enter_scores_frame_competitorlist[i][2]:
						self.enter_scores_frame_playerB_correct = [True, i]

				if self.enter_scores_frame_playerA_correct[0] == True:
					i = self.enter_scores_frame_playerA_correct[1]
					#fill out data

					self.enter_scores_frame_playerA_nametype1_value.config(text=self.enter_scores_frame_competitorlist[i][2])
					self.enter_scores_frame_playerA_nametype2_value.config(text=self.enter_scores_frame_competitorlist[i][3])
					self.enter_scores_frame_playerA_teamtype1_value.config(text=self.enter_scores_frame_competitorlist[i][4])
					self.enter_scores_frame_playerA_teamtype2_value.config(text=self.enter_scores_frame_competitorlist[i][5])
					self.enter_scores_frame_playerA_oldrating_value.config(text=self.enter_scores_frame_competitorlist[i][7])


				else:
					i = self.enter_scores_frame_playerA_correct[1]
					self.enter_scores_frame_playerA_nametype1_value.config(text="")
					self.enter_scores_frame_playerA_nametype2_value.config(text="")
					self.enter_scores_frame_playerA_teamtype1_value.config(text="")
					self.enter_scores_frame_playerA_teamtype2_value.config(text="")
					self.enter_scores_frame_playerA_oldrating_value.config(text="")
					#delete data

				if self.enter_scores_frame_playerB_correct[0] == True:
					i = self.enter_scores_frame_playerB_correct[1]
					self.enter_scores_frame_playerB_nametype1_value.config(text=self.enter_scores_frame_competitorlist[i][2])
					self.enter_scores_frame_playerB_nametype2_value.config(text=self.enter_scores_frame_competitorlist[i][3])
					self.enter_scores_frame_playerB_teamtype1_value.config(text=self.enter_scores_frame_competitorlist[i][4])
					self.enter_scores_frame_playerB_teamtype2_value.config(text=self.enter_scores_frame_competitorlist[i][5])
					self.enter_scores_frame_playerB_oldrating_value.config(text=self.enter_scores_frame_competitorlist[i][7])
					#fill data
				else:
					i = self.enter_scores_frame_playerB_correct[1]
					self.enter_scores_frame_playerB_nametype1_value.config(text="")
					self.enter_scores_frame_playerB_nametype2_value.config(text="")
					self.enter_scores_frame_playerB_teamtype1_value.config(text="")
					self.enter_scores_frame_playerB_teamtype2_value.config(text="")
					self.enter_scores_frame_playerB_oldrating_value.config(text="")
					#delete data







		return True
		
	def change_mode(self, *args):
		self.competitors_frame.place_forget()
		self.enter_scores_frame.place_forget()
		self.database_frame.place_forget()
		self.settings_frame.place_forget()



		if self.mode_variable.get() == self.mode_options[0]:
			self.competitors_frame.place(anchor=CENTER, relx = 0.49, rely = 0.525)
			self.populate_competitor_frame_listbox()
			self.competitors_frame_check_auto()
			self.bind_escape()
			self.competitors_frame_nametype1_entrybox1.focus()

			self.competitors_frame_nametype1_label1.config(text=self.name_type_1_title)
			self.competitors_frame_nametype2_label1.config(text=self.name_type_2_title)
			self.competitors_frame_teamtype1_label1.config(text=self.team_type_1_title)
			self.competitors_frame_teamtype2_label1.config(text=self.team_type_2_title)
			self.competitors_frame_nametype1_label2.config(text=self.name_type_1_title)
			self.competitors_frame_nametype2_label2.config(text=self.name_type_2_title)
			self.competitors_frame_teamtype1_label2.config(text=self.team_type_1_title)
			self.competitors_frame_teamtype2_label2.config(text=self.team_type_2_title)
			
						


		elif self.mode_variable.get() == self.mode_options[1]:
			self.enter_scores_frame.place(anchor=CENTER, relx = 0.49, rely = 0.525)
			self.enter_scores_frame_playerA_entry.focus()
			self.enter_scores_frame_playerA_nametype1.config(text = self.name_type_1_title)
			self.enter_scores_frame_playerA_nametype2.config(text = self.name_type_2_title)
			self.enter_scores_frame_playerA_teamtype1.config(text = self.team_type_1_title)
			self.enter_scores_frame_playerA_teamtype2.config(text = self.team_type_2_title)
			self.enter_scores_frame_playerB_nametype1.config(text = self.name_type_1_title)
			self.enter_scores_frame_playerB_nametype2.config(text = self.name_type_2_title)
			self.enter_scores_frame_playerB_teamtype1.config(text = self.team_type_1_title)
			self.enter_scores_frame_playerB_teamtype2.config(text = self.team_type_2_title)

		elif self.mode_variable.get() == self.mode_options[2]:
			self.database_frame.place(anchor=CENTER, relx = 0.49, rely = 0.525)
			self.populate_database_frame_listbox()
			self.database_frame_entry_box.focus()
			self.scrollbar.pack(side=RIGHT, fill = BOTH)



		elif self.mode_variable.get() == self.mode_options[3]:
			self.settings_frame.place(anchor=CENTER, relx = 0.49, rely = 0.525)
			self.settings_frame_entry_avalue.delete(0, END)
			self.settings_frame_entry_avalue.insert(END, self.a)

			self.settings_frame_entry_nametype1.delete(0, END)
			self.settings_frame_entry_nametype1.insert(END, self.name_type_1_title)

			self.settings_frame_entry_nametype2.delete(0, END)
			self.settings_frame_entry_nametype2.insert(END, self.name_type_2_title)

			self.settings_frame_entry_teamtype1.delete(0, END)
			self.settings_frame_entry_teamtype1.insert(END, self.team_type_1_title)

			self.settings_frame_entry_teamtype2.delete(0, END)
			self.settings_frame_entry_teamtype2.insert(END, self.team_type_2_title)

			self.settings_frame_entry_startingrating.delete(0, END)
			self.settings_frame_entry_startingrating.insert(END, self.startingrating)

			self.settings_frame_label_success.place_forget()








		else:
			pass

	def populate_competitor_frame_listbox(self):
		#delete list box old entries
		self.competitors_frame_nametype1_listbox.delete(0, END)
		self.competitors_frame_nametype2_listbox.delete(0, END)
		self.competitors_frame_teamtype1_listbox.delete(0, END)
		self.competitors_frame_teamtype2_listbox.delete(0, END)
		self.competitors_frame_rating_listbox.delete(0, END)

		self.c.execute('SELECT * FROM rating_data WHERE tableName = ?', [self.current_table])
		self.competitors_frame_competitors = self.c.fetchall()
		if len(self.competitors_frame_competitors) == 1:
			pass
		else:
			self.competitors_frame_competitors.pop(0)
			for i in range(len(self.competitors_frame_competitors)):
				
			
				self.competitors_frame_nametype1_listbox.insert(END, self.competitors_frame_competitors[i][2])
				self.competitors_frame_nametype2_listbox.insert(END, self.competitors_frame_competitors[i][3])
				self.competitors_frame_teamtype1_listbox.insert(END, self.competitors_frame_competitors[i][4])
				self.competitors_frame_teamtype2_listbox.insert(END, self.competitors_frame_competitors[i][5])
				self.competitors_frame_rating_listbox.insert(END, self.competitors_frame_competitors[i][7])

		self.competitors_frame_nametype1_listbox.insert(END, "New")
		self.competitors_frame_nametype2_listbox.insert(END, "New")
		self.competitors_frame_teamtype1_listbox.insert(END, "New")
		self.competitors_frame_teamtype2_listbox.insert(END, "New")
		self.competitors_frame_rating_listbox.insert(END, "New")
		return True

	def populate_database_frame_listbox(self):

		self.database_frame_list_box.delete(0, END)
		self.c.execute('SELECT tableName FROM rating_data WHERE nametype1 = "Table"')


		self.database_frame_list_box_list = self.c.fetchall()
		for i in range(len(self.database_frame_list_box_list)):
			self.database_frame_list_box.insert(END, self.database_frame_list_box_list[i][0])

		self.c.execute('SELECT settingValue FROM settings WHERE settingName = "selected_table"')
		
		self.database_frame_list_box.select_set(0)

	def competitors_frame_delete(self):

		self.c.execute('SELECT * FROM rating_data WHERE tableName = ?', [self.current_table])
		self.competitors_frame_competitors = self.c.fetchall()
		self.competitors_frame_competitors.pop(0)
		self.competitors_frame_competitors_temp_pass = [0,0]
		for i in range(len(self.competitors_frame_competitors)):
			
			if self.competitors_frame_competitors[i][2] == self.competitors_frame_nametype1_entrybox1.get():
				self.competitors_frame_competitors_temp_pass = [True, i]
				

		if self.competitors_frame_competitors_temp_pass[0] == True:
			i = self.competitors_frame_competitors_temp_pass[1]
			if(messagebox.askyesno("Delete?", f'Do you want to delete this competitor?\n{self.name_type_1_title}:{self.competitors_frame_competitors[i][2]}\n{self.name_type_2_title}:{self.competitors_frame_competitors[i][3]}\n{self.team_type_1_title}:{self.competitors_frame_competitors[i][4]}\n{self.team_type_2_title}:{self.competitors_frame_competitors[i][5]}\nRating:{self.competitors_frame_competitors[i][7]}')) == True:
				self.c.execute('DELETE FROM rating_data WHERE nametype1 =? AND tableName = ?', [self.competitors_frame_competitors[i][2], self.current_table])
				self.bind_escape()
				self.populate_competitor_frame_listbox()
				self.conn.commit()
			else:
				pass
	
	def competitors_frame_save_button_command(self):
		self.c.execute('SELECT * FROM rating_data WHERE tableName = ? AND nametype1 = ?', [self.current_table, self.competitors_frame_nametype1_entrybox1.get()])
		self.dbFetch = self.c.fetchall()

		if self.dbFetch == []:
			self.c.execute('SELECT settingValue FROM settings WHERE settingName = "selected_table"')
			#self.c.execute('INSERT INTO rating_data(tableName, tableNum, nametype1, nametype2, teamtype1, teamtype2, description, rating) VALUES(?,?,?,?,?,?,?,?)', ["autosave.tb", 1, "nbond34", "Nicholas", "Arrow","12","","1380"])
			self.c.execute('INSERT INTO rating_data(tableName, tableNum, nametype1, nametype2, teamtype1, teamtype2, description, rating) VALUES(?,?,?,?,?,?,?,?)', [self.current_table, self.c.fetchall()[0][0], self.competitors_frame_nametype1_entrybox1.get(), self.competitors_frame_nametype2_entrybox1.get(), self.competitors_frame_teamtype1_entrybox1.get(),self.competitors_frame_teamtype2_entrybox1.get(), "", self.startingrating])
		else:

			self.c.execute('UPDATE rating_data SET nametype2 = ?, teamtype1 = ?, teamtype2 =? WHERE nametype1 = ? AND tableName = ?',[self.competitors_frame_nametype2_entrybox1.get(), self.competitors_frame_teamtype1_entrybox1.get(), self.competitors_frame_teamtype2_entrybox1.get(), self.competitors_frame_nametype1_entrybox1.get(), self.current_table])
		
		self.bind_escape()
		self.populate_competitor_frame_listbox()
		self.conn.commit()




		self.conn.commit()
		return True

	def database_frame_submit_button_command(self):
		self.c.execute('SELECT tableName FROM rating_data WHERE tableName = ?', [f'{self.database_frame_entry_box.get()}.tb'])
			
		if self.c.fetchall() == []:
			self.database_frame_entry_input = self.database_frame_entry_box.get()
			self.database_frame_entry_box.delete(0, END)
			self.c.execute('SELECT tableNum FROM rating_data WHERE nametype1 = "Table"')
			self.dbFetch = self.c.fetchall()
			self.next_number = self.dbFetch[len(self.dbFetch)-1][0]+1
			self.c.execute('INSERT INTO rating_data(tableName, tableNum, nametype1, nametype2, teamtype1, teamtype2,description, rating) VALUES (?,?,?,?,?,?,?,?)', [f'{self.database_frame_entry_input}.tb', self.next_number, "Table", "Table", "Table","Table","Table","Table"])
			self.conn.commit()
			self.populate_database_frame_listbox()

	def database_frame_delete(self):
		if self.mode_variable.get() == "Database":
			
			self.c.execute('DELETE FROM rating_data WHERE tableName = ?', [self.database_frame_list_box.get(ACTIVE)])

			self.i = 0
			while (self.database_frame_list_box.get(ACTIVE) != self.database_frame_list_box.get(self.i)) and (self.i< self.database_frame_list_box.size()):
			
				self.i = self.i + 1

			self.database_frame_list_box.delete(self.i)
			self.conn.commit()

	def database_frame_open(self):
		if self.mode_variable.get() == "Database":
			self.current_table = self.database_frame_list_box.get(ACTIVE)
			self.i = 0
			while (self.database_frame_list_box.get(ACTIVE) != self.database_frame_list_box.get(self.i)) and (self.i< self.database_frame_list_box.size()):
			
				self.i = self.i + 1

			self.c.execute('UPDATE settings SET settingValue = ? WHERE settingName = ?', [self.i+1, "selected_table"])
			self.table_button.config(text = f'~{self.current_table}')

			self.conn.commit()
			self.database_frame_current_save.config(text = f"Current Save: {self.current_table}")
			

def main():
	root = Tk()
	conn = sqlite3.connect('Hudsen System')

	window = main_window_class(root, conn)
	root.mainloop()


if __name__ == "__main__":
	main()

		
