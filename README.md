# 🦁 Detroit Lions Game Day Bot

An automated Twitter bot that posts game day messages for Detroit Lions fans! The bot automatically tweets "Today the Detroit Lions vs [team], Go Lions!" at 10:00 AM on game days with dynamic messages and team-specific hashtags.

## ✨ Features

- 🕙 **Automatic Scheduling**: Posts at 10:00 AM on game days
- 🎲 **Dynamic Messages**: 10+ different message templates with random variations
- 🏷️ **Smart Hashtags**: Team-specific hashtags for each opponent
- 📊 **Real-time GUI**: Live activity log with professional interface
- 🔒 **Duplicate Prevention**: Smart uniqueness system prevents Twitter blocks
- ⚡ **Easy Controls**: Start/stop scheduler, manual posting, testing

## 🏈 Example Tweets

- "🦁 TODAY'S THE DAY! Detroit Lions vs Green Bay Packers! Go Lions! ⚡ #OnePride #DivisionRival"
- "🏈 Good morning Lions fans! GAME DAY! Lions take on the Chicago Bears today! Let's roar! #OnePride #DivisionRival"
- "🔥 Lions vs Kansas City Chiefs TODAY! Detroit vs Everybody! Let's get this W! 💯 #OnePride #SuperBowlChamps"

## 📋 Prerequisites

### Twitter Developer Account
1. Apply for a Twitter Developer account at [developer.twitter.com](https://developer.twitter.com)
2. Create a new project/app
3. Generate your API keys:
   - Consumer Key
   - Consumer Secret
   - Access Token
   - Access Token Secret
4. Set app permissions to **"Read and Write"**

### Python Requirements
- Python 3.7 or higher
- Required packages (install via pip)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/lions-game-day-bot.git
cd lions-game-day-bot
```

### 2. Install Dependencies
```bash
pip install tweepy schedule tkinter
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Create Configuration File
Create a file named `config.py` in the project directory:

```python
# config.py
CONSUMER_KEY = "your_consumer_key_here"
CONSUMER_SECRET = "your_consumer_secret_here"
ACCESS_TOKEN = "your_access_token_here"
ACCESS_TOKEN_SECRET = "your_access_token_secret_here"
```

**⚠️ Keep your keys private! Add config.py to .gitignore**

### 4. Update Game Schedule
Edit the `LIONS_SCHEDULE` dictionary in `main.py` with current season games:

```python
LIONS_SCHEDULE = {
    "2025-09-07": "Green Bay Packers",
    "2025-09-14": "Chicago Bears",
    # Add more games here...
}
```

## 🎮 Usage

### Starting the Bot
```bash
python main.py
```

This launches the GUI interface with two main sections:
- **Left Panel**: Control buttons and status
- **Right Panel**: Live activity log

### GUI Controls

| Button | Function |
|--------|----------|
| 🔐 Test Auth | Verify Twitter API connection |
| 📅 Show Games | Display upcoming Lions games |
| 🧪 Test Tweet | Post a test tweet to verify functionality |
| 🦁 Post Now | Manually post game day tweet (if there's a game today) |
| ▶️ Start Auto | Start automatic scheduler (posts at 10:00 AM) |
| ⏹️ Stop Auto | Stop automatic scheduler |
| 🧹 Clear Logs | Clear the activity log display |

### Step-by-Step Setup

1. **Test Authentication**
   - Click "🔐 Test Auth" to verify your API keys work
   - Should show your Twitter username in the log

2. **Check Schedule**
   - Click "📅 Show Games" to see upcoming Lions games
   - Update the schedule if games are missing

3. **Test Functionality**
   - Click "🧪 Test Tweet" to post a test message
   - Verify it appears on your Twitter account

4. **Start Automation**
   - Click "▶️ Start Auto" to begin scheduled posting
   - Status will change to "▶️ Running" (green)
   - Keep the program running for automatic posts

## ⚙️ Customization

### Adding Games
Edit `LIONS_SCHEDULE` in `main.py`:
```python
LIONS_SCHEDULE = {
    "YYYY-MM-DD": "Opponent Team Name",
    "2025-09-07": "Green Bay Packers",
    # Add new games here
}
```

### Custom Messages
Modify the `messages` list in `create_game_day_message()`:
```python
messages = [
    f"🦁 YOUR CUSTOM MESSAGE vs {opponent}!",
    f"🏈 Another custom message for {opponent}!",
    # Add more variations
]
```

### Team-Specific Hashtags
Update `TEAM_HASHTAGS` dictionary:
```python
TEAM_HASHTAGS = {
    "Green Bay Packers": "#OnePride #DivisionRival #GoPackGo",
    "Your Team": "#OnePride #YourHashtags",
}
```

### Change Post Time
Modify the schedule in `schedule_game_day_posts()`:
```python
schedule.every().day.at("08:00").do(post_game_day_tweet)  # 8:00 AM instead
```

## 🛠️ Troubleshooting

### Common Issues

**❌ 401 Unauthorized**
- Check your API keys in `config.py`
- Ensure app permissions are "Read and Write"
- Regenerate keys if needed

**❌ 403 Forbidden - Duplicate Content**
- Bot has built-in duplicate prevention
- If still occurs, restart the bot
- Each message includes unique timestamps and IDs

**❌ No Games Showing**
- Update `LIONS_SCHEDULE` with current season games
- Use format: `"YYYY-MM-DD": "Team Name"`
- Restart the application after updates

**❌ Scheduler Not Working**
- Ensure bot is running continuously
- Check system time is correct
- Restart scheduler if needed

### Twitter API Limitations

**Basic Tier (Free)**
- ✅ Can post tweets
- ✅ Can use this bot
- ❌ Cannot search tweets (not needed for this bot)

**Rate Limits**
- 300 tweets per 15-minute window
- Bot posts once per game day, well within limits

## 📁 Project Structure

```
lions-game-day-bot/
├── main.py           # Main bot application
├── config.py         # API keys (create this)
├── README.md         # This file
├── requirements.txt  # Python dependencies
└─