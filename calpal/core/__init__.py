"""
CalPal Core Module

Contains the core functionality including models, agents, and business logic.
"""

from .models import MeetingRequest, TimeSlot, CalendarEvent
from .parser_agent import ParserAgent
from .calendar_agent import CalendarAgent
from .scheduler_agent import SchedulerAgent

__all__ = [
    'MeetingRequest',
    'TimeSlot', 
    'CalendarEvent',
    'ParserAgent',
    'CalendarAgent',
    'SchedulerAgent'
]