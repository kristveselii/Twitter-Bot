import tweepy
from config import *
from tkinter import *

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACESS_TOKEN
access_token_secret = ACESS_TOKEN_SECRET

def authenticate_twitter_app():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication successful")
        return api
    except Exception as e:
        print("Authentication failed:", e)
        return None
    
api = authenticate_twitter_app()

# Follow everyone who follows you
def follow_followers(api):
    if api is None:
        print("API not authenticated. Cannot follow followers.")
        return
    
    try:
        for follower in tweepy.Cursor(api.followers).items():
            follower.follow()
            print(f"Followed {follower.screen_name}")
    except Exception as e:
        print("An error occurred while following followers:", e)
    
    print("Finished following all followers.")