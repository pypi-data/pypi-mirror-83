import datetime
import requests
import jwt
from anymate.models import *
from anymate.helpers import *


class client:
    access_token: str = None
    client_id: str = None
    client_secret: str = None
    username: str = None
    password: str = None
    on_premises_mode: bool = None
    client_uri: str = None
    auth_uri: str = None

    def __init__(self, client_id, client_secret, username, password):
        self.password = password
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.set_cloud_mode()

    def set_on_premises_mode(self, client_uri, auth_uri):
        self.on_premises_mode = True

        auth_uri = auth_uri.strip()
        if auth_uri.endswith('/'):
            auth_uri = auth_uri[:-1]
        self.auth_uri = auth_uri

        client_uri = client_uri.strip()
        if client_uri.endswith('/'):
            client_uri = client_uri[:-1]
        self.client_uri = client_uri

    def set_cloud_mode(self):
        self.on_premises_mode = False
        self.client_uri = self._get_api_url()
        self.auth_uri = self._get_auth_url()

    def _get_api_url(self):
        return f'https://{self.client_id}.anymate.app'

    def _get_auth_url(self):
        return f'https://{self.client_id}.auth.anymate.app';

    def _authenticate(self):
        auth = {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'password',
                'username': self.username,
                'password': self.password}
        result = requests.post(f'{self.auth_uri}/connect/token', data=auth)
        response = AuthResponse(**result.json())
        self.access_token = response.access_token
        return response.access_token

    def _get_or_refresh_access_token(self):
        get_new_token = True
        if self.access_token:
            decoded_token = jwt.decode(self.access_token, verify=False)
            expiration_time = decoded_token['exp']
            expiration_datetime = datetime.datetime.utcfromtimestamp(expiration_time)
            diff = expiration_datetime - datetime.datetime.utcnow()
            get_new_token = diff.total_seconds() < 5 * 60

        if not get_new_token:
            return

        self.access_token = self._authenticate()
        return

    def _api_post(self, endpoint, json_payload):
        self._get_or_refresh_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-type': 'application/json'}
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'

        url = f'{self.client_uri}/{endpoint}'
        result = requests.post(url, data=json_payload, headers=headers)
        json_result = result.json()
        return json_result

    def _api_get(self, endpoint):
        self._get_or_refresh_access_token()
        headers = {'Authorization': f'Bearer {self.access_token}',
                   'Content-type': 'application/json'}
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'

        url = f'{self.client_uri}/{endpoint}'
        result = requests.get(url, headers=headers)
        json_result = result.json()
        return json_result

    def failure(self, anymate_process_failure):
        endpoint = 'apimate/Failure'
        json_payload = json.dumps(anymate_process_failure)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def finish_run(self, anymate_finish_run):
        endpoint = 'apimate/FinishRun'
        json_payload = json.dumps(anymate_finish_run)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def start_or_get_run(self, processKey):
        endpoint = f'apimate/StartOrGetRun/{processKey}'
        result = self._api_get(endpoint)
        response = AnymateRunResponse(**result)
        return response

    def ok_to_run(self, processKey):
        endpoint = f'apimate/OkToRun/{processKey}'
        result = self._api_get(endpoint)
        response = AnymateOkToRun(**result)
        return response

    def get_rules(self, processKey):
        endpoint = f'apimate/GetRules/{processKey}'
        result = self._api_get(endpoint)
        return result
        # response = get_object(result)
        # return response

    def take_next(self, processKey):
        endpoint = f'apimate/TakeNext/{processKey}'
        result = self._api_get(endpoint)
        return result
        # response = get_object(result)
        # return response

    def create_task(self, processKey, new_task):
        endpoint = f'apimate/CreateTask/{processKey}'
        json_payload = json.dumps(new_task)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def create_and_take_task(self, processKey, new_task):
        endpoint = f'apimate/CreateAndTakeTask/{processKey}'
        json_payload = json.dumps(new_task)
        result = self._api_post(endpoint, json_payload)
        return result
        # response = get_object(result)
        # return response

    def update_task(self, task):
        endpoint = f'apimate/UpdateTask'
        json_payload = json.dumps(task)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def error(self, action):
        endpoint = f'apimate/Error'
        json_payload = json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def manual(self, action):
        endpoint = f'apimate/Manual'
        json_payload = json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def retry(self, action):
        endpoint = f'apimate/Retry'
        json_payload = json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response

    def solved(self, action):
        endpoint = f'apimate/Solved'
        json_payload = json.dumps(action)
        result = self._api_post(endpoint, json_payload)
        response = AnymateResponse(**result)
        return response
