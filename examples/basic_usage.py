#!/usr/bin/env python3
"""
CalPal Basic Usage Example

This example shows how to use CalPal programmatically.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calpal.core import ParserAgent, CalendarAgent, SchedulerAgent


def main():
    """Basic usage example"""
    print("CalPal Basic Usage Example")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_GENERATIVE_AI_API_KEY')
    if not api_key:
        print("Error: GOOGLE_GENERATIVE_AI_API_KEY not found")
        return
    
    try:
        # Initialize parser
        print("Initializing ParserAgent...")
        parser = ParserAgent(api_key)
        
        # Parse a meeting request
        request = "Lunch with John next Thursday at 1pm"
        print(f"\nParsing: '{request}'")
        
        meeting = parser.parse(request)
        print(f"Topic: {meeting.topic}")
        print(f"Attendees: {', '.join(meeting.attendees)}")
        print(f"Duration: {meeting.duration_minutes} minutes")
        print(f"Time constraint: {meeting.time_constraint}")
        
        print("\n✓ Parsing successful!")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

