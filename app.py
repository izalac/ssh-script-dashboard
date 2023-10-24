'''
    SSH Script Dashboard
    An interface for executing scripts locally, or remotely over SSH
    Copyright (C) 2023 Ivan Žalac
    https://github.com/izalac/ssh-script-dashboard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from flask import Flask, render_template, session
import os
import json
import envexecute as ex


app = Flask(__name__)
version='V1.0.4'


if os.environ['AUTH_MODEL'] == 'oidc':
    from flask_pyoidc.provider_configuration import ClientMetadata
    from flask_pyoidc.provider_configuration import ProviderConfiguration
    from flask_pyoidc.user_session import UserSession
    from flask_pyoidc import OIDCAuthentication
    app.config.update(OIDC_REDIRECT_URI=os.environ['LOCAL_OIDC_REDIRECT_URI'],
                      SECRET_KEY=os.environ['LOCAL_SECRET_KEY'])
    cli_meta = ClientMetadata(client_id=os.environ['OIDC_CLIENT_ID'],
                              client_secret=os.environ['OIDC_CLIENT_SECRET'])
    provider_config = ProviderConfiguration(issuer=os.environ['OIDC_ISSUER'],
                                            client_metadata=cli_meta)
    auth = OIDCAuthentication({'oidc-provider': provider_config})
    auth.init_app(app)


# Loads the configured commands
try:
    with open("config/commands.json") as command_file:
        commands = json.load(command_file)
except Exception as e:
    message=(f'Critical error in loading commands.json: {e}')
    app.logger.critical(message)
    raise Exception(message)


# Main landing page
# If using OIDC, add the following line under the @app.route line:
# @auth.oidc_auth('oidc-provider')
@app.route("/")
def index():
    return render_template('index.html', commands=commands, version=version)


# Script running endpoint
# If using OIDC, add the following line under the @app.route line:
# @auth.oidc_auth('oidc-provider')
@app.route("/scripts/<string:script>")
def run_script(script):
    try:
        name='user'
        if os.environ['AUTH_MODEL'] == 'oidc':
            user_session = UserSession(session)
            name = user_session.userinfo['name']
        app.logger.info(f'{script} triggered by {name}')
        result = ex.default_execute(commands[script])
        return result
    except Exception as e:
        message=(f'Execution error: {e}')
        app.logger.error(message)
        return (f'{message} <br />')


# Runs the app
if __name__ == "__main__":
    app.run()
