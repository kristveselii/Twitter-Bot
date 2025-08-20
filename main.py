import tweepy
import tkinter as tk
import threading
import random
import time
import schedule
import datetime
from config import *

# ------------------------
# Twitter Auth
# ------------------------
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)

# ------------------------
# Lions Schedule Data (2024-2025 Season)
# ------------------------
LIONS_SCHEDULE = {
    # Format: "YYYY-MM-DD": "Opponent Team Name"
    "2025-09-07": "Green Bay Packers",
    "2025-09-14": "Chicago Bears",  # Example game
    "2025-09-22": "Baltimore Ravens",
    "2025-09-28": "Cleveland Browns",
    "2025-10-05": "Cincinnati Bengals",
    "2025-10-12": "Kansas City Chiefs",
    "2025-10-20": "Tampa Bay Buccaneers",
    "2025-11-02": "Minnesota Vikings",
    "2025-11-09": "Washington Commanders",
    "2025-11-16": "Philadelphia Eagles",
    "2025-11-23": "New York Giants",
    "2025-11-27": "Green Bay Packers",
    "2025-12-04": "Dallas Cowboys",
    "2025-12-14": "Los Angeles Rams",
    "2025-12-21": "Pittsburgh Steelers",
    "2025-12-25": "Minnesota Vikings",

}

# Additional opponent variations for more dynamic tweets
TEAM_HASHTAGS = {
    "Washington Commanders": "#OnePride #DetroitVsEverybody",
    "Green Bay Packers": "#OnePride #DivisionRival",
    "Chicago Bears": "#OnePride #DivisionRival", 
    "Minnesota Vikings": "#OnePride #DivisionRival",
    "Tampa Bay Buccaneers": "#OnePride #DetroitVsEverybody",
    "Cleveland Browns": "#OnePride #DetroitVsEverybody",
    "Baltimore Ravens": "#OnePride #DetroitVsEverybody",
    "Cincinnati Bengals": "#OnePride #DetroitVsEverybody",
    "Kansas City Chiefs": "#OnePride #SuperBowlChamps",
    "Dallas Cowboys": "#OnePride #America'sTeam",
    "Los Angeles Rams": "#OnePride #WestCoastBattle",
    "Pittsburgh Steelers": "#OnePride #SteelCityShowdown",
    "Philadelphia Eagles": "#OnePride #NFCShowdown",
    "New York Giants": "#OnePride #BigAppleBattle",
    "Detroit Lions": "#OnePride",  # Self-reference
    "TBD": "#OnePride #PlayoffBound"
}

