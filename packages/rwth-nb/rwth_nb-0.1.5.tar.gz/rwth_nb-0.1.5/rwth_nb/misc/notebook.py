import os
import requests
from IPython.lib import kernel
from notebook import notebookapp

def get_contents():
    servers = list(notebookapp.list_running_servers())
    
    token = servers[0]['token']
    api_url = servers[0]['url'] + 'api'

    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
    
    headers = {
        'Authorization': f'token {token}'
    }

    r = requests.request('GET', f'{api_url}/sessions', headers=headers)
    
    for session in r.json():
        if session['kernel']['id'] == kernel_id:
            path = session['notebook']['path']

    r = requests.request('GET', f'{api_url}/contents/{path}', headers=headers)

    return r.json()