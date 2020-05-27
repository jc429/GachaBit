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

#user database
import users


####################
# Global Variables #
####################
sleep_timer = 15
keywords =  ["test"]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
recent_replies = []
last_check = datetime.utcnow()

###
# Scan for all new mentions 
###
def check_mentions(api, DEBUG_SKIP_REPLY = False):
	
		
	check_time = datetime.utcnow()
	logger.info("Retrieving mentions since %s" % last_check)
	mentions = tweepy.Cursor(api.mentions_timeline, since=last_check).items(20)
	for e, tweet in enumerate(mentions):
		logger.info("#%s" % e)
		logger.info("tweeted at %s" % tweet.created_at)
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
						if DEBUG_SKIP_REPLY is False:
							compose_reply(api, tweet, userid, username)
							pass
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
# Compose a reply tweet
###
def compose_reply(api, src_tweet, userid, username):
	if not username:
		logger.info("invalid username, tweet abandoned")
		return
	logger.info(userid)
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
	api = create_twitter_api()
	logger.info("Bot Started: %s" %  datetime.utcnow())
	load_cfg()
	users.init_user_list()


###
# Primary bot loop, periodically checks for new mentions and replies to them.
###
def gachabit_loop():
	last_check = datetime.utcnow()
	while True:
		logger.info("Checking mentions")
		last_check = check_mentions(api)
		logger.info("Replied to tweets up to %s" % last_check)
		save_cfg()
		logger.info("Napping...zzz")
		sleep(sleep_timer)


###
# Debugger Function
###
def gachabit_debug():
	last_check = datetime.utcnow()
	while True:
		logger.info("D: Checking mentions")
		last_check = check_mentions(api, True)
		logger.info("D: Replied to tweets up to %s" % last_check)
		save_cfg()
		users.save()
		logger.info("D: Napping...zzz...")
		sleep(sleep_timer)


###
# Main Function
###
def main():
	DEBUG_MODE = True
	init()
	if DEBUG_MODE:
		logger.info("Main loop bypassed - GachaBit will not Tweet in this state")
		##logger.info("Override Enabled: Will not post replies")
		gachabit_debug()
	else:
		gachabit_loop()


###
# Start Program
###
if __name__ == "__main__":
	main()

