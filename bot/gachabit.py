##########################
# Main Bot Functionality #
##########################

# timestamp checking 
from datetime import datetime, timezone

import sys
from time import sleep

import logging


import requests

import tweepy

from config import load_cfg, save_cfg, create_twitter_api
from imgpicker import generate_img



####################
# Global Variables #
####################
sleep_timer = 15
keywords =  ["test"]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
recent_replies = []

###
# Scan for all new mentions 
###
def check_mentions(api):
	logger.info("retrieving mentions")
	check_time = datetime.now()
	mentions = tweepy.Cursor(api.mentions_timeline).items()
	for tweet in mentions:
		try:
			# Only check tweets that haven't previously been checked
			tweet_timestamp = tweet.created_at
			if last_check is not None:
				if tweet_timestamp < last_check:
					continue
			
			if validate_mention(tweet):
				try:
					username = tweet.user.screen_name
					userid = tweet.user.id
					compose_reply(api, tweet, userid, username)
				except AttributeError as e:
					username = None
					userid = None
					logger.error("Failed to obtain user - {}".format(e))

		except Exception as e:
			logger.error("Failed while fetching mentions - {}".format(e))
			break
			
	return check_time


###
# Check that the given tweet is valid to reply to 
###
def validate_mention(tweet):
	valid = True
	# TODO - Make sure tweet has not already been replied to

	# Make sure tweet is not a reply to someone else
	if tweet.in_reply_to_status_id is not None:
		valid = False

	# TODO - Make sure user has not already received a reply in the recent past

	# Check for matching keyword (disable to reply to all mentions)
	check_keywords = False
	if check_keywords:
		has_keywords = False
		if any(keyword in tweet.text.lower() for keyword in keywords):
			has_keywords = True
		if has_keywords is False:
			valid = False

	return valid


###
# Compose the reply
###
def compose_reply(api, src_tweet, userid, username):
	if not username:
		logger.info("invalid username, tweet abandoned")
		return
	
	logger.info(f"Replying to {username}")
	msg = "@%s hey!" % username
	#generate image 

	img_path = generate_img()

	try:
		api.update_with_media(
			img_path,
			status = msg,
			in_reply_to_status_id = src_tweet.id,
		)
	except Exception as e:
		logger.error("Failed to post reply - {}".format(e))

###
# Gracefully shut down the bot
###
def shutdown():
	sys.exit(0)
	return

###
# Initialize global variables
###
def init():
	global api 
	global last_check
	load_cfg()
	api = create_twitter_api()
	last_check = None

###
# Main bot loop, periodically checks for new mentions and replies to them.
###
def main():
	init()
	while True:
		last_check = check_mentions(api)
		logger.info("Replied to tweets up to %s" % last_check)
		save_cfg()
		logger.info("Napping...zzz")
		sleep(sleep_timer)





if __name__ == "__main__":
	main()

