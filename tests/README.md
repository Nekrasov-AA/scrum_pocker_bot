# 🧪 Scrum Poker Bot - Test Suite

This directory contains all tests for the Scrum Poker Bot project.

## 📁 Test Files

### `test_demo.py`
**Function Demonstration Test**
- 🎨 Media content verification (emoji, buttons)
- ⚙️ Settings configuration test  
- 📝 Command parsing verification
- 🗳️ Voting logic simulation
- 📨 Message formatting test

**Usage:**
```bash
python tests/test_demo.py
```

### `test_async.py`  
**Async Handlers Test**
- 🔄 Bot handler functions testing
- ⚡ Async operations verification
- 💬 Command processing simulation
- 🗂️ Session management testing

**Usage:**
```bash
python tests/test_async.py
```

### `run_all_tests.py`
**Test Suite Runner**
- 🚀 Automated execution of all tests
- 📊 Comprehensive test reporting
- ✅ Pass/fail status for each test
- 📋 Summary statistics

**Usage:**
```bash
python tests/run_all_tests.py
```

## 🎯 Test Purpose

These tests allow you to:

1. **Verify functionality** without running a real Telegram bot
2. **Check all components** work correctly after code changes  
3. **Understand bot behavior** through interactive demonstrations
4. **Validate async operations** and handler logic
5. **Test import dependencies** and module structure

## ✅ Test Requirements

- **No Telegram bot token needed** - tests use mock objects
- **No network connection required** - all operations are simulated
- **All dependencies must be installed** - run `pip install -r requirements.txt`
- **Python 3.8+ required** - for async/await support

## 🚀 Running Tests

### Quick Start
```bash
# From project root directory
cd /path/to/scrum_pocker_bot

# Activate virtual environment
source .venv/bin/activate

# Run all tests
python tests/run_all_tests.py
```

### Individual Tests
```bash
# Demo test - shows all bot functions
python tests/test_demo.py

# Async test - verifies async handlers
python tests/test_async.py
```

## 📊 Expected Output

All tests should show:
- ✅ **Green checkmarks** for passed operations
- 🎨 **Emoji and UI elements** working correctly  
- 📝 **Command parsing** functioning properly
- 🗳️ **Voting logic** operating as expected
- 📨 **Message formatting** displaying correctly

## 🐛 Troubleshooting

### Import Errors
If you see import errors:
```bash
# Make sure you're in the project root
cd /path/to/scrum_pocker_bot

# Check Python path
python -c "import sys; print(sys.path)"

# Install dependencies
pip install -r requirements.txt
```

### Path Issues
Tests automatically add parent directory to Python path:
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

## 📈 Test Development

To add new tests:

1. Create test file in `tests/` directory
2. Add import path adjustment at the top
3. Use mock objects for Telegram API calls
4. Add test to `run_all_tests.py` if needed
5. Follow existing naming convention

---

🎯 **Goal**: Ensure all bot functionality works correctly before deployment!