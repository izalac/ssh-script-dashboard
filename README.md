# SSH Script Dashboard

If you work as a GNU/Linux expert, sysadmin or devops in some capacity, you might be writing some scripts at your workplace to automate some of the tasks. Many of them can be fully automated, such as with crontab or systemd timers, but there are a few which you might need to run manually when a user requests it.

SSH Script Dashboard is intended as a solution to those issues. It allows you to set up a script dashboard for yourself, and it can be deployed as a self-service portal to allow users to trigger scripts themselves. It can run scripts remotely via SSH, or locally on any OS it runs on, and supports both plaintext and HTML output of scripts. It supports OpenID Connect (OIDC) for secure single sign-on and identity and access management. By default, it comes with a lightweight, flexible design, with dark and light mode themes, and can be easily customized. It works on screens of any size, including mobile.

Some configuration is required before you run it - either via environment variables, or via the included env.json config file. You can list your custom scripts in the provided commands.json config file. Dockerfile is also provided for container deployments, with commented-out section that allows you to inject your own CA certificate, if required.

## Requirements and initial setup

SSH Script Dashboard is built using the following technology:

* Python 3.11 (older versions might work too)
* Flask framework
* Jinja2 templates
* Tailwind CSS
* HTMX

To download SSH Script Dashboard, you need Python 3 on your system. From your terminal or command prompt, clone this repository and enter it. If it's your first time, you'll need to create a virtual environment, which you need to activate, and install the requirements in package. As an alternative to git clone, [downloadable releases](https://github.com/izalac/ssh-script-dashboard/releases) are also provided.

### GNU/Linux instructions (should also work on Mac and most OS-es)

    git clone https://github.com/izalac/ssh-script-dashboard
    cd ssh-script-dashboard
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3 -m flask run

### Windows instructions

    git clone https://github.com/izalac/ssh-script-dashboard
    cd ssh-script-dashboard
    py -m venv venv
    venv\Scripts\activate.bat
    pip3 install -r requirements.txt
    py -m flask run

When this is done, you should see the application running in your browser on http://localhost:5000/

At this point, you probably want to quit running and configure it further...

## Configuration

SSH Script Dashboard requires some configuration to run properly. You'll find the documents below:

* [Environment setup](docs/environment.md)
* [Security setup](docs/security.md)
* [Command setup](commands.md)

## Legal stuff

Copyright © 2023 Ivan Žalac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
[GNU General Public License](LICENSE) for more details.