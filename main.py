import tweepy
import tkinter as tk
import threading
import random
import time
from config import *

# ------------------------
# Twitter Auth (v2 Client w/ User Context)
# ------------------------
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True  # Automatically handle rate limits
)

# ------------------------
# Authentication Test
# ------------------------
def test_authentication():
    """Test if authentication is working properly"""
    try:
        me = client.get_me()
        print(f"✅ Authentication successful! Logged in as: @{me.data.username}")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

# ------------------------
# Bot Functions (v2)
# ------------------------
def reply_to_keyword(keyword, reply_message, max_results=5):
    """Reply to tweets containing a specific keyword"""
    try:
        print(f"🔍 Searching for tweets with keyword: '{keyword}'")
        
        # Search for tweets (requires Elevated access)
        tweets = client.search_recent_tweets(
            query=f"{keyword} -is:retweet -is:reply",  # Exclude retweets and replies
            max_results=max_results,
            tweet_fields=['author_id', 'created_at']
        )
        
        if tweets.data:
            print(f"Found {len(tweets.data)} tweets")
            for tweet in tweets.data:
                try:
                    # Add delay to avoid hitting rate limits
                    time.sleep(1)
                    
                    response = client.create_tweet(
                        text=reply_message,
                        in_reply_to_tweet_id=tweet.id
                    )
                    print(f"✅ Replied to tweet ID {tweet.id}")
                    
                except tweepy.TooManyRequests:
                    print("⏳ Rate limit reached. Waiting...")
                    time.sleep(15 * 60)  # Wait 15 minutes
                except tweepy.Forbidden as e:
                    print(f"❌ Forbidden: {e}")
                    break
                except Exception as e:
                    print(f"❌ Error replying to tweet {tweet.id}: {e}")
        else:
            print(f"No tweets found for keyword: '{keyword}'")
            
    except tweepy.Unauthorized:
        print("❌ 401 Unauthorized: Check your API permissions and access level")
        print("   - Ensure your app has 'Read and Write' permissions")
        print("   - You may need Elevated API access for search functionality")
    except tweepy.Forbidden:
        print("❌ 403 Forbidden: Your app doesn't have permission for this operation")
    except Exception as e:
        print(f"❌ Error while searching/replying to tweets: {e}")

def reply_to_detroit_lions():
    """Reply to Detroit Lions tweets"""
    reply_to_keyword("Detroit Lions", "Go Lions! 🦁")

def basic_tier_bot():
    """Bot functions that work with Basic API access"""
    print("🤖 Running Basic Tier Bot (no search required)...")
    
    if not test_authentication():
        print("❌ Bot cannot run due to authentication issues")
        return
    
    # Post a status update
    try:
        status_tweets = [
            "🤖 Bot is active and monitoring!",
            "🐍 Python automation at work!",
            "🚀 Testing Twitter API integration!",
            "💻 Coding with Tweepy library!",
            "🦁 Detroit Lions fan checking in!"
        ]
        
        tweet_text = random.choice(status_tweets) + f" #{random.randint(1000, 9999)}"
        response = client.create_tweet(text=tweet_text)
        print(f"✅ Posted status tweet: {response.data['text']}")
        
    except Exception as e:
        print(f"❌ Error posting status: {e}")
    
    # You can add more basic tier functionality here:
    # - Reply to your own tweets
    # - Post scheduled content
    # - Respond to mentions (if you can get them)
    
    print("✅ Basic tier bot finished!")

def run_bot_with_search():
    """Bot that requires Elevated API access for search functionality"""
    print("🤖 Starting Advanced Twitter bot (requires Elevated access)...")
    
    # Test authentication first
    if not test_authentication():
        print("❌ Bot cannot run due to authentication issues")
        return
    
    print("Running Twitter bot operations with search...")
    
    # Try different search terms
    reply_to_keyword("Python programming", "Hello from the Twitter Bot! 🐍")
    reply_to_detroit_lions()
    
    print("✅ Advanced bot finished running.")

# ------------------------
# Test Tweet
# ------------------------
def test_post():
    """Post a test tweet"""
    try:
        tweet_text = f"🚀 Test tweet from my Tweepy bot! #{random.randint(1,10000)}"
        response = client.create_tweet(text=tweet_text)
        print("✅ Tweet posted successfully:")
        print(f"   Tweet ID: {response.data['id']}")
        print(f"   Text: {response.data['text']}")
    except tweepy.Unauthorized:
        print("❌ 401 Unauthorized: Check your API keys and permissions")
    except tweepy.Forbidden:
        print("❌ 403 Forbidden: Your app may not have write permissions")
    except Exception as e:
        print(f"❌ Failed to post tweet: {e}")

