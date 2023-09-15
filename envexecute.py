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

import fabric
import os
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


# Tries to read EXECUTE_MODEL from environment, if it doesn't succeed, it
# populates the environment with values from config/env.json
try:
    if os.environ['EXECUTE_MODEL']:
        pass
except KeyError:
    try:
        with open('config/env.json') as env_file:
            env_data = json.load(env_file)
            for env_item in env_data:
                os.environ[env_item] = env_data[env_item]
    except Exception as e:
        message=(f'Environment load error: {e}')
        logging.critical(message)
        raise Exception(message)

# remote ssh server setup, if the appropriate EXECUTE_MODEL is set
if (os.environ['EXECUTE_MODEL'] == 'remote'
        or os.environ['EXECUTE_MODEL'] == 'remote-background'):
    try:
        server = fabric.Connection(os.environ['REMOTESERVER'], port=22,
                                   user=os.environ['REMOTEUSER'],
                                   connect_kwargs={"key_filename":
                                                   os.environ['REMOTECERT']})
    except Exception as e:
        message=(f"Remote connection to "
                f"{os.environ['REMOTESERVER']} failed: {e}")
        logging.critical(message)
        raise Exception(message)


def local_execute(script):
    ''' Function that executes the argument on a local system, and returns
     its output in html form '''
    try:
        execute = os.popen(script)
        output = execute.read()
        output = output.replace('\n', '<br />')
        return output
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        exec_err = f'{exec_err} <br />'
        return exec_err


def local_execute_background(script):
    ''' Function that executes the argument on a local system in background
      using tmux '''
    try:
        script_2 = f"tmux new -d '{script}'"
        os.system(script_2)
        return "Script executed in background. <br />"
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        exec_err = f'{exec_err} <br />'
        return exec_err


def remote_execute(script):
    ''' Function that executes the argument on a remote system, and returns
      its output in html form '''
    try:
        # Remote execution
        execute = server.run(script)
        output = execute.stdout
        # reformatting newlines to html <br /> tag for html output
        output = output.replace('\n', '<br />')
        return output
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        exec_err = f'{exec_err} <br />'
        return exec_err


def remote_execute_background(script):
    ''' Function that executes the argument on a remote system in background
      using tmux '''
    try:
        script_2 = f"tmux new -d '{script}'"
        server.run(script_2)
        return "Script executed in background. <br />"
    except Exception as e:
        exec_err = f"Error in running script {script}: {e}"
        logging.error(exec_err)
        exec_err = f'{exec_err} <br />'
        return exec_err


def default_execute(script):
    ''' Function that will call the appropriate function according to the
      EXECUTE_MODEL env variable '''
    if os.environ['EXECUTE_MODEL'] == 'local':
        return local_execute(script)
    elif os.environ['EXECUTE_MODEL'] == 'local-background':
        return local_execute_background(script)
    elif os.environ['EXECUTE_MODEL'] == 'remote':
        return remote_execute(script)
    elif os.environ['EXECUTE_MODEL'] == 'remote-background':
        return remote_execute_background(script)
