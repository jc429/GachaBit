#############################################################
# Handles user-specific data (punchcards, rate limits, etc) #
#############################################################

import json

user_list = {}


class User:
	user_id = 0
	user_name = ""
	pulls = []
	last_roll = 0


	def __init__(self, id, name = ""):
		self.user_id = id
		self.user_name = name
		self.pulls = []
		self.last_roll = 0

	def get_id(self):
		return self.user_id

	def get_name(self):
		return self.user_name
	
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
	for i in range(indentation):
		ind_str += " "
	return ind_str


def load_user_cfg():
	pass


def save_user_cfg():
	indentation_level = 0
	print(create_json_line("{", indentation_level))

	indentation_level = 1
	print(create_json_line('"users": [', indentation_level))

	indentation_level = 2
	userno = 0
	userct = len(user_list)
	for user in user_list:
		user_str = user_list.get(user).to_json(indentation_level)

		userno += 1
		if(userno < userct):
			print(user_str + ',')
		else:
			print(user_str)
		pass

	indentation_level = 1
	print(create_json_line(']', indentation_level))
	
	indentation_level = 0
	print(create_json_line('}', indentation_level))

###
# returns a line with appropriate indentation level
###
def create_json_line(text, ind_lvl):
	ind_str = get_indent(ind_lvl)
	return ind_str + text


# temp function
def temp_populate_user_list():
	u1 = User(1, "Bob")
	u2 = User(3, "Michelle")
	register_user(u1)
	register_user(u2)
	pass


###
# User list initialization
###
def init_user_list():
	temp_populate_user_list()
	save_user_cfg()

###
# Adds a user to the database
###
def register_user(user):
	if user.get_id() in user_list:
		return
	user_list[user.get_id()] = user

###
# Checks if a user already exists in the user database
###
def user_in_list(user_id):
	for user in user_list:
		if user.get_id() == user_id:
			return True
	return False

###
# Returns the user from the database, or creates a new entry if one doesnt exist
###
def get_user_info(user_id):
	if user_id in user_list:
		return user_list[user_id]
	new_user = User(user_id)
	user_list[user_id] = new_user
	return new_user



if __name__ == "__main__":
	init_user_list()