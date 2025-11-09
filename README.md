# Scrum Poker Bot

Telegram bot for conducting Planning Poker / Scrum Poker voting sessions in development teams.

## 🎯 How it works

1. **Add the bot to your team's group chat** in Telegram
2. **User sends Jira ticket link** using `/poll` command
3. **Bot creates a poll** - how many story points the ticket is worth
4. **After all participants vote** bot sends the results

## 🚀 Quick Start

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather)
2. Create a bot: `/newbot`
3. Follow instructions, get the token
4. Put token in `API_KEY` file:

```bash
echo "1234567890:AAEhLiunEZefLuWk4k4Bjijugjuj12345" > API_KEY
```

### 2. Setup Jira

Edit `settings.py`:

```python
JIRA_LINK = 'https://your-company.atlassian.net/browse/'
```

### 3. Installation and Launch

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## 📱 Usage

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Greeting | `/start` |
| `/poll` | Start voting | `/poll PROJ-123 @alice @bob @charlie` |

### 🗳 Voting Process

1. **Create voting session:**
   ```
   /poll PROJ-123 @alice @bob @charlie
   ```

2. **Bot creates message with buttons:**
   - ☕ 0.5 point
   - 1️⃣ 1 point  
   - 2️⃣ 2 points
   - 3️⃣ 3 points
   - 5️⃣ 5 points
   - 8️⃣ 8 points
   - 🔚 End voting

3. **During voting** participants see emoji instead of numbers
4. **After everyone votes** real estimates are shown
5. **New voting**: just send new ticket ID

### 📊 Example Session

```
👤 User: /poll FEAT-456 @alice @bob @charlie

🤖 Bot: 🚨 Rate ticket: https://company.atlassian.net/browse/FEAT-456
alice: -
bob: -  
charlie: -
[Voting buttons]

# After alice votes (3 points):
🤖 Bot: 🚨 Rate ticket: https://company.atlassian.net/browse/FEAT-456
alice: 🎉
bob: -
charlie: -

# After everyone votes:
🤖 Bot: Voting ended for FEAT-456
alice: 3
bob: 5
charlie: 2
```

## 🔧 Technical Details

### Architecture

```
bot.py          # 🚀 Main file, bot launcher
├── commands.py # 📋 Commands dictionary
├── handlers.py # 🔄 Event handlers  
├── session.py  # 🗳 Voting session logic
├── media_content.py # 🎨 UI elements
├── settings.py # ⚙️ Configuration
└── tests/      # 🧪 Test suite
    ├── __init__.py       # Test package
    ├── test_demo.py      # Function demos
    ├── test_async.py     # Async handler tests
    └── run_all_tests.py  # Test runner
```

### Dependencies

- **Python 3.8+**
- **python-telegram-bot 20.7** (async version)
- **emoji 0.6.0**

### Features

- ✅ **Async architecture** - high performance
- 🔒 **Hidden votes** - emoji instead of numbers during voting
- 🔄 **Participant reuse** - new voting sessions with same participants
- 🌐 **Jira integration** - automatic ticket links
- 🎨 **Rich UI** - emoji and inline buttons

## 🧪 Testing

Project includes a comprehensive test suite in the `tests/` directory:

```bash
# Run all tests with test runner
python tests/run_all_tests.py

# Or run individual tests:
python tests/test_demo.py      # Demo of all functions
python tests/test_async.py     # Test async handlers
```

### Test Coverage:
- ✅ **Function Demo** (`test_demo.py`) - Showcase of all bot components
- ✅ **Async Handlers** (`test_async.py`) - Bot handlers and async operations  
- ✅ **Test Runner** (`run_all_tests.py`) - Automated test execution

## 🐛 Debugging

### Common Issues

1. **"Import telegram could not be resolved"**
   ```bash
   pip install python-telegram-bot==20.7
   ```

2. **"API_KEY file not found"**
   ```bash
   echo "YOUR_BOT_TOKEN" > API_KEY
   ```

3. **"Invalid token"**
   - Check token with @BotFather
   - Make sure there are no extra spaces in API_KEY

### Logging

Detailed logging is enabled in `bot.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔮 Future Plans (TODO)

- [ ] 🔧 Environment variables support
- [ ] 💾 Voting history storage  
- [ ] 📊 Export results to CSV/JSON
- [ ] 🎚 Custom story points values
- [ ] 🔗 User validation via Jira API
- [ ] 📈 Statistics and analytics
- [ ] 🌍 Multi-language support
- [ ] 👥 Participant role management

## 📄 License

Open source project. Use freely!

---

💡 **Tip:** For productive work, it's recommended to add the bot only to development team group chats.