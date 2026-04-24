# SSH Script Dashboard (V1.1.0)

If you work as a GNU/Linux expert, sysadmin or devops in some capacity, you might be writing some scripts at your workplace to automate some of the tasks. Many of them can be fully automated, such as with crontab or systemd timers, but there are a few which you might need to run manually when a user requests it.

SSH Script Dashboard is intended as a solution to those issues. It allows you to set up a script dashboard for yourself, and it can be deployed as a self-service portal to allow users to trigger scripts themselves. It can run scripts remotely via SSH, or locally on any OS it runs on, and supports both plaintext and HTML output of scripts. It supports OpenID Connect (OIDC) for secure single sign-on and identity and access management.

## Screenshots

Light mode, custom HTTP script output, desktop:

![Light mode, HTTP script output, desktop](https://raw.githubusercontent.com/izalac/misc-files/main/ssh-dashboard-html-light-desktop.png "Light mode, HTTP script output, desktop")

Dark mode, top output, mobile:

![Dark mode, top output, mobile](https://raw.githubusercontent.com/izalac/misc-files/main/ssh-dashboard-top-dark-mobile.png "Dark mode, top output, mobile")

Visuals can be further customized in [index.html](templates/index.html)

## Key Features in V1.1.0

*   **Secure Execution:** Migrated from legacy `os.popen` to the `subprocess` module with improved error handling and security.
*   **Application Factory:** Refactored Flask application for better modularity and testability.
*   **Enhanced UI:** Added HTMX loading indicators providing real-time "Running..." feedback for long-running scripts.
*   **Comprehensive Testing:** New automated test suite using `unittest` and `flask.test_client`.
*   **Modernized Dependencies:** Updated to Flask 3.1+ and other modern libraries for improved security and performance.
*   **Mobile Ready:** Responsive design with dark and light mode themes, optimized for screens of any size.

## Requirements and Initial Setup

SSH Script Dashboard is built using the following technology:

*   Python 3.11+
*   Flask 3.1+
*   Fabric (for remote execution)
*   HTMX & Tailwind CSS

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/izalac/ssh-script-dashboard
    cd ssh-script-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # GNU/Linux or Mac
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

### Docker Deployment

A `.dockerignore` file is provided to keep the build context small. The Docker image automatically runs unit tests during the build phase to ensure stability.

```bash
docker build -t ssh-script-dashboard .
docker run -d -p 5000:5000 ssh-script-dashboard
```

## Configuration

SSH Script Dashboard requires some configuration to run properly. Environment variables take precedence over the `config/env.json` file.

*   **Environment Variables:** [Environment setup](docs/environment.md)
*   **Security & SSH:** [Security setup](docs/security.md)
*   **Defining Scripts:** [Command setup](docs/commands.md)

## Testing

The project includes a comprehensive test suite. To run tests locally:

```bash
python -m unittest testunit.py
```

## Legal stuff

Copyright © 2023-2026 Ivan Žalac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