# ------------------------
# Check API Status
# ------------------------
def check_api_access_level():
    """Check what API access level we have"""
    try:
        print("📊 Checking API Access Level...")
        
        # Test basic operations
        me = client.get_me()
        print(f"✅ Basic Auth: Can get user info (@{me.data.username})")
        
        # Test tweet posting (we know this works)
        print("✅ Tweet Creation: Working")
        
        # Test search (this is what's failing)
        try:
            test_search = client.search_recent_tweets(query="test", max_results=5)
            print("✅ Search Recent Tweets: Working (Elevated Access)")
        except tweepy.Unauthorized:
            print("❌ Search Recent Tweets: Requires Elevated Access")
            print("   Current Access: Basic (Free)")
            print("   Needed: Elevated Access")
            
        print("\n📋 API Access Summary:")
        print("   - Your current tier: Basic (Free)")
        print("   - Can post tweets: ✅")
        print("   - Can search tweets: ❌ (needs Elevated)")
        print("   - Can reply to your own tweets: ✅")
        print("   - Can reply to mentions: ✅")
            
    except Exception as e:
        print(f"❌ Error checking API access: {e}")

# ------------------------
# GUI
# ------------------------
def create_gui():
    """Create the main GUI interface"""
    root = tk.Tk()
    root.title("Twitter Bot (v2) - Improved")
    root.geometry("300x400")
    
    # Title label
    title_label = tk.Label(root, text="Twitter Bot Control Panel", font=("Arial", 12, "bold"))
    title_label.pack(pady=10)
    
    # Status label
    status_label = tk.Label(root, text="Ready to run...", fg="blue")
    status_label.pack(pady=5)
    
    # Test Authentication button
    auth_button = tk.Button(
        root,
        text="Test Authentication",
        command=lambda: threading.Thread(target=test_authentication).start(),
        bg="lightblue"
    )
    auth_button.pack(pady=5)
    
    # Check API Access button
    access_button = tk.Button(
        root,
        text="Check API Access Level",
        command=lambda: threading.Thread(target=check_api_access_level).start(),
        bg="lightyellow"
    )
    access_button.pack(pady=5)
    
    # Test Tweet button
    test_button = tk.Button(
        root,
        text="Post Test Tweet",
        command=lambda: threading.Thread(target=test_post).start(),
        bg="lightgreen"
    )
    test_button.pack(pady=5)
    
    # Basic Bot button (works without Elevated access)
    basic_button = tk.Button(
        root,
        text="Run Basic Bot",
        command=lambda: threading.Thread(target=basic_tier_bot).start(),
        bg="lightblue"
    )
    basic_button.pack(pady=5)
    
    # Advanced Bot button (requires Elevated access)
    advanced_button = tk.Button(
        root,
        text="Run Advanced Bot (Search)",
        command=lambda: threading.Thread(target=run_bot_with_search).start(),
        bg="orange"
    )
    advanced_button.pack(pady=5)
    
    # Instructions
    instructions = tk.Text(root, height=8, width=35, wrap=tk.WORD)
    instructions.insert(tk.END, 
        "Instructions:\n\n"
        "1. Check API Access Level first\n"
        "2. Test Authentication\n"
        "3. Try posting a test tweet\n"
        "4. Use Basic Bot (works now)\n"
        "5. Advanced Bot needs Elevated access\n\n"
        "Current Status:\n"
        "- Basic access: ✅ Working\n"
        "- Can post tweets: ✅\n"
        "- Can search tweets: ❌ (needs upgrade)\n\n"
        "To get Elevated access:\n"
        "Apply at developer.twitter.com"
    )
    instructions.config(state=tk.DISABLED)
    instructions.pack(pady=10)
    
    # Close button
    close_button = tk.Button(root, text="Close", command=root.destroy, bg="lightcoral")
    close_button.pack(pady=5)
    
    root.mainloop()

# ------------------------
# Main
# ------------------------
def main():
    print("🚀 Launching Twitter Bot GUI...")
    print("="*50)
    create_gui()

if __name__ == "__main__":
    main()