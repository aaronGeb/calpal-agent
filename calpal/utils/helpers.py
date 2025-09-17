"""
CalPal Helper Utilities
"""

import re
from datetime import datetime, timedelta
from typing import List, Optional


def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def extract_names(text: str) -> List[str]:
    """Extract potential names from text"""
    name_pattern = r'\b[A-Z][a-z]+\b'
    names = re.findall(name_pattern, text)
    # Filter out common non-name words
    exclude_words = {
        'Meeting', 'Lunch', 'Dinner', 'Call', 'Coffee', 'Team', 'Project',
        'Review', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday', 'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August', 'September', 'October', 'November',
        'December', 'Tomorrow', 'Today', 'Next', 'Week', 'Month', 'Year'
    }
    return [name for name in names if name not in exclude_words]


def parse_duration(text: str) -> int:
    """Parse duration from text and return minutes"""
    duration_pattern = r'(\d+)\s*(hour|hr|minute|min)'
    duration_match = re.search(duration_pattern, text, re.IGNORECASE)
    
    if duration_match:
        value = int(duration_match.group(1))
        unit = duration_match.group(2).lower()
        if unit in ['hour', 'hr']:
            return value * 60
        else:
            return value
    
    return 60  # Default 1 hour


def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime('%A, %B %d at %I:%M %p')


def get_next_weekday(weekday: int) -> datetime:
    """Get next occurrence of a weekday (0=Monday, 6=Sunday)"""
    today = datetime.now()
    days_ahead = weekday - today.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return today + timedelta(days=days_ahead)

