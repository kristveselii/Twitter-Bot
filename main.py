import tweepy
import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import time
import schedule
import datetime
from config import *

# ------------------------
# Global GUI Components
# ------------------------
log_display = None

def log_to_gui(message):
    """Add a log message to the GUI display"""
    global log_display
    if log_display:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Thread-safe GUI update
        log_display.after(0, lambda: _update_log_display(formatted_message))
    
    # Also print to terminal for backup
    print(message)

def _update_log_display(message):
    """Update the log display in a thread-safe way"""
    global log_display
    if log_display:
        log_display.config(state=tk.NORMAL)
        log_display.insert(tk.END, message)
        log_display.see(tk.END)  # Auto-scroll to bottom
        log_display.config(state=tk.DISABLED)

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
    "Dallas Cowboys": "#OnePride #AmericasTeam",
    "Los Angeles Rams": "#OnePride #WestCoastBattle",
    "Pittsburgh Steelers": "#OnePride #SteelCityShowdown",
    "Philadelphia Eagles": "#OnePride #NFCShowdown",
    "New York Giants": "#OnePride #BigAppleBattle",
    "Detroit Lions": "#OnePride",  # Self-reference
    "TBD": "#OnePride #PlayoffBound"
}

# Scheduler status
scheduler_running = False

# ------------------------
# Game Day Functions
# ------------------------
def get_todays_opponent():
    """Check if Lions play today and return opponent"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    return LIONS_SCHEDULE.get(today)

def create_game_day_message(opponent):
    """Create a game day message with unique elements"""
    current_time = datetime.datetime.now()
    
    # Base messages with more variety
    messages = [
        f"🦁 TODAY'S THE DAY! Detroit Lions vs {opponent}! Go Lions!",
        f"🏈 GAME DAY! Lions take on the {opponent} today! Let's roar!",
        f"⚡ IT'S GAME DAY! Detroit Lions vs {opponent}! Time to show them what we're made of!",
        f"🔥 Lions vs {opponent} TODAY! Detroit vs Everybody! Let's get this W!",
        f"🦁 ROAR! Game day is here! Detroit Lions vs {opponent}!",
        f"🌟 GAME TIME! Lions ready to battle {opponent}! One Pride!",
        f"💪 Lions Nation, it's time! Detroit vs {opponent} today!",
        f"🏆 Big game alert! Lions face {opponent}! Let's go Detroit!",
        f"⚡ Electric atmosphere! Lions vs {opponent} - Game Day!",
        f"🔴 Red zone ready! Lions vs {opponent} kicks off today!"
    ]
    
    # Add time-based variations to make posts more unique
    if current_time.hour < 12:
        time_prefix = "Good morning Lions fans! "
    elif current_time.hour < 17:
        time_prefix = "Afternoon Lions faithful! "
    else:
        time_prefix = "Evening roar! "
    
    base_message = random.choice(messages)
    
    # Sometimes add the time prefix for variety
    if random.random() < 0.3:  # 30% chance
        base_message = time_prefix + base_message
    
    # Get hashtags for the opponent
    hashtags = TEAM_HASHTAGS.get(opponent, "#OnePride #DetroitVsEverybody")
    
    # Occasionally add extra flair
    extra_flair = [
        "", "", "",  # Empty strings to make it less frequent
        " 🌟", " ⚡", " 💯", " 🔥", " 💪"
    ]
    
    flair = random.choice(extra_flair)
    
    return f"{base_message}{flair} {hashtags}"

def post_game_day_tweet():
    """Post the game day tweet if Lions play today"""
    try:
        opponent = get_todays_opponent()
        
        if opponent:
            message = create_game_day_message(opponent)
            response = client.create_tweet(text=message)
            
            log_to_gui(f"🦁 GAME DAY TWEET POSTED!")
            log_to_gui(f"   Opponent: {opponent}")
            log_to_gui(f"   Message: {message}")
            log_to_gui(f"   Tweet ID: {response.data['id']}")
            
            return True
        else:
            log_to_gui(f"📅 No Lions game today ({datetime.date.today()})")
            return False
            
    except Exception as e:
        log_to_gui(f"❌ Error posting game day tweet: {e}")
        return False

def schedule_game_day_posts():
    """Schedule the 10:00 AM game day posts"""
    global scheduler_running
    schedule.clear()  # Clear any existing schedules
    schedule.every().day.at("10:00").do(post_game_day_tweet)
    scheduler_running = True
    log_to_gui("⏰ Scheduled game day tweets for 10:00 AM daily")

def run_scheduler():
    """Run the scheduler continuously"""
    global scheduler_running
    log_to_gui("🔄 Starting tweet scheduler...")
    log_to_gui(f"📅 Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while scheduler_running:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
    
    log_to_gui("⏹️ Scheduler stopped")

def stop_scheduler():
    """Stop the scheduler"""
    global scheduler_running
    scheduler_running = False
    schedule.clear()
    log_to_gui("⏹️ Stopping scheduler...")

# ------------------------
# Manual Functions
# ------------------------
def test_authentication():
    """Test if authentication is working properly"""
    try:
        log_to_gui("🔐 Testing authentication...")
        me = client.get_me()
        log_to_gui(f"✅ Authentication successful! Logged in as: @{me.data.username}")
        return True
    except Exception as e:
        log_to_gui(f"❌ Authentication failed: {e}")
        return False

def post_test_game_day_tweet():
    """Manually post a test game day tweet"""
    try:
        log_to_gui("🧪 Posting test tweet...")
        
        # Create unique test messages with timestamp and random elements
        timestamp = datetime.datetime.now().strftime("%H:%M")
        unique_id = random.randint(1000, 9999)
        
        opponent = get_todays_opponent()
        
        if opponent:
            # If there's a game today, create a test version of the game day message
            test_messages = [
                f"🧪 TEST [{timestamp}]: {create_game_day_message(opponent)} #TestBot{unique_id}",
                f"🔧 TESTING Game Day Tweet at {timestamp} - Lions vs {opponent}! #OnePride #Test{unique_id}",
                f"⚡ TEST RUN {unique_id}: Game Day message ready! Lions vs {opponent} 🦁 #TestTweet"
            ]
        else:
            # Find the next scheduled game for testing
            today = datetime.date.today()
            upcoming_games = []
            
            for date_str, team in LIONS_SCHEDULE.items():
                game_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                if game_date >= today:
                    upcoming_games.append((game_date, team))
            
            if upcoming_games:
                upcoming_games.sort()
                next_game_date, next_opponent = upcoming_games[0]
                days_until = (upcoming_games[0][0] - today).days
                
                test_messages = [
                    f"🧪 BOT TEST [{timestamp}]: Next Lions game in {days_until} days vs {next_opponent}! #OnePride #Test{unique_id}",
                    f"🔧 Testing at {timestamp} - Lions vs {next_opponent} on {next_game_date.strftime('%B %d')}! #TestBot{unique_id}",
                    f"⚡ Lions Bot Test #{unique_id}: Ready for {next_opponent} game! 🦁 #OnePride #Testing"
                ]
            else:
                test_messages = [
                    f"🧪 Lions Bot Test #{unique_id} at {timestamp}! Ready to roar! 🦁 #OnePride #TestTweet",
                    f"🔧 Bot Status Check [{timestamp}]: Detroit Lions Game Day Bot operational! #Test{unique_id}",
                    f"⚡ Testing Lions Bot #{unique_id} - All systems go! #OnePride #DetroitVsEverybody"
                ]
        
        # Choose a random test message to ensure uniqueness
        test_message = random.choice(test_messages)
        
        response = client.create_tweet(text=test_message)
        log_to_gui(f"✅ Test tweet posted successfully!")
        log_to_gui(f"   Message: {test_message}")
        log_to_gui(f"   Tweet ID: {response.data['id']}")
        
    except tweepy.Forbidden as e:
        if "duplicate content" in str(e).lower():
            log_to_gui(f"❌ Duplicate content detected. Trying again with different message...")
            # Try one more time with extra randomization
            try:
                extra_unique = f"Test{random.randint(10000, 99999)}"
                fallback_message = f"🧪 Lions Bot Test {extra_unique} at {datetime.datetime.now().strftime('%H:%M:%S')}! #OnePride #Testing"
                response = client.create_tweet(text=fallback_message)
                log_to_gui(f"✅ Fallback test tweet posted!")
                log_to_gui(f"   Message: {fallback_message}")
            except Exception as e2:
                log_to_gui(f"❌ Still failed: {e2}")
        else:
            log_to_gui(f"❌ Forbidden error: {e}")
    except Exception as e:
        log_to_gui(f"❌ Error posting test tweet: {e}")

def check_upcoming_games():
    """Display upcoming Lions games"""
    log_to_gui("📅 Detroit Lions Upcoming Games:")
    log_to_gui("=" * 50)
    
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
                log_to_gui(f"🦁 TODAY: vs {opponent}")
            elif days_until == 1:
                log_to_gui(f"📅 TOMORROW: vs {opponent}")
            else:
                log_to_gui(f"📅 {game_date.strftime('%B %d, %Y')} ({days_until} days): vs {opponent}")
    else:
        log_to_gui("No upcoming games scheduled in the database")
        log_to_gui("Update LIONS_SCHEDULE in the code with new games")

def clear_logs():
    """Clear the log display"""
    global log_display
    if log_display:
        log_display.config(state=tk.NORMAL)
        log_display.delete(1.0, tk.END)
        log_display.config(state=tk.DISABLED)
        log_to_gui("🧹 Logs cleared")

# ------------------------
# GUI
# ------------------------
def create_gui():
    """Create the main GUI interface"""
    global log_display
    
    root = tk.Tk()
    root.title("Detroit Lions Game Day Bot")
    root.geometry("800x700")
    
    # Create main frame with two columns
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Left column - Controls
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    
    # Right column - Log display
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # === LEFT COLUMN - CONTROLS ===
    
    # Title
    title_label = tk.Label(left_frame, text="🦁 Detroit Lions\nGame Day Bot", 
                          font=("Arial", 14, "bold"), fg="blue")
    title_label.pack(pady=10)
    
    # Current status
    today_opponent = get_todays_opponent()
    if today_opponent:
        status_text = f"🏈 GAME DAY!\nvs {today_opponent}"
        status_color = "red"
    else:
        status_text = "📅 No game today"
        status_color = "gray"
    
    status_label = tk.Label(left_frame, text=status_text, font=("Arial", 10), 
                           fg=status_color, justify=tk.CENTER)
    status_label.pack(pady=5)
    
    # Separator
    tk.Label(left_frame, text="─" * 20).pack(pady=5)
    
    # Control buttons
    buttons = [
        ("🔐 Test Auth", test_authentication, "lightblue"),
        ("📅 Show Games", check_upcoming_games, "lightyellow"), 
        ("🧪 Test Tweet", post_test_game_day_tweet, "lightgreen"),
        ("🦁 Post Now", post_game_day_tweet, "orange"),
    ]
    
    for text, command, color in buttons:
        btn = tk.Button(left_frame, text=text,
                       command=lambda cmd=command: threading.Thread(target=cmd).start(),
                       bg=color, width=15, height=2)
        btn.pack(pady=3)
    
    # Scheduler controls
    tk.Label(left_frame, text="─" * 20).pack(pady=5)
    tk.Label(left_frame, text="Scheduler", font=("Arial", 10, "bold")).pack()
    
    global scheduler_status_label
    scheduler_status_label = tk.Label(left_frame, text="⏹️ Stopped", fg="red")
    scheduler_status_label.pack(pady=2)
    
    start_btn = tk.Button(left_frame, text="▶️ Start Auto",
                         command=lambda: start_scheduler_gui(),
                         bg="lightcoral", width=15)
    start_btn.pack(pady=2)
    
    stop_btn = tk.Button(left_frame, text="⏹️ Stop Auto", 
                        command=stop_scheduler,
                        bg="lightgray", width=15)
    stop_btn.pack(pady=2)
    
    # Log controls
    tk.Label(left_frame, text="─" * 20).pack(pady=5)
    tk.Label(left_frame, text="Logs", font=("Arial", 10, "bold")).pack()
    
    clear_btn = tk.Button(left_frame, text="🧹 Clear Logs",
                         command=clear_logs,
                         bg="lightyellow", width=15)
    clear_btn.pack(pady=2)
    
    # Close button
    tk.Label(left_frame, text="─" * 20).pack(pady=5)
    close_button = tk.Button(left_frame, text="❌ Close", 
                           command=root.destroy, 
                           bg="lightcoral", width=15)
    close_button.pack(pady=5)
    
    # === RIGHT COLUMN - LOG DISPLAY ===
    
    log_frame_label = tk.Label(right_frame, text="📋 Activity Log", 
                              font=("Arial", 12, "bold"))
    log_frame_label.pack(anchor=tk.W)
    
    # Create scrolled text widget for logs
    log_display = scrolledtext.ScrolledText(
        right_frame, 
        width=50, 
        height=35,
        wrap=tk.WORD,
        font=("Consolas", 9),
        bg="black",
        fg="green",
        state=tk.DISABLED
    )
    log_display.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    # Initial welcome message
    log_to_gui("🦁 Detroit Lions Game Day Bot Initialized")
    log_to_gui(f"📅 Today: {datetime.date.today()}")
    log_to_gui("Ready for commands!")
    
    root.mainloop()

def start_scheduler_gui():
    """Start scheduler with GUI updates"""
    global scheduler_status_label
    
    def run_with_status():
        scheduler_status_label.config(text="▶️ Running", fg="green")
        schedule_game_day_posts()
        run_scheduler()
        scheduler_status_label.config(text="⏹️ Stopped", fg="red")
    
    threading.Thread(target=run_with_status, daemon=True).start()

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
    
    print("\n🚀 Launching GUI...")
    create_gui()

if __name__ == "__main__":
    main()