# CalPal API Documentation

## Core Module

### Models

#### MeetingRequest
Represents a structured meeting request parsed from natural language.

```python
from calpal.core import MeetingRequest

meeting = MeetingRequest(
    attendees=["john@example.com", "jane@example.com"],
    topic="Project Discussion",
    duration_minutes=60,
    time_constraint="next Thursday at 1pm",
    location="Conference Room A",
    description="Weekly project review"
)
```

#### TimeSlot
Represents an available time slot for scheduling.

```python
from calpal.core import TimeSlot
from datetime import datetime

slot = TimeSlot(
    start_time=datetime.now(),
    end_time=datetime.now(),
    duration_minutes=60
)
```

#### CalendarEvent
Represents a calendar event to be created.

```python
from calpal.core import CalendarEvent
from datetime import datetime

event = CalendarEvent(
    summary="Team Meeting",
    start_time=datetime.now(),
    end_time=datetime.now(),
    attendees=["team@example.com"]
)
```

### Agents

#### ParserAgent
Converts natural language to structured meeting data.

```python
from calpal.core import ParserAgent

parser = ParserAgent(google_api_key="your-key")
meeting = parser.parse("Lunch with John next Thursday at 1pm")
```

#### CalendarAgent
Handles Google Calendar operations.

```python
from calpal.core import CalendarAgent

calendar = CalendarAgent(
    credentials_file="credentials.json",
    token_file="token.json",
    calendar_id="primary"
)

# Find available slots
slots = calendar.find_available_slots(60, "next week")

# Create event
success = calendar.create_event(event)
```

#### SchedulerAgent
Orchestrates the complete scheduling workflow.

```python
from calpal.core import SchedulerAgent

scheduler = SchedulerAgent(parser, calendar)
success = scheduler.schedule_meeting("Lunch with John next Thursday at 1pm")
```

## CLI Module

### Command Line Interface

```bash
# Schedule a meeting
calpal schedule "Lunch with John next Thursday at 1pm"

# Check available slots
calpal check 60 "next week"

# Setup instructions
calpal setup
```

## Utilities

### Helper Functions

```python
from calpal.utils.helpers import extract_emails, parse_duration

emails = extract_emails("Contact john@example.com or jane@example.com")
duration = parse_duration("2 hours")  # Returns 120
```

## Exceptions

```python
from calpal.exceptions import ParsingError, CalendarError

try:
    meeting = parser.parse("invalid request")
except ParsingError as e:
    print(f"Parsing failed: {e}")
```

