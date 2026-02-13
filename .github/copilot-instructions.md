# Copilot Instructions for SSH Script Dashboard

## Project Overview

**SSH Script Dashboard** is a Flask-based web application that provides a self-service portal for executing scripts—either locally or remotely over SSH. It supports both plaintext and HTML script outputs, OpenID Connect (OIDC) authentication, and responsive UI with dark/light modes.

**Key technologies:**
- Python 3.11 + Flask 2.3
- Fabric for SSH/remote execution
- Jinja2 templates + Tailwind CSS for UI
- HTMX for interactive frontend
- Flask-pyoidc for OIDC authentication (optional)

## Build, Test & Run Commands

### Development Setup
```bash
# Windows
py -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Run Application
```bash
# Development server (port 5000)
python -m flask run

# With debug mode
$env:FLASK_ENV = 'development'; python -m flask run  # Windows
FLASK_ENV=development python -m flask run  # Linux/Mac
```

### Running Tests
```bash
# Run all unit tests
python -m unittest discover -s . -p "test*.py"

# Run single test file
python -m unittest testunit.py

# Run specific test case
python -m unittest testunit.DemoTest.test_demo
```

### Docker
```bash
docker build -t ssh-script-dashboard .
docker run -d -p 5000:5000 ssh-script-dashboard
```

## High-Level Architecture

### Core Files
- **app.py** - Flask application entry point; defines two routes:
  - `/` - Landing page showing available commands
  - `/scripts/<script>` - Executes a command and returns output
  - Routes can be decorated with `@auth.oidc_auth('oidc-provider')` for OIDC protection

- **envexecute.py** - Script execution engine; key functions:
  - `default_execute(script)` - Router function that delegates to appropriate execution method
  - `local_execute()` / `remote_execute()` - Runs scripts and captures output
  - Background variants using tmux for long-running tasks
  - Handles environment setup (loads from env.json if env vars not set)

- **config/commands.json** - JSON file defining available commands as a dictionary mapping script IDs to shell commands

- **config/env.json** - Local environment configuration (fallback if env vars not set)

- **templates/index.html** - Responsive HTML/CSS/JS UI with HTMX integration

### Execution Flow
1. User clicks a button in UI (index.html)
2. HTMX request to `/scripts/<script>` endpoint
3. app.py calls `ex.default_execute()` with the script command
4. envexecute.py determines execution mode from `EXECUTE_MODEL` env var
5. Script runs locally or remotely via SSH (Fabric), output returned as HTML

### Configuration Sources (Priority Order)
1. Environment variables (recommended for production)
2. config/env.json (fallback for development/local testing)

### Authentication Models
- **none** (default) - No authentication
- **oidc** - OpenID Connect via Flask-pyoidc; requires OIDC decorators on routes and additional env vars

## Key Conventions

### Environment Variables
Critical variables that control behavior:
- **EXECUTE_MODEL** - Controls where/how scripts run:
  - `local` - Run on local machine, show output
  - `local-background` - Run locally in tmux (no output)
  - `remote` - Run on remote server via SSH, show output
  - `remote-background` - Run on remote server in tmux
- **AUTH_MODEL** - Authentication method (`none` or `oidc`)
- **LOG_FILE** (optional) - If set, logs to file; otherwise to console

### Remote SSH Configuration
When using `remote` or `remote-background` modes, these vars must be set:
- **REMOTESERVER** - Hostname/IP of target system
- **REMOTEUSER** - SSH username
- **REMOTECERT** - Path to private SSH key

Fabric connection is initialized in envexecute.py's module-level code and stored in the `server` global variable.

### OIDC Setup
When AUTH_MODEL=oidc, add `@auth.oidc_auth('oidc-provider')` decorator to routes you want to protect. Note: Comments in app.py show where to add this.

### Output Formatting
- All script output is converted to HTML by replacing `\n` with `<br />`
- Errors are returned as formatted HTML strings with `<br />` tags

### Logging
- Uses Python's standard logging module
- Configured in envexecute.py at module load time
- Logs script execution, errors, and connection issues

### Error Handling
- Try-catch blocks in both app.py and envexecute.py
- Errors logged and returned as HTML to user
- Critical errors (config load, remote connection) raise exceptions at startup

## File Organization
```
.
├── app.py                    # Flask routes and request handlers
├── envexecute.py            # Script execution logic
├── testunit.py              # Unit tests (currently minimal)
├── requirements.txt         # Python dependencies
├── config/
│   ├── commands.json        # Available scripts (user-configurable)
│   ├── env.json             # Local env config (fallback)
│   └── id-remote*           # SSH key pair (example)
├── templates/
│   └── index.html           # Frontend UI
├── docs/
│   ├── environment.md       # Env var documentation
│   ├── security.md          # Security/SSH setup guide
│   └── commands.md          # Command configuration guide
└── Dockerfile               # Container deployment
```

## Development Notes

- **Flask Debug Mode:** When FLASK_ENV is set to 'development', Flask auto-reloads on file changes
- **SSH Keys:** Examples in config/ use key-based auth; no password auth for remote modes
- **OIDC Integration:** Flask-pyoidc is only imported if AUTH_MODEL=oidc to keep setup optional
- **HTML Output:** Output is HTML-safe but passed directly; sanitize if displaying user input
- **Commands Dict:** Access via `commands[script]` in routes; missing keys raise KeyError (caught as execution error)
- **Fabric Usage:** Fabric 3.x Connection object persists for the app lifetime; reused for all remote calls
