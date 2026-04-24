# Copilot Instructions for SSH Script Dashboard (V1.1.0)

## Project Overview

**SSH Script Dashboard** is a Flask-based web application that provides a self-service portal for executing scripts—either locally or remotely over SSH. It supports both plaintext and HTML script outputs, OpenID Connect (OIDC) authentication, and a responsive UI with dark/light modes.

**Key technologies:**
- Python 3.11+ + Flask 3.1+
- Fabric for SSH/remote execution
- Subprocess & shlex for secure local execution and background tasks
- Jinja2 templates + Tailwind CSS for UI
- HTMX for interactive frontend with loading indicators
- Flask-pyoidc for OIDC authentication (optional)

## Build, Test & Run Commands

### Development Setup
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Application
```bash
# Direct execution (recommended)
python app.py

# Via Flask CLI
flask run
```

### Running Tests
```bash
# Run the main test suite
python -m unittest testunit.py
```

### Docker
```bash
docker build -t ssh-script-dashboard .
docker run -d -p 5000:5000 ssh-script-dashboard
```

## High-Level Architecture

### Core Files
- **app.py** - Flask application using the **Application Factory pattern** (`create_app`):
  - Configuration is managed via `app.config`.
  - Commands are loaded into `app.config['COMMANDS']`.
  - Supports configuration overrides for testing.
  - Routes:
    - `/` - Dashboard landing page.
    - `/scripts/<script>` - Executes script, returns HTML-formatted output.

- **envexecute.py** - Execution engine using `subprocess`:
  - `local_execute(script)`: Uses `subprocess.run` with `capture_output`.
  - `local_execute_background(script)`: Uses `shlex.quote` and `tmux` for backgrounding.
  - `get_server_connection()`: Lazily initializes the Fabric connection.
  - Handles environment loading from `config/env.json`.

- **config/commands.json** - Dictionary mapping script IDs to shell commands.

- **config/env.json** - Fallback environment variables.

- **templates/index.html** - HTMX-powered frontend. Uses `hx-indicator="#indicator"` and `hx-target="#output-content"`.

### Execution Flow
1. User clicks a button -> HTMX triggers `GET /scripts/<script>`.
2. UI shows `#indicator` ("Running...").
3. `app.py` calls `ex.default_execute()`.
4. `envexecute.py` runs the command using `subprocess` (local) or `fabric` (remote).
5. Output is returned as HTML (newlines replaced by `<br />`).
6. HTMX swaps output into `#output-content`.

## Key Conventions

### Environment Variables
- **EXECUTE_MODEL**: `local`, `local-background`, `remote`, `remote-background`.
- **AUTH_MODEL**: `none` or `oidc`.
- **REMOTESERVER**, **REMOTEUSER**, **REMOTECERT**: Required for remote modes.

### Security
- **ALWAYS** use `subprocess.run` instead of `os.popen`.
- **ALWAYS** use `shlex.quote` when constructing shell commands that include variables (especially for background `tmux` tasks).
- Use `check=False` for script execution to capture error output without crashing the worker.

### Testing
- Tests in `testunit.py` use `unittest.mock.patch` to isolate execution logic.
- The `app` fixture should be created using `create_app(config_overrides)`.

### HTMX Usage
- Target specific content areas (e.g., `#output-content`) instead of large containers to maintain UI state (like visibility of indicators).
- Use `hx-indicator` to provide visual feedback for network-bound operations.

## File Organization
```
.
├── app.py                    # Application Factory and routes
├── envexecute.py            # Subprocess/Fabric execution logic
├── testunit.py              # Mock-based unit tests
├── requirements.txt         # Pinned modern dependencies
├── .dockerignore           # Optimized build context
├── config/
│   ├── commands.json        # User scripts
│   ├── env.json             # Dev fallbacks
│   └── id-remote*           # SSH keys
├── templates/
│   └── index.html           # HTMX + Tailwind dashboard
└── Dockerfile               # Production-ready container
```
