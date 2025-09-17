"""
CalPal CLI - Command-line interface for the meeting scheduler
"""

import click
import os
from dotenv import load_dotenv

from .core import ParserAgent, CalendarAgent, SchedulerAgent


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """CalPal - The Smart Meeting Scheduler Agent"""
    pass


@cli.command()
@click.argument('meeting_request', type=str)
@click.option('--google-ai-key', envvar='GOOGLE_GENERATIVE_AI_API_KEY', help='Google Generative AI API key')
@click.option('--credentials-file', envvar='GOOGLE_CREDENTIALS_FILE', 
              default='credentials.json', help='Google Calendar credentials file')
@click.option('--token-file', envvar='GOOGLE_TOKEN_FILE', 
              default='token.json', help='Google Calendar token file')
@click.option('--calendar-id', envvar='DEFAULT_CALENDAR_ID', 
              default='primary', help='Google Calendar ID')
def schedule(meeting_request, google_ai_key, credentials_file, token_file, calendar_id):
    """Schedule a meeting using natural language"""
    
    # Load environment variables
    load_dotenv()
    
    # Validate required parameters
    if not google_ai_key:
        click.echo("Error: GOOGLE_GENERATIVE_AI_API_KEY is required")
        click.echo("   Set it as an environment variable or use --google-ai-key")
        return
    
    if not os.path.exists(credentials_file):
        click.echo(f"Error: Google credentials file not found: {credentials_file}")
        click.echo("   Please download your credentials.json from Google Cloud Console")
        return
    
    try:
        # Initialize agents
        click.echo("Initializing CalPal agents...")
        parser_agent = ParserAgent(google_ai_key)
        calendar_agent = CalendarAgent(credentials_file, token_file, calendar_id)
        scheduler_agent = SchedulerAgent(parser_agent, calendar_agent)
        
        # Schedule the meeting
        success = scheduler_agent.schedule_meeting(meeting_request)
        
        if success:
            click.echo("Meeting scheduled successfully!")
        else:
            click.echo("Failed to schedule meeting")
            exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}")
        exit(1)


@cli.command()
@click.argument('duration', type=int)
@click.argument('time_constraint', type=str)
@click.option('--google-ai-key', envvar='GOOGLE_GENERATIVE_AI_API_KEY', help='Google Generative AI API key')
@click.option('--credentials-file', envvar='GOOGLE_CREDENTIALS_FILE', 
              default='credentials.json', help='Google Calendar credentials file')
@click.option('--token-file', envvar='GOOGLE_TOKEN_FILE', 
              default='token.json', help='Google Calendar token file')
@click.option('--calendar-id', envvar='DEFAULT_CALENDAR_ID', 
              default='primary', help='Google Calendar ID')
def check(duration, time_constraint, google_ai_key, credentials_file, token_file, calendar_id):
    """Check available time slots without scheduling"""
    
    # Load environment variables
    load_dotenv()
    
    # Validate required parameters
    if not google_ai_key:
        click.echo("Error: GOOGLE_GENERATIVE_AI_API_KEY is required")
        return
    
    if not os.path.exists(credentials_file):
        click.echo(f"Error: Google credentials file not found: {credentials_file}")
        return
    
    try:
        # Initialize agents
        click.echo("Initializing CalPal agents...")
        parser_agent = ParserAgent(google_ai_key)
        calendar_agent = CalendarAgent(credentials_file, token_file, calendar_id)
        scheduler_agent = SchedulerAgent(parser_agent, calendar_agent)
        
        # Check available slots
        slots = scheduler_agent.list_available_slots(duration, time_constraint)
        
        if not slots:
            click.echo("No available time slots found")
            exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}")
        exit(1)


@cli.command()
def setup():
    """Setup CalPal with required credentials"""
    click.echo("🔧 CalPal Setup")
    click.echo("=" * 50)
    
    click.echo("\n1. Google Generative AI API Key:")
    click.echo("   - Get your API key from: https://makersuite.google.com/app/apikey")
    click.echo("   - Set it as an environment variable: export GOOGLE_GENERATIVE_AI_API_KEY='your-key'")
    click.echo("   - Or add it to a .env file: GOOGLE_GENERATIVE_AI_API_KEY=your-key")
    
    click.echo("\n2. Google Calendar API:")
    click.echo("   - Go to: https://console.cloud.google.com/")
    click.echo("   - Create a new project or select existing one")
    click.echo("   - Enable the Google Calendar API")
    click.echo("   - Create credentials (OAuth 2.0 Client ID)")
    click.echo("   - Download the credentials.json file")
    click.echo("   - Place it in your CalPal directory")
    
    click.echo("\n3. First Run:")
    click.echo("   - Run: calpal schedule 'Lunch with John next Thursday at 1pm'")
    click.echo("   - You'll be prompted to authenticate with Google")
    
    click.echo("\nSetup complete! You're ready to schedule meetings.")


if __name__ == '__main__':
    cli()

