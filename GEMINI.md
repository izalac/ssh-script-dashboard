# SSH Script Dashboard - Project Overview

SSH Script Dashboard is a self-service web portal designed for system administrators and DevOps engineers to trigger scripts locally or remotely via SSH. It features a lightweight, flexible design with OIDC support for secure authentication and interactive output rendering.

## Core Technologies
- **Backend:** Python 3.11+, Flask 3.1.0+
- **Frontend:** Jinja2, Tailwind CSS, HTMX
- **Execution:** Fabric (SSH), `subprocess` (Local), `tmux` (Background tasks)
- **Authentication:** OpenID Connect (OIDC) via `flask-pyoidc` (Optional)

## Project Structure
- `app.py`: Flask application using a factory pattern (`create_app`) for better testability and configuration management.
- `envexecute.py`: Refactored execution logic using `subprocess` for improved security and reliability. Handles local, remote, and background scripts.
- `config/`: Configuration directory.
    - `env.json`: Environment variable overrides (loaded if not already set).
    - `commands.json`: Definition of available scripts/commands.
    - `id-remote`: SSH private key for remote execution.
- `docs/`: Detailed documentation on environment, security, and commands.
- `templates/`: HTML templates (single-page dashboard using HTMX).
- `testunit.py`: Comprehensive test suite covering web routes and execution logic.

## Building and Running

### Local Development
1. **Initialize Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```
2. **Configure:**
   - Edit `config/env.json` to set `EXECUTE_MODEL` (`local`, `remote`, etc.) and `AUTH_MODEL`.
   - Edit `config/commands.json` to add your scripts.
3. **Run:**
   ```bash
   python app.py
   ```

### Docker Deployment
```bash
docker build -t ssh-script-dashboard .
docker run -d -p 5000:5000 ssh-script-dashboard
```
*Note: The Docker build runs unit tests automatically.*

## Testing
Run the comprehensive test suite using:
```bash
python -m unittest testunit.py
```

## Key Improvements in V1.1.0
- **Security:** Replaced `os.popen`/`os.system` with `subprocess` and used `shlex.quote` for background task command construction.
- **Robustness:** Improved environment loading and error handling across the application.
- **Testability:** Refactored `app.py` to use a factory pattern, allowing for easy testing with mock configurations.
- **Dependencies:** Updated all core dependencies to modern versions to address security vulnerabilities and improve performance.
- **UI:** The dashboard continues to use HTMX for a seamless, no-reload experience.
