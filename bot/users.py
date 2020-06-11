#############################################################
# Handles user-specific data (punchcards, rate limits, etc) #
#############################################################

import os
import sys
import json
from dateutil import parser
from datetime import datetime

user_list = {}
data_folder = os.getcwd() + '\\data\\'
user_path = data_folder + 'users.json'
print_to_file = True
print_to_console = True


class User:
	user_id = 0
	user_name = ""
	pulls = []


	def __init__(self, id, name = ""):
		self.user_id = id
		self.user_name = name
		self.pulls = []

	def get_id(self):
		return self.user_id

	def get_name(self):
		return self.user_name

	def set_data(self, username):
		self.user_name = username

	def copy_data(self, other):
		self.user_name = other.user_name
	
	def to_json(self, ind):
		json_src = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=ind)
		json_arr = json_src.splitlines()
		ind_str = get_indent(ind)
		json_str = ""

		for line in json_arr[:-1]:
			json_str += ind_str
			json_str += line
			json_str += "\n"
		line = json_arr[-1]
		json_str += ind_str
		json_str += line

		return json_str




###
# Returns a string of (indent) spaces
###
def get_indent(indentation_level):
	indentation = indentation_level * 4
	ind_str = ""
	for _ in range(indentation):
		ind_str += " "
	return ind_str


def load_user_cfg(filepath):
	with open(filepath, 'r') as cfg_file:
		json_data = json.load(cfg_file)
		users_json = json_data['users']
		for u_json in users_json:
			u_id = u_json['user_id']
			u_name = u_json['user_name']
			u_pulls = u_json['pulls']
			user = User(u_id, u_name)
			user.pulls = u_pulls
			register_user(user)
			#print(u_json)
		print("User file successfully loaded")


def save_user_cfg(filepath, DEBUG_PRINT_TO_CONSOLE = False):
	
	def write_cfg():
		# write out the json 
		indentation_level = 0
		print(create_json_line("{", indentation_level), file=cfg_file)

		indentation_level = 1
		print(create_json_line('"users": [', indentation_level), file=cfg_file)

		indentation_level = 2
		userno = 0
		userct = len(user_list)
		for user in user_list:
			user_str = user_list.get(user).to_json(indentation_level)

			userno += 1
			if(userno < userct):
				print(user_str + ',', file=cfg_file)
			else:
				print(user_str, file=cfg_file)
			pass

		indentation_level = 1
		print(create_json_line(']', indentation_level), file=cfg_file)
		
		indentation_level = 0
		print(create_json_line('}', indentation_level), file=cfg_file)

		# end write_cfg

	#write to console
	if DEBUG_PRINT_TO_CONSOLE:
		cfg_file = sys.stdout
		write_cfg()

	# open file 
	if print_to_file:
		with open(filepath, 'w') as cfg_file:
			write_cfg()
			print('user file succesfully written')

###
# Save the list of interacted users
###
def save():
	save_user_cfg(user_path, print_to_console)


###
# returns a line with appropriate indentation level
###
def create_json_line(text, ind_lvl):
	ind_str = get_indent(ind_lvl)
	return ind_str + text




###
# User list initialization
###
def init_user_list():
	print('Initializing User List...')
	data_folder = os.getcwd() + '\\data\\'
	user_path = data_folder + 'users.json'
	load_user_cfg(user_path)
	#temp_populate_user_list()
	#save_user_cfg(user_path, True)
	print('User List successfully initialized!')
	print('')


###
# Adds a user to the database
###
def register_user(user):
	if user.get_id() in user_list:
		#user_list[user.get_id()]
		return
	user_list[user.get_id()] = user


###
# Checks if a user already exists in the user database
###
def user_in_list(user_id):
	return (user_id in user_list)


###
# Returns the user from the database, or creates a new entry if one doesnt exist
###
def get_user_info(user_id):
	if user_id in user_list:
		return user_list[user_id]
	new_user = User(user_id)
	user_list[user_id] = new_user
	return new_user


###
# updates the user entry in the database with current info, or adds a new entry
###
def update_user_info(user):
	if user.user_id in user_list:
		user_list[user.user_id].copy_data(user)
	else:
		register_user(user)


###
# Logs a user
###
def log_user(id, username, timestamp):
	user = get_user_info(id)
	user.set_data(username)
	update_user_info(user)
	print('User Logged: %s \n' % username)


if __name__ == "__main__":
	init_user_list()