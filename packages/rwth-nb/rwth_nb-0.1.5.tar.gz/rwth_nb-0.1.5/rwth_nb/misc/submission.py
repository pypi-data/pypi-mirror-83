import requests
import json
import os
import datetime as dt

import rwth_nb.misc.notebook as notebook


class Submission:
    """Submit and retrieve submissions to RWTH JupyterHub Service"""

    def __init__(self, realm):
        self.realm = realm
        
        self.profile = os.environ.get('JUPYTERHUB_PROFILE')
        self.token = os.environ.get('JUPYTERHUB_API_TOKEN')

        self.service_url = 'http://proxy-public.jhub/services/submission'
        
        if self.token is None or self.profile is None:
            raise Exception('Submissions only work inside the RWTHjupyter cluster!')
    
    def url(self, user='me', ident=None):
        url = f'{self.service_url}/{self.profile}/{self.realm}'
        
        if user is not None:
            url += f'/{user}'
            
            if ident is not None:
                url += f'/{ident}'
                
        return url
    
    def headers(self):
        return {
            'Authorization': f'token {self.token}'
        }
    
    def _parse_get(self, response):
        payload = response.json()
        
        if 'data' in payload:
            for data in payload['data']:
                if 'submitted' in data:
                    data['submitted'] = dt.datetime.fromisoformat(data['submitted'])
                    
        return payload

    def submit(self, data):
        """Submit some arbitrary JSON payload"""

        r = requests.request('POST',
                             url=self.url(user=None),
                             data=json.dumps(data),
                             headers=self.headers())
        r.raise_for_status()
        
    def submit_notebook(self):
        """Submit the notebook as JSON"""

        nb = notebook.get_contents()
        
        self.submit(nb)

    def is_submitted(self):
        """Check if the user has already submitted something to this realm"""
        
        s = self.get()
        
        return len(s) > 0
    
    def get(self, user='me', ident=None, limit=None):
        """Get all submissions for a user"""

        params = {}
        if limit is not None:
            params['limit'] = limit
        
        r = requests.request('GET', url=self.url(user, ident),
                             headers=self.headers(),
                             params=params)
        r.raise_for_status()

        j = self._parse_get(r)
        
        return j['submissions']
    
    def fetch_notebook(self, user='me', ident=None, limit=None, subdir=None, prefix=None):
        subs = self.get(user, ident, limit)
        
        for sub in subs:            
            nb = sub.pop('data')
            
            realm = sub['realm']
            submitter = sub['submitter']
            id = sub['id']
            name, ext = os.path.splitext(nb['name'])
            
            # Add submission details as metadata to the notebook
            nb['content']['metadata']['submission'] = sub
            
            fn = f'{name}_{realm}_{submitter}-{id}{ext}'
            
            if prefix:
                fn = f'{prefix}_{fn}'

            if subdir:
                os.makedirs(subdir)
                fn = f'{subdir}/{fn}'
            
            with open(fn, 'w+') as nb_file:
                json.dump(nb['content'], nb_file)
                
    def fetch_all_notebooks(self):
        """Get all submissions in a realm"""

        return self.fetch_notebook(user=None)
    
    def delete(self, user='me', ident=None):
        """Delete the users submission"""
        
        r = requests.request('DELETE', url=self.url(user, ident),
                             headers=self.headers())
        r.raise_for_status()
        
    def get_all(self):
        """Get all submissions in a realm"""

        return self.get(user=None)
    
    def delete_all(self):
        """Delete all submissions"""
        
        return self.delete(user=None)