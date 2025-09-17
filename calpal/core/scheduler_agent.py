"""
Scheduler Agent - Orchestrates the meeting scheduling workflow
"""

from typing import List

from .models import TimeSlot, CalendarEvent
from .parser_agent import ParserAgent
from .calendar_agent import CalendarAgent


class SchedulerAgent:
    """Main orchestrator agent that coordinates the scheduling workflow"""
    
    def __init__(self, parser_agent: ParserAgent, calendar_agent: CalendarAgent):
        self.parser_agent = parser_agent
        self.calendar_agent = calendar_agent
    
    def schedule_meeting(self, natural_language_request: str) -> bool:
        """Main method to schedule a meeting from natural language"""
        print(f"Processing request: '{natural_language_request}'")
        
        # Step 1: Parse the natural language request
        print("Parsing meeting details...")
        try:
            meeting_request = self.parser_agent.parse(natural_language_request)
            print(f"Parsed meeting: {meeting_request.topic}")
            print(f"   Attendees: {', '.join(meeting_request.attendees)}")
            print(f"   Duration: {meeting_request.duration_minutes} minutes")
            print(f"   Time constraint: {meeting_request.time_constraint}")
        except Exception as e:
            print(f"Failed to parse meeting request: {e}")
            return False
        
        # Step 2: Find available time slots
        print("Finding available time slots...")
        try:
            available_slots = self.calendar_agent.find_available_slots(
                duration_minutes=meeting_request.duration_minutes,
                time_constraint=meeting_request.time_constraint
            )
            
            if not available_slots:
                print("No available time slots found")
                return False
            
            print(f"Found {len(available_slots)} available slots:")
            for i, slot in enumerate(available_slots, 1):
                print(f"   {i}. {slot.start_time.strftime('%A, %B %d at %I:%M %p')}")
            
        except Exception as e:
            print(f" Failed to find available slots: {e}")
            return False
        
        # Step 3: Propose time to user and get confirmation
        print("\nProposed meeting time:")
        proposed_slot = available_slots[0]  # Use the first available slot
        print(f"{proposed_slot.start_time.strftime('%A, %B %d at %I:%M %p')}")
        print(f"  Duration: {proposed_slot.duration_minutes} minutes")
        
        # In a real CLI, you'd get user input here
        # For now, we'll auto-confirm the first slot
        confirmation = self._get_user_confirmation(proposed_slot)
        
        if not confirmation:
            print("Meeting scheduling cancelled")
            return False
        
        # Step 4: Create the calendar event
        print("Creating calendar event...")
        try:
            calendar_event = CalendarEvent(
                summary=meeting_request.topic,
                start_time=proposed_slot.start_time,
                end_time=proposed_slot.end_time,
                attendees=meeting_request.attendees,
                location=meeting_request.location,
                description=meeting_request.description
            )
            
            success = self.calendar_agent.create_event(calendar_event)
            
            if success:
                print("Meeting scheduled successfully!")
                print(f"    {proposed_slot.start_time.strftime('%A, %B %d at %I:%M %p')}")
                print(f"   👥 Attendees: {', '.join(meeting_request.attendees)}")
                return True
            else:
                print("Failed to create calendar event")
                return False
                
        except Exception as e:
            print(f"Error creating calendar event: {e}")
            return False
    
    def _get_user_confirmation(self, proposed_slot: TimeSlot) -> bool:
        """Get user confirmation for the proposed time slot"""
        # In a real implementation, this would prompt the user
        # For now, we'll return True to auto-confirm
        print("Auto-confirming first available slot...")
        return True
    
    def list_available_slots(self, duration_minutes: int, time_constraint: str) -> List[TimeSlot]:
        """List available time slots without scheduling"""
        print(f"🔍 Finding available slots for {duration_minutes} minutes...")
        
        try:
            available_slots = self.calendar_agent.find_available_slots(
                duration_minutes=duration_minutes,
                time_constraint=time_constraint
            )
            
            if available_slots:
                print(f"Found {len(available_slots)} available slots:")
                for i, slot in enumerate(available_slots, 1):
                    print(f"   {i}. {slot.start_time.strftime('%A, %B %d at %I:%M %p')}")
            else:
                print("No available time slots found")
            
            return available_slots
            
        except Exception as e:
            print(f"Error finding available slots: {e}")
            return []
