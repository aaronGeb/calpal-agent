"""
Calendar Agent - Handles Google Calendar operations
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import os
import re
from typing import List, Optional
import pickle

from .models import TimeSlot, CalendarEvent


class CalendarAgent:
    """Agent responsible for Google Calendar operations"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, credentials_file: str, token_file: str, calendar_id: Optional[str] = None):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.calendar_id = calendar_id or 'primary'
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def find_available_slots(self, duration_minutes: int, time_constraint: str, 
                           days_ahead: int = 7) -> List[TimeSlot]:
        """Find available time slots for a meeting"""
        try:
            # Parse time constraint to get start and end times
            start_time, end_time = self._parse_time_constraint(time_constraint, days_ahead)
            
            # Get busy times from calendar
            freebusy_query = {
                'timeMin': start_time.isoformat() + 'Z',
                'timeMax': end_time.isoformat() + 'Z',
                'items': [{'id': self.calendar_id}]
            }
            
            freebusy_result = self.service.freebusy().query(body=freebusy_query).execute()
            busy_times = freebusy_result['calendars'][self.calendar_id]['busy']
            
            # Find free slots
            available_slots = []
            current_time = start_time
            
            while current_time + timedelta(minutes=duration_minutes) <= end_time:
                slot_end = current_time + timedelta(minutes=duration_minutes)
                
                # Check if this slot conflicts with busy times
                is_free = True
                for busy_period in busy_times:
                    busy_start = datetime.fromisoformat(busy_period['start'].replace('Z', '+00:00'))
                    busy_end = datetime.fromisoformat(busy_period['end'].replace('Z', '+00:00'))
                    
                    # Convert to naive datetime for comparison
                    busy_start = busy_start.replace(tzinfo=None)
                    busy_end = busy_end.replace(tzinfo=None)
                    
                    if (current_time < busy_end and slot_end > busy_start):
                        is_free = False
                        break
                
                if is_free:
                    available_slots.append(TimeSlot(
                        start_time=current_time,
                        end_time=slot_end,
                        duration_minutes=duration_minutes
                    ))
                
                # Move to next 30-minute slot
                current_time += timedelta(minutes=30)
            
            return available_slots[:5]  # Return top 5 options
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def create_event(self, event: CalendarEvent) -> bool:
        """Create a calendar event"""
        try:
            event_body = {
                'summary': event.summary,
                'start': {
                    'dateTime': event.start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': event.end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'attendees': [{'email': email} for email in event.attendees],
            }
            
            if event.location:
                event_body['location'] = event.location
            
            if event.description:
                event_body['description'] = event.description
            
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event_body
            ).execute()
            
            print(f"Event created: {created_event.get('htmlLink')}")
            return True
            
        except HttpError as error:
            print(f"An error occurred while creating event: {error}")
            return False
    
    def _parse_time_constraint(self, time_constraint: str, days_ahead: int) -> tuple[datetime, datetime]:
        """Parse time constraint string to get start and end times"""
        now = datetime.now()
        
        # Simple parsing - in a real implementation, you'd use a more sophisticated parser
        if "tomorrow" in time_constraint.lower():
            start_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif "next week" in time_constraint.lower():
            start_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=7)
        elif "next thursday" in time_constraint.lower():
            days_until_thursday = (3 - now.weekday()) % 7
            if days_until_thursday == 0:
                days_until_thursday = 7
            start_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=days_until_thursday)
        else:
            # Default to next few days
            start_time = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        # Extract specific time if mentioned
        time_pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)?'
        time_match = re.search(time_pattern, time_constraint.lower())
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            period = time_match.group(3)
            
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            start_time = start_time.replace(hour=hour, minute=minute)
        
        end_time = start_time + timedelta(days=days_ahead)
        return start_time, end_time
