#########################
# Handles Image Picking #
#########################

import os
import json
import random


img_folder = os.getcwd() + '\\img\\'
data_folder = os.getcwd() + '\\data\\'
gallery_path = data_folder + 'gallery.json'

# dict of GachaImages 
image_list = {}
# just a simple list of strings to randomly select
quote_list = []

class GachaImage:
	filename = ''
	img_name = ''
	rarity = 1

	def __init__(self, file_name, img_name = '', rty = 1):
		self.filename = file_name
		self.img_name = img_name
		self.rarity = rty

	def get_filename(self):
		return self.filename

###
# Loads all the necessary image info from a JSON file 
###
def load_image_json(filepath):
	with open(filepath, 'r') as cfg_file:
		json_data = json.load(cfg_file)
		# get current pool name
		cur_pool = json_data['current_pool']
		#get data of that pool
		pool_json = json_data[cur_pool]
		# load images
		img_json = pool_json['images']
		for i_json in img_json:
			i_file = i_json['file']
			i_rty = i_json['rarity']
			i_name = i_json['name']
			img = GachaImage(i_file, i_name, i_rty)
			register_img(img)

		quote_json = pool_json['quotes']
		for quote in quote_json:
			quote_list.append(quote)
		

	return

###
# Image list initialization
###
def init_img_list():
	print('Initializing Image List...')
	load_image_json(gallery_path)


###
# Adds an image to the database
###
def register_img(img):
	if img.get_filename() in image_list:
		return
	image_list[img.get_filename()] = img




###
# Randomly selects an image from the pool and returns its filepath
###
def random_image():
	#TODO: weighted probability image generation
	file_path = img_folder + 'test.png'
	#logger.info(file_path)

	return file_path

###
# Randomly selects and returns a quote
###
def random_quote():
	r = random.randint(0,len(quote_list))
	quote = quote_list[r]
	
	print("Quote Selected: " + quote)

	return quote


if __name__ == "__main__":
	init_img_list()