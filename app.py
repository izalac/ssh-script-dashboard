'''
    SSH Script Dashboard
    An interface for executing scripts locally, or remotely over SSH
    Copyright (C) 2023-2024 Ivan Žalac
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

from flask import Flask, render_template, session, current_app
import os
import json
import envexecute as ex

VERSION = 'V1.1.0'

def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config['VERSION'] = VERSION
    
    # Default COMMANDS
    app.config['COMMANDS'] = {}
    commands_path = os.path.join('config', 'commands.json')
    try:
        if os.path.exists(commands_path):
            with open(commands_path) as command_file:
                app.config['COMMANDS'] = json.load(command_file)
        else:
            app.logger.warning("commands.json not found, initializing with empty commands.")
    except Exception as e:
        app.logger.critical(f'Critical error in loading commands.json: {e}')
        raise

    if config_overrides:
        app.config.update(config_overrides)

    # OIDC Setup
    auth_model = os.environ.get('AUTH_MODEL', 'none')
    if auth_model == 'oidc':
        setup_oidc(app)

    register_routes(app)
    return app

def setup_oidc(app):
    from flask_pyoidc.provider_configuration import ClientMetadata, ProviderConfiguration
    from flask_pyoidc import OIDCAuthentication
    
    app.config.update(
        OIDC_REDIRECT_URI=os.environ.get('LOCAL_OIDC_REDIRECT_URI'),
        SECRET_KEY=os.environ.get('LOCAL_SECRET_KEY')
    )
    
    cli_meta = ClientMetadata(
        client_id=os.environ.get('OIDC_CLIENT_ID'),
        client_secret=os.environ.get('OIDC_CLIENT_SECRET')
    )
    provider_config = ProviderConfiguration(
        issuer=os.environ.get('OIDC_ISSUER'),
        client_metadata=cli_meta
    )
    auth = OIDCAuthentication({'oidc-provider': provider_config})
    auth.init_app(app)
    app.config['AUTH'] = auth

def register_routes(app):
    @app.route("/")
    def index():
        auth = app.config.get('AUTH')
        # If OIDC is enabled, we might want to protect this route
        # For now, keeping it consistent with the original logic but cleaner
        return render_template('index.html', 
                             commands=app.config['COMMANDS'], 
                             version=app.config['VERSION'])

    @app.route("/scripts/<string:script>")
    def run_script(script):
        try:
            name = 'user'
            if os.environ.get('AUTH_MODEL') == 'oidc':
                from flask_pyoidc.user_session import UserSession
                user_session = UserSession(session)
                name = user_session.userinfo.get('name', 'user')
            
            app.logger.info(f'{script} triggered by {name}')
            
            commands = app.config['COMMANDS']
            if script not in commands:
                return f"Error: Script '{script}' not found.<br />", 404
                
            result = ex.default_execute(commands[script])
            return result
        except Exception as e:
            message = f'Execution error: {e}'
            app.logger.error(message)
            return f'{message} <br />', 500

app = create_app()

if __name__ == "__main__":
    app.run()