# ------------------------
# Game Day Functions
# ------------------------
def get_todays_opponent():
    """Check if Lions play today and return opponent"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    return LIONS_SCHEDULE.get(today)

def create_game_day_message(opponent):
    """Create a game day message"""
    messages = [
        f"🦁 TODAY'S THE DAY! Detroit Lions vs {opponent}! Go Lions! #OnePride",
        f"🏈 GAME DAY! Lions take on the {opponent} today! Let's roar! #DetroitVsEverybody",
        f"⚡ IT'S GAME DAY! Detroit Lions vs {opponent}! Time to show them what we're made of! #OnePride",
        f"🔥 Lions vs {opponent} TODAY! Detroit vs Everybody! Let's get this W! #OnePride",
        f"🦁 ROAR! Game day is here! Detroit Lions vs {opponent}! #OnePride #DetroitLions"
    ]
    
    base_message = random.choice(messages)
    hashtags = TEAM_HASHTAGS.get(opponent, "#OnePride #DetroitVsEverybody")
    
    return f"{base_message} {hashtags}"

def post_game_day_tweet():
    """Post the game day tweet if Lions play today"""
    try:
        opponent = get_todays_opponent()
        
        if opponent:
            message = create_game_day_message(opponent)
            response = client.create_tweet(text=message)
            
            print(f"🦁 GAME DAY TWEET POSTED!")
            print(f"   Opponent: {opponent}")
            print(f"   Message: {message}")
            print(f"   Tweet ID: {response.data['id']}")
            
            return True
        else:
            print(f"📅 No Lions game today ({datetime.date.today()})")
            return False
            
    except Exception as e:
        print(f"❌ Error posting game day tweet: {e}")
        return False

def schedule_game_day_posts():
    """Schedule the 10:00 AM game day posts"""
    schedule.every().day.at("10:00").do(post_game_day_tweet)
    print("⏰ Scheduled game day tweets for 10:00 AM daily")

def run_scheduler():
    """Run the scheduler continuously"""
    print("🔄 Starting tweet scheduler...")
    print(f"📅 Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# ------------------------
# Manual Functions
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

def post_test_game_day_tweet():
    """Manually post a test game day tweet"""
    try:
        # Use next scheduled game or create a test message
        opponent = get_todays_opponent()
        
        if not opponent:
            # Find the next scheduled game
            today = datetime.date.today()
            upcoming_games = []
            
            for date_str, team in LIONS_SCHEDULE.items():
                game_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                if game_date >= today:
                    upcoming_games.append((game_date, team))
            
            if upcoming_games:
                upcoming_games.sort()
                next_game_date, next_opponent = upcoming_games[0]
                test_message = f"🧪 TEST TWEET: Next Lions game is {next_game_date.strftime('%B %d')} vs {next_opponent}! #OnePride #TestTweet"
            else:
                test_message = f"🧪 TEST TWEET: Detroit Lions Game Day Bot is ready! #OnePride #TestTweet #{random.randint(1000, 9999)}"
        else:
            test_message = f"🧪 TEST: {create_game_day_message(opponent)} #TestTweet"
        
        response = client.create_tweet(text=test_message)
        print(f"✅ Test tweet posted successfully!")
        print(f"   Message: {test_message}")
        print(f"   Tweet ID: {response.data['id']}")
        
    except Exception as e:
        print(f"❌ Error posting test tweet: {e}")

def check_upcoming_games():
    """Display upcoming Lions games"""
    print("📅 Detroit Lions Upcoming Games:")
    print("="*50)
    
    today = datetime.date.today()
    upcoming_games = []
    
    for date_str, opponent in LIONS_SCHEDULE.items():
        game_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if game_date >= today:
            upcoming_games.append((game_date, opponent))
    
    if upcoming_games:
        upcoming_games.sort()
        for game_date, opponent in upcoming_games[:5]:  # Show next 5 games
            days_until = (game_date - today).days
            if days_until == 0:
                print(f"🦁 TODAY: vs {opponent}")
            elif days_until == 1:
                print(f"📅 TOMORROW: vs {opponent}")
            else:
                print(f"📅 {game_date.strftime('%B %d, %Y')} ({days_until} days): vs {opponent}")
    else:
        print("No upcoming games scheduled in the database")
        print("Update LIONS_SCHEDULE in the code with new games")

def add_game_to_schedule():
    """Function to add games to schedule (for GUI)"""
    print("📝 To add games to the schedule:")
    print("1. Edit the LIONS_SCHEDULE dictionary in the code")
    print("2. Use format: 'YYYY-MM-DD': 'Opponent Name'")
    print("3. Restart the application")

# ------------------------
# GUI
# ------------------------
def create_gui():
    """Create the main GUI interface"""
    root = tk.Tk()
    root.title("Detroit Lions Game Day Bot")
    root.geometry("400x600")
    
    # Title
    title_label = tk.Label(root, text="🦁 Detroit Lions Game Day Bot", 
                          font=("Arial", 14, "bold"), fg="blue")
    title_label.pack(pady=10)
    
    # Current status
    today_opponent = get_todays_opponent()
    if today_opponent:
        status_text = f"🏈 GAME DAY! vs {today_opponent}"
        status_color = "red"
    else:
        status_text = "📅 No game today"
        status_color = "gray"
    
    status_label = tk.Label(root, text=status_text, font=("Arial", 10), fg=status_color)
    status_label.pack(pady=5)
    
    # Test Authentication
    auth_button = tk.Button(
        root, text="🔐 Test Authentication",
        command=lambda: threading.Thread(target=test_authentication).start(),
        bg="lightblue", width=25
    )
    auth_button.pack(pady=5)
    
    # Check Upcoming Games
    games_button = tk.Button(
        root, text="📅 Show Upcoming Games", 
        command=lambda: threading.Thread(target=check_upcoming_games).start(),
        bg="lightyellow", width=25
    )
    games_button.pack(pady=5)
    
    # Test Game Day Tweet
    test_button = tk.Button(
        root, text="🧪 Post Test Tweet",
        command=lambda: threading.Thread(target=post_test_game_day_tweet).start(),
        bg="lightgreen", width=25
    )
    test_button.pack(pady=5)
    
    # Manual Game Day Tweet
    manual_button = tk.Button(
        root, text="🦁 Post Game Day Tweet Now",
        command=lambda: threading.Thread(target=post_game_day_tweet).start(),
        bg="orange", width=25
    )
    manual_button.pack(pady=5)
    
    # Start Scheduler
    scheduler_button = tk.Button(
        root, text="⏰ Start Auto Scheduler",
        command=lambda: threading.Thread(target=start_scheduler, daemon=True).start(),
        bg="lightcoral", width=25
    )
    scheduler_button.pack(pady=5)
    
    # Separator
    separator = tk.Label(root, text="─" * 40)
    separator.pack(pady=10)
    
    # Instructions text area
    instructions = tk.Text(root, height=12, width=45, wrap=tk.WORD)
    instructions.insert(tk.END, 
        "🦁 Detroit Lions Game Day Bot\n\n"
        "How it works:\n"
        "• Automatically posts at 10:00 AM on game days\n"
        "• Messages like 'Today the Detroit Lions vs [team], Go Lions!'\n"
        "• Uses #OnePride and team-specific hashtags\n\n"
        "Setup Instructions:\n"
        "1. Test authentication first\n"
        "2. Check upcoming games in schedule\n"
        "3. Test with a sample tweet\n"
        "4. Start the auto scheduler\n"
        "5. Keep the program running!\n\n"
        "Schedule Management:\n"
        "• Edit LIONS_SCHEDULE in code to add games\n"
        "• Format: 'YYYY-MM-DD': 'Team Name'\n"
        "• Restart app after adding games\n\n"
        "Current Features:\n"
        "✅ Manual posting\n"
        "✅ Scheduled posting (10:00 AM)\n"
        "✅ Dynamic messages\n"
        "✅ Team-specific hashtags"
    )
    instructions.config(state=tk.DISABLED)
    instructions.pack(pady=10)
    
    # Close button
    close_button = tk.Button(root, text="❌ Close", command=root.destroy, 
                           bg="lightgray", width=25)
    close_button.pack(pady=5)
    
    root.mainloop()

def start_scheduler():
    """Start the scheduler with setup"""
    schedule_game_day_posts()
    run_scheduler()

# ------------------------
# Main
# ------------------------
def main():
    print("🦁 Detroit Lions Game Day Bot")
    print("=" * 50)
    print(f"📅 Today: {datetime.date.today()}")
    
    # Check if there's a game today
    today_opponent = get_todays_opponent()
    if today_opponent:
        print(f"🏈 GAME DAY! Lions vs {today_opponent}")
    else:
        print("📅 No Lions game today")
    
    # Show upcoming games
    print("\n📅 Next few games:")
    check_upcoming_games()
    
    print("\n🚀 Launching GUI...")
    create_gui()

if __name__ == "__main__":
    main()