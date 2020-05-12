##########################
# Main Bot Functionality #
##########################

# timestamp checking 
from datetime import datetime
from datetime import timezone

import os
import sys
from time import sleep

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import requests

# handles twitter stuff 
import tweepy 
#from config import create_twitter_api
import config


import json


sleep_timer = 15

###
# Scan for all new mentions 
###
def check_mentions(api, keywords):
	logger.info("retrieving mentions")
	check_time = datetime.now()
	mentions = tweepy.Cursor(api.mentions_timeline).items()
	for tweet in mentions:
		try:
			tweet_timestamp = tweet.created_at
			if last_check is not None:
				if tweet_timestamp < last_check:
					continue
			if tweet.in_reply_to_status_id is not None:
				continue
			# check for matching keyword (disable to reply to all mentions)
			if any(keyword in tweet.text.lower() for keyword in keywords):
				try:
					username = tweet.user.screen_name
					userid = tweet.user.id
					compose_tweet(api, tweet, userid, username)
				except AttributeError as e:
					username = None
					userid = None
					logger.error("Failed to obtain user - {}".format(e))


		except Exception as e:
			logger.error("Failed while fetching mentions - {}".format(e))
			break
			
	return check_time

###
# Compose the reply
###
def compose_tweet(api, src_tweet, userid, username):
	if not username:
		logger.info("invalid username, tweet abandoned")
		return
	
	logger.info(f"Replying to {username}")
	#msg = "@%s hi :)" % username
	msg = "hey!"
	#generate image 

	img_path = generate_img()

	api.update_with_media(
		img_path,
		status = msg,
		in_reply_to_status_id = src_tweet.id,
	)

###
# Randomly selects an image from the pool and returns its filepath
###
def generate_img():
	img_folder = os.getcwd() + "\\img\\"
	file_path = img_folder + "test.png"
	#logger.info(file_path)

	return file_path

###
# Gracefully shut down the bot
###
def shutdown():
	sys.exit(0)
	return

###
# Main bot loop, periodically checks for new mentions and replies to them
###
def reply_cycle():
	last_check = check_mentions(api, ["test"])
	logger.info("replied to tweets up to %s" % last_check)
	config.save_cfg()
	logger.info("napping...zzz")
	sleep(sleep_timer)

###
# initialize global variables
###
def init():
	global api 
	global last_check
	config.load_cfg()
	api = config.create_twitter_api()
	last_check = None

###
# main 
###
def main():
	init()
	while True:
		reply_cycle()

if __name__ == "__main__":
	main()

