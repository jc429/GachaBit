#################
# Image Rolling #
#################

import os
import json

###
# Loads all the necessary image info from a JSON file 
###
def load_image_info():
	# TODO - load in json info of all the images
	return

###
# Randomly selects an image from the pool and returns its filepath
###
def generate_img():
	img_folder = os.getcwd() + '\\img\\'
	file_path = img_folder + 'test.png'
	#logger.info(file_path)

	return file_path