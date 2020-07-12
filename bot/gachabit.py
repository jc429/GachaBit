##########################
# Main Bot Functionality #
##########################


from time import sleep
# timestamp checking 
from datetime import datetime, timezone


import sys

import logging

import requests

import tweepy

# bot config 
import config
# user database
import users
# image picker 
import imgpicker


####################
# Global Variables #
####################
sleep_timer = 15
check_keywords = False
keywords =  ["test"]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
last_check = datetime.utcnow()

###
# Scan for all new mentions 
###
def check_mentions(api, DEBUG_MODE = False):
	DEBUG_SKIP_REPLY = False
		
	check_time = datetime.utcnow()
	logger.info("Retrieving mentions since %s" % last_check)
	mentions = tweepy.Cursor(api.mentions_timeline, since=last_check).items(20)
	for t, tweet in enumerate(mentions):
		logger.info("Mention #%d -- tweeted at %s" % (t, tweet.created_at))
		try:
			# Only check tweets that haven't previously been checked
			tweet_timestamp = tweet.created_at
			if tweet_timestamp < last_check:
				#print("tweet time: %s" % tweet_timestamp)
				#print("last check: %s" % last_check)
				logger.info("Reached a tweet that is too old. Breaking loop.")
				break
			else:
				if validate_mention(tweet):
					try:
						username = tweet.user.screen_name
						userid = tweet.user.id
						users.log_user(userid, username, tweet_timestamp)
						if not (DEBUG_MODE and DEBUG_SKIP_REPLY):
							compose_reply(api, tweet, userid, username)
							pass
					except AttributeError as e2:
						username = None
						userid = None
						logger.error("Failed to obtain user - {}".format(e2))

		except Exception as e:
			logger.error("Failed while fetching mentions - {}".format(e))
			break
			
	return check_time


###
# Check that the given tweet is valid to reply to 
###
def validate_mention(tweet):
	valid = True
	# TODO - Make sure tweet has not already been replied to ? 

	# Make sure tweet is not a reply to someone else
	if tweet.in_reply_to_status_id is not None:
		valid = False

	# TODO - Make sure user has not already received a reply in the recent past

	# Check for matching keyword (disable to reply to all mentions)
	if check_keywords:
		has_keywords = False
		if any(keyword in tweet.text.lower() for keyword in keywords):
			has_keywords = True
		if has_keywords is False:
			valid = False

	return valid


###
# Compose a reply tweet
###
def compose_reply(api, src_tweet, userid, username):
	DEBUG_REPLY_TO_CONSOLE = False
	if not username:
		logger.info('invalid username, tweet abandoned')
		return
	logger.info(userid)
	logger.info(f'Replying to {username}')
	
	#generate image 

	img_path = imgpicker.random_image()
	quote = imgpicker.random_quote()
	msg = '@%s ' % username
	msg += quote

	if DEBUG_REPLY_TO_CONSOLE:
		logstr = '\n'
		logstr += 'Reply To Tweet ID: %s \n' % src_tweet.id
		logstr += 'Message: %s \n' % quote
		logstr += 'Image Path: %s \n' % img_path
		logger.info(logstr)
	else:
		try:
			api.update_with_media(
				img_path,
				status = msg,
				in_reply_to_status_id = src_tweet.id,
			)
		except Exception as e:
			logger.error('Failed to post reply - {}'.format(e))

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
	api = config.create_twitter_api()
	logger.info('Bot Started: %s' %  datetime.utcnow())
	config.load_cfg()
	imgpicker.init_img_list()
	users.init_user_list()


###
# Primary bot loop, periodically checks for new mentions and replies to them.
###
def gachabit_loop(DEBUG_MODE = False):
	global last_check
	last_check = datetime.utcnow()
	while True:
		logger.info("Checking mentions")
		last_check = check_mentions(api, DEBUG_MODE)
		logger.info("Replied to tweets up to %s" % last_check)
		config.save_cfg()
		logger.info("Napping...zzz...")
		sleep(sleep_timer)


###
# Main Function
###
def gachabit_main():
	DEBUG_MODE = True
	init()
	if DEBUG_MODE:
		logger.info("Main loop bypassed - GachaBit will not Tweet in this state")
		gachabit_loop(True)
	else:
		gachabit_loop()


###
# Start Program
###
if __name__ == "__main__":
	gachabit_main()

