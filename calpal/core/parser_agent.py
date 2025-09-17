"""
Parser Agent - Converts natural language to structured meeting data
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import json
import re

from .models import MeetingRequest


class ParserAgent:
    """Agent responsible for parsing natural language meeting requests"""
    
    def __init__(self, google_api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0,
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a meeting request parser. Extract the following information from natural language and return ONLY valid JSON.

Expected format:
{{
    "attendees": ["list", "of", "people", "emails", "or", "names"],
    "topic": "Meeting subject/title",
    "duration_minutes": 60,
    "time_constraint": "Time preference (e.g., 'next Thursday at 1pm', 'tomorrow morning')",
    "location": "Meeting location if mentioned (optional)",
    "description": "Additional details if provided (optional)"
}}

Rules:
- attendees: Extract all people mentioned (names or emails)
- topic: Create a clear meeting title
- duration_minutes: Convert to minutes (default 60 if not specified)
- time_constraint: Keep the original time reference
- Return ONLY the JSON, no other text"""),
            ("human", "{input}")
        ])
    
    def parse(self, natural_language: str) -> MeetingRequest:
        """Parse natural language into structured meeting request"""
        try:
            # Create the chain
            chain = self.prompt | self.llm
            
            # Get response from LLM
            response = chain.invoke({"input": natural_language})
            
            # Extract JSON from response
            json_str = self._extract_json(response.content)
            
            # Parse JSON and create MeetingRequest
            data = json.loads(json_str)
            return MeetingRequest(**data)
            
        except Exception as e:
            print(f"LLM parsing failed: {e}")
            # Fallback to simple parsing
            return self._fallback_parse(natural_language)
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from LLM response"""
        # Look for JSON in the response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group()
        else:
            # If no JSON found, try to clean up the response
            cleaned = text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            return cleaned.strip()
    
    def _fallback_parse(self, natural_language: str) -> MeetingRequest:
        """Fallback parsing when LLM parsing fails"""
        # Simple keyword extraction as fallback
        attendees = []
        topic = "Meeting"
        duration_minutes = 60  # Default 1 hour
        time_constraint = natural_language
        
        # Extract attendees (simple pattern matching)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, natural_language)
        attendees.extend(emails)
        
        # Extract names (simple heuristic)
        name_pattern = r'\b[A-Z][a-z]+\b'
        names = re.findall(name_pattern, natural_language)
        attendees.extend([name for name in names if name not in ['Meeting', 'Lunch', 'Dinner', 'Call', 'Call']])
        
        # Extract duration
        duration_pattern = r'(\d+)\s*(hour|hr|minute|min)'
        duration_match = re.search(duration_pattern, natural_language, re.IGNORECASE)
        if duration_match:
            value = int(duration_match.group(1))
            unit = duration_match.group(2).lower()
            if unit in ['hour', 'hr']:
                duration_minutes = value * 60
            else:
                duration_minutes = value
        
        return MeetingRequest(
            attendees=attendees,
            topic=topic,
            duration_minutes=duration_minutes,
            time_constraint=time_constraint
        )
