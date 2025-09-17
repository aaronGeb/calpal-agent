# CalPal Development Guide

## Project Structure

```
calpal-agent/
├── calpal/                    # Main package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                 # Command-line interface
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── models.py          # Data models
│   │   ├── parser_agent.py    # Natural language parsing
│   │   ├── calendar_agent.py  # Google Calendar integration
│   │   └── scheduler_agent.py # Workflow orchestration
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── exceptions/            # Custom exceptions
│       ├── __init__.py
│       └── calpal_exceptions.py
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_calpal.py
│   └── test_parsing.py
├── examples/                  # Usage examples
│   └── basic_usage.py
├── docs/                      # Documentation
│   ├── API.md
│   └── DEVELOPMENT.md
├── config/                    # Configuration files
│   └── env.example
├── scripts/                   # Build and utility scripts
│   └── install.sh
├── requirements.txt           # Python dependencies
├── setup.py                  # Package setup
└── README.md                 # Project documentation
```

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calpal-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   cp config/env.example .env
   # Edit .env with your API keys
   ```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_parsing.py

# Run with coverage
python -m pytest tests/ --cov=calpal
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep functions small and focused

## Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes in appropriate module
3. Add tests for new functionality
4. Update documentation if needed
5. Run tests and linting
6. Submit pull request

## Architecture Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Agents are injected into the scheduler
- **Error Handling**: Custom exceptions for different error types
- **Extensibility**: Easy to add new agents or modify existing ones

