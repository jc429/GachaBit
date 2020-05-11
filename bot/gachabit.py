#
# main bot functionality
#

# timestamp checking 
from datetime import datetime
from datetime import timezone

import os
from time import sleep

import logging
import requests

# handles twitter stuff 
import tweepy 
from config import create_twitter_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#
# Scan for all new mentions 
#
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
				username = tweet.user.screen_name
				userid = tweet.userid
				compose_tweet(api, tweet, userid, username)


		except Exception as e:
			logger.error("Failed while fetching mentions - {}".format(e))
			break
			
	return check_time

#
# Compose the reply
#
def compose_tweet(api, src_tweet, userid, username):
	logger.info(f"replying to {username}")
	msg = "@%s hi :)" % username
	#generate image 

	img_path = generate_img()

	api.update_with_media(
		img_path,
		status = msg,
		in_reply_to_status_id = src_tweet.id,
	)

#
# Randomly selects an image from the pool and returns its filepath
#
def generate_img():
	img_folder = os.getcwd() + "\\img\\"
	file_path = img_folder + "test.png"
	#logger.info(file_path)

	return file_path

#
# Gracefully shut down the bot
#
def shutdown():

	return


def reply_cycle():
	sleep_timer = 15
	api = create_twitter_api()
	global last_check
	last_check = None
	while True:
		last_check = check_mentions(api, ["test"])
		logger.info("replied to tweets up to %s" % last_check)

		logger.info("napping...zzz")
		sleep(sleep_timer)

def main():
	for var in os.environ:
		print(var)

if __name__ == "__main__":
	main()

