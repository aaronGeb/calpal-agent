#!/usr/bin/env python3
"""
Test CalPal parsing functionality with Google AI
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_parsing():
    """Test the parsing functionality"""
    print("Testing CalPal Parsing with Google AI")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
    if not api_key:
        print("Error: GOOGLE_GENERATIVE_AI_API_KEY not found in environment")
        return False
    
    try:
        from calpal.core import ParserAgent
        
        # Initialize parser
        print("Initializing ParserAgent...")
        parser = ParserAgent(api_key)
        
        # Test cases
        test_cases = [
            "Lunch with John next Thursday at 1pm",
            "Team meeting tomorrow at 9am for 2 hours",
            "Coffee with Sarah and Mike next week",
            "Project review with the team on Friday at 3pm for 90 minutes"
        ]
        
        print("\nTesting natural language parsing...")
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}: '{test_case}'")
            try:
                result = parser.parse(test_case)
                print(f"  Topic: {result.topic}")
                print(f"  Attendees: {', '.join(result.attendees)}")
                print(f"  Duration: {result.duration_minutes} minutes")
                print(f"  Time constraint: {result.time_constraint}")
                print("  ✓ Parsed successfully")
            except Exception as e:
                print(f"  ✗ Failed to parse: {e}")
                return False
        
        print("\n✓ All parsing tests passed!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_parsing()
    if success:
        print("\n🎉 CalPal parsing is working perfectly with Google AI!")
        print("\nTo test full functionality, you'll need to:")
        print("1. Set up Google Calendar API credentials")
        print("2. Run: calpal schedule 'Your meeting request'")
    else:
        print("\n❌ Parsing tests failed")
        sys.exit(1)

