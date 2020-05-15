#############################################################
# Handles user-specific data (punchcards, rate limits, etc) #
#############################################################

user_list = {}


class User:
	user_id = 0
	user_name = ""
	pulls = []
	last_roll = 0


	def __init__(self, id, name = ""):
		self.user_id = id
		self.user_name = name

	def get_id(self):
		return self.user_id

	def get_name(self):
		return self.user_name
	


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
