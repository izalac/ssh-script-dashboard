# Environment setup for SSH Script Dashboard

SSH Script Dashboard depends on several environmental variables. For [security reasons](security.md), the best practice is if these are actually set up as environment variables. There are secure ways to inject this in many environments, such as a password vault, or kubernetes secrets.

App checks if **EXECUTE_MODEL** variable is set in the environment, if it's not, it injects default environment variables from env.json. These can also be modified, if you wish to run them locally.

## You must have these variables

* **EXECUTE_MODEL** determines how you run your scripts. It can be one of the following values:
    * *local* is default, the app will run scripts on local system and display their output. Best option for quick scripts.
    * *local-background* will run scripts on local system, but in a tmux detached session. Requires tmux to be installed. Output will not be displayed. Best option for long-running scripts.
    * *remote* runs scripts on a remote system over SSH and display their output. Best option for quick scripts.
    * *remote-background* will run scripts on a remote system over SSH, but in a tmux detached session. Requires tmux to be installed. Output will not be displayed. Best option for long-running scripts.
* **AUTH_MODEL** sets up your authentication model:
    * *none* is default, but any other value not otherwise defined will function the same. No authentication or authorization, unless you set it up elsewhere.
    * *oidc* sets up OIDC authentication. This will require having a SSO system that supports OIDC, setting up some additional variables, possibly adding custom CA certificates, as well as adding a line of code in app.py under every route you wish to secure. More details on the latest part is in comments in app.py

## Remote server configuration

If your **EXECUTE_MODEL** is *remote* or *remote-background*, you **must** have these variables set up to connect to remote server via ssh:

* **REMOTESERVER** - a hostname or IP address of a target system you're connecting to
* **REMOTEUSER** - username you're connecting as
* **REMOTECERT** - path to the private key of a SSH certificate

Info on how to create SSH certificates is in the [security document](security.md)

## OIDC configuration

These variables are required if your **AUTH_MODEL** is *oidc*.

* **LOCAL_OIDC_REDIRECT_URI** - redirect URI which you send to OIDC server, the default of http://localhost:5000/redirect_uri should be fine for testing, but make sure to use the hostname and port on which this app will be available, and change to https once you set it up.
* **LOCAL_SECRET_KEY** - your local secret key that will sign your session. You can change it to any random string, you should not use the default provided value. You can use the following one-liner to randomly generate a new one:

        python -c "import secrets; print(secrets.token_urlsafe())"

* **OIDC_ISSUER** - base OIDC URI. The other endpoints required for OIDC will be autodiscovered from it.
* **OIDC_CLIENT_ID** - the id of your OIDC client
* **OIDC_CLIENT_SECRET** - secret value of your OIDC client; client authentication/confidential access must be set up, this is the only OIDC client configuration that will work


## Logging

* **LOG_FILE** - enter the filename for log file. This parameter is optional - if it's not present, all logging will be done in console output instead of saved into a file.

[Back to Readme](../README.md)