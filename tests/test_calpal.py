#!/usr/bin/env python3
"""
Simple test script for CalPal
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from calpal.core import MeetingRequest, TimeSlot, CalendarEvent
        print("Models imported successfully")
    except Exception as e:
        print(f"Failed to import models: {e}")
        return False
    
    try:
        from calpal.core import ParserAgent
        print("ParserAgent imported successfully")
    except Exception as e:
        print(f"Failed to import ParserAgent: {e}")
        return False
    
    try:
        from calpal.core import CalendarAgent
        print("CalendarAgent imported successfully")
    except Exception as e:
        print(f" Failed to import CalendarAgent: {e}")
        return False
    
    try:
        from calpal.core import SchedulerAgent
        print("SchedulerAgent imported successfully")
    except Exception as e:
        print(f"Failed to import SchedulerAgent: {e}")
        return False
    
    try:
        from calpal.cli import cli
        print("CLI imported successfully")
    except Exception as e:
        print(f"Failed to import CLI: {e}")
        return False
    
    return True

def test_models():
    """Test model creation"""
    print("\n Testing models...")
    
    try:
        from calpal.core import MeetingRequest, TimeSlot, CalendarEvent
        from datetime import datetime
        
        # Test MeetingRequest
        meeting = MeetingRequest(
            attendees=["john@example.com", "jane@example.com"],
            topic="Project Discussion",
            duration_minutes=60,
            time_constraint="next Thursday at 2pm"
        )
        print("MeetingRequest created successfully")
        
        # Test TimeSlot
        now = datetime.now()
        slot = TimeSlot(
            start_time=now,
            end_time=now,
            duration_minutes=60
        )
        print("TimeSlot created successfully")
        
        # Test CalendarEvent
        event = CalendarEvent(
            summary="Test Meeting",
            start_time=now,
            end_time=now,
            attendees=["test@example.com"]
        )
        print("CalendarEvent created successfully")
        
        return True
        
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("CalPal Test Suite")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Run tests
    tests = [
        test_imports,
        test_models,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! CalPal is ready to use.")
        print("\nNext steps:")
        print("1. Set up your Google AI API key: export GOOGLE_GENERATIVE_AI_API_KEY='your-key'")
        print("2. Set up Google Calendar credentials (see README)")
        print("3. Run: python -m calpal schedule 'Lunch with John next Thursday at 1pm'")
    else:
        print("Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

