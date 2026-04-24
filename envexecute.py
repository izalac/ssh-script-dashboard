'''
    SSH Script Dashboard
    An interface for executing scripts locally, or remotely over SSH
    Copyright (C) 2023-2026 Ivan Žalac
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

import fabric
import os
import json
import logging
import subprocess
import shlex

# Tries to read EXECUTE_MODEL from environment, if it doesn't succeed, it
# populates the environment with values from config/env.json
def load_env():
    if not os.environ.get('EXECUTE_MODEL'):
        try:
            env_path = os.path.join('config', 'env.json')
            if os.path.exists(env_path):
                with open(env_path) as env_file:
                    env_data = json.load(env_file)
                    for env_item, value in env_data.items():
                        if env_item not in os.environ:
                            os.environ[env_item] = str(value)
            else:
                os.environ.setdefault('EXECUTE_MODEL', 'local')
                os.environ.setdefault('AUTH_MODEL', 'none')
        except Exception as e:
            logging.error(f'Environment load error: {e}')
            raise Exception(f'Environment load error: {e}')

load_env()

# Sets up logging
log_file = os.environ.get('LOG_FILE')
if log_file:
    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logging.info(f'App startup. Logging to {log_file} started.')
else:
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info('App startup. Logging to terminal only.')

# remote ssh server setup, if the appropriate EXECUTE_MODEL is set
_server_connection = None

def get_server_connection():
    global _server_connection
    execute_model = os.environ.get('EXECUTE_MODEL', 'local')
    if execute_model.startswith('remote') and _server_connection is None:
        try:
            _server_connection = fabric.Connection(
                os.environ['REMOTESERVER'],
                port=22,
                user=os.environ['REMOTEUSER'],
                connect_kwargs={"key_filename": os.environ['REMOTECERT']}
            )
            logging.info('Remote server connection established.')
        except Exception as e:
            message = f"Remote connection to {os.environ.get('REMOTESERVER')} failed: {e}"
            logging.critical(message)
            raise Exception(message)
    return _server_connection

def local_execute(script):
    ''' Function that executes the argument on a local system, and returns
     its output in html form '''
    try:
        # Use subprocess for better security and control
        result = subprocess.run(script, shell=True, capture_output=True, text=True, check=False)
        output = result.stdout + result.stderr
        logging.debug(f"Local execution output: {output}")
        # reformatting newlines to html <br /> tag for html output
        return output.replace('\n', '<br />')
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        return f'{exec_err} <br />'

def local_execute_background(script):
    ''' Function that executes the argument on a local system in background
      using tmux '''
    try:
        # Avoid shell injection by using shlex to quote the script
        quoted_script = shlex.quote(script)
        cmd = f"tmux new -d {quoted_script}"
        subprocess.run(cmd, shell=True, check=True)
        return "Script executed in background. <br />"
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        return f'{exec_err} <br />'

def remote_execute(script):
    ''' Function that executes the argument on a remote system, and returns
      its output in html form '''
    try:
        conn = get_server_connection()
        result = conn.run(script, hide=True)
        output = result.stdout + result.stderr
        logging.debug(f"Remote execution output: {output}")
        return output.replace('\n', '<br />')
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        return f'{exec_err} <br />'

def remote_execute_background(script):
    ''' Function that executes the argument on a remote system in background
      using tmux '''
    try:
        conn = get_server_connection()
        quoted_script = shlex.quote(script)
        conn.run(f"tmux new -d {quoted_script}", hide=True)
        return "Script executed in background. <br />"
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        return f'{exec_err} <br />'

def default_execute(script):
    ''' Function that will call the appropriate function according to the
      EXECUTE_MODEL env variable '''
    model = os.environ.get('EXECUTE_MODEL', 'local')
    logging.info(f'Running script in {model} mode...')
    
    if model == 'local':
        return local_execute(script)
    elif model == 'local-background':
        return local_execute_background(script)
    elif model == 'remote':
        return remote_execute(script)
    elif model == 'remote-background':
        return remote_execute_background(script)
    else:
        logging.warning(f'Unknown EXECUTE_MODEL {model}, falling back to local.')
        return local_execute(script)
