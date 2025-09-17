"""
Data models for CalPal
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MeetingRequest(BaseModel):
    """Structured meeting request data"""
    attendees: List[str]
    topic: str
    duration_minutes: int
    time_constraint: str  # e.g., "next Thursday at 1pm", "tomorrow morning"
    location: Optional[str] = None
    description: Optional[str] = None


class TimeSlot(BaseModel):
    """Available time slot for meeting"""
    start_time: datetime
    end_time: datetime
    duration_minutes: int


class CalendarEvent(BaseModel):
    """Calendar event data"""
    summary: str
    start_time: datetime
    end_time: datetime
    attendees: List[str]
    location: Optional[str] = None
    description: Optional[str] = None



