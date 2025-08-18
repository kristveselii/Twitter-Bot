import tweepy
from config import *

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACESS_TOKEN
access_token_secret = ACESS_TOKEN_SECRET

def authenticate_twitter_app():
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication successful")
        return api
    except Exception as e:
        print("Authentication failed:", e)
        return None


def follow_followers(api):
    if api is None:
        print("API not authenticated. Cannot follow followers.")
        return
    
    try:
        for follower in tweepy.Cursor(api.get_followers).items():
            follower.follow()
            print(f"Followed {follower.screen_name}")
    except Exception as e:
        print("An error occurred while following followers:", e)
    
    print("Finished following all followers.")


def reply_to_keyword(api, keyword, reply_message):
    if api is None:
        print("API not authenticated. Cannot reply to tweets.")
        return
    
    try:
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(5):
            try:
                api.update_status(
                    status=f"@{tweet.user.screen_name} {reply_message}",
                    in_reply_to_status_id=tweet.id
                )
                print(f"Replied to {tweet.user.screen_name}")
            except Exception as e:
                print(f"Failed to reply to {tweet.user.screen_name}: {e}")
    except Exception as e:
        print("An error occurred while searching for tweets:", e)
    
    print("Finished replying to tweets.")

def reply_to_detroit_lions(api):
    if api is None:
        print("API not authenticated. Cannot reply to tweets.")
        return
    
    keyword = "Detroit Lions"
    reply_message = "Go Lions!"
    
    try:
        for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(5):
            if "Detroit Lions" in tweet.text:
                try:
                    api.update_status(
                        status=f"@{tweet.user.screen_name} {reply_message}",
                        in_reply_to_status_id=tweet.id
                    )
                    print(f"Replied to {tweet.user.screen_name} about Detroit Lions")
                except Exception as e:
                    print(f"Failed to reply to {tweet.user.screen_name}: {e}")
    except Exception as e:
        print("An error occurred while searching for tweets:", e)
    
    print("Finished replying to Detroit Lions tweets.")

# Feel free to change the keyword and reply message
def main():
    api = authenticate_twitter_app()
    
    if api:
        follow_followers(api)
        reply_to_keyword(api, "Python", "Hello from the Twitter Bot!")
        reply_to_detroit_lions(api)

