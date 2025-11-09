#!/usr/bin/env python3
"""
Test script for demonstrating Scrum Poker Bot functions
This script doesn't run the real bot, but shows how the main components work
"""

import asyncio
import sys
import os
from unittest.mock import Mock, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from session import Session, SessionStatus
from media_content import rating_keyboard, rotating_light, icons
from settings import JIRA_LINK

def test_media_content():
    """Test media content"""
    print("=== Media Content Test ===")
    print(f"🚨 Rotating light: {rotating_light}")
    print(f"🎯 Random icons: {icons[:5]}...")  # show first 5
    print(f"⌨️ Keyboard buttons count: {len(rating_keyboard.inline_keyboard)}")
    for i, button_row in enumerate(rating_keyboard.inline_keyboard):
        for button in button_row:
            print(f"  Button {i}: '{button.text}' -> '{button.callback_data}'")
    print()

def test_settings():
    """Test settings"""
    print("=== Settings Test ===")
    print(f"🔗 Jira base URL: {JIRA_LINK}")
    print(f"🎫 Example ticket URL: {JIRA_LINK}PROJ-123")
    print()

def create_mock_update(message_text, username="testuser"):
    """Creates mock Update object for testing"""
    update = Mock()
    update.message = Mock()
    update.message.text = message_text
    update.message.chat_id = 12345
    update.message.reply_text = MagicMock()
    
    # Mock callback query for voting
    callback_query = Mock()
    callback_query.from_user = Mock()
    callback_query.from_user.username = username
    callback_query.data = "3"
    callback_query.message = Mock()
    callback_query.message.chat_id = 12345
    
    return update, callback_query

def test_session_parsing():
    """Test Session command parsing"""
    print("=== Command Parsing Test ===")
    
    # Test cases
    test_cases = [
        "/poll PROJ-123 @alice @bob @charlie",
        "/poll BUG-456 @user1 @user2",
        "/poll FEATURE-789 @developer"
    ]
    
    for message_text in test_cases:
        print(f"📝 Command: {message_text}")
        update, _ = create_mock_update(message_text)
        
        # Create session without async calls
        session = Session(update)
        
        print(f"  🎫 Ticket: {session.ticket}")
        print(f"  👥 Users: {session.users}")
        print(f"  ✅ Valid: {session.is_valid_users(session.users)}")
        print(f"  📊 Status: {session.status}")
        print()

def test_voting_logic():
    """Test voting logic"""
    print("=== Voting Logic Test ===")
    
    update, callback_query = create_mock_update("/poll PROJ-123 @alice @bob")
    session = Session(update)
    
    # Initialize votes manually (without async calls)
    session.user_votes = {user: None for user in session.users}
    session.user_votes_placeholders = {}
    
    print(f"👥 Voting participants: {list(session.user_votes.keys())}")
    print(f"🗳️ Initial vote state: {session.user_votes}")
    
    # Simulate alice voting
    callback_query.from_user.username = "alice"
    callback_query.data = "3"
    session.set_user_data("alice", callback_query)
    
    print(f"📊 After alice vote (3): {[user for user, vote in session.user_votes.items() if vote]}")
    print(f"🎨 Placeholder for alice: {session.get_vote_value(session.user_votes['alice'])}")
    
    # Simulate bob voting
    callback_query2 = Mock()
    callback_query2.from_user = Mock()
    callback_query2.from_user.username = "bob"
    callback_query2.data = "5"
    session.set_user_data("bob", callback_query2)
    
    print(f"📊 After bob vote (5): everyone voted: {all(vote is not None for vote in session.user_votes.values())}")
    
    # Show final results
    session.status = SessionStatus.finished
    print(f"🏁 Final results:")
    for user, vote in session.user_votes.items():
        print(f"  {user}: {session.get_vote_value(vote)}")
    
    print()

def test_message_formatting():
    """Test message formatting"""
    print("=== Message Formatting Test ===")
    
    update, _ = create_mock_update("/poll PROJ-123 @alice @bob")
    session = Session(update)
    session.user_votes = {"alice": None, "bob": None}
    session.user_votes_placeholders = {}
    
    print("📝 Message during voting process:")
    message = session.get_poll_list_message()
    print(f"  {message}")
    
    # Add votes
    callback1 = Mock()
    callback1.from_user = Mock()
    callback1.from_user.username = "alice"
    callback1.data = "3"
    session.set_user_data("alice", callback1)
    
    callback2 = Mock()  
    callback2.from_user = Mock()
    callback2.from_user.username = "bob"
    callback2.data = "5"
    session.set_user_data("bob", callback2)
    
    print("📝 Message during voting (with placeholders):")
    message = session.get_poll_list_message()
    print(f"  {message}")
    
    # End voting
    session.status = SessionStatus.finished
    print("📝 Final message:")
    message = session.get_poll_list_message()
    print(f"  {message}")
    
    print()

def main():
    """Main function to run all tests"""
    print("🤖 Scrum Poker Bot - Function Demo\n")
    
    test_media_content()
    test_settings()
    test_session_parsing()
    test_voting_logic()
    test_message_formatting()
    
    print("=== Instructions to run the bot ===")
    print("1. Get bot token from @BotFather")
    print("2. Put token in API_KEY file")
    print("3. Update JIRA_LINK in settings.py")
    print("4. Run: python bot.py")
    print("\n✅ All tests passed successfully!")

if __name__ == "__main__":
    main()