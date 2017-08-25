import os
import json
import urllib.parse
import requests
import xmltodict

API_USER_ENV = "API_USERNAME"
API_PASSWD_ENV = "API_PASSWORD"
API_TOKEN = "API_TOKEN"
API_URL = "API_URL"

VALID_TASK_STATUS = ['running', 'complete', 'failed']
DEFAULT_REQUEST_TIMEOUT = 5000

def get_transcript(uri):
    response = requests.get(uri, timeout=DEFAULT_REQUEST_TIMEOUT)
    if response.status_code != 200:
        return None

    return xmltodict.parse(response.text)


class APIClient(object):
    def __new__(cls):
        username = os.getenv(API_USER_ENV)
        password = os.getenv(API_PASSWD_ENV)
        token = os.getenv(API_TOKEN)
        url = os.getenv(API_URL)
        if url is None or (token is None and (username is None or password is None)):
            raise ValueError
        else:
            return super(APIClient, cls).__new__(cls)

    def __init__(self):
        self.username = os.getenv(API_USER_ENV)
        self.password = os.getenv(API_PASSWD_ENV)
        self.token = os.getenv(API_TOKEN)
        self.url = os.getenv(API_URL)

        if self.token is None:
            self.try_login()

        self.header = {
            'Authorization': 'Bearer %s' % self.token,
        }

    def try_login(self):
        login_data = {
            'userName': self.username,
            'password': self.password,
        }
        url = urllib.parse.urljoin(self.url, 'admin/login')
        response = requests.post(url, data=login_data, timeout=DEFAULT_REQUEST_TIMEOUT)
        if response.status_code != 200:
            raise ValueError

        response_json = json.loads(response.text)
        self.token = response_json['apiToken']

    def get_recording(self, recording_id):
        url = urllib.parse.urljoin(self.url, 'recording/{}'.format(recording_id))
        response = requests.get(url, headers=self.header, timeout=DEFAULT_REQUEST_TIMEOUT)
        if response.status_code != 200:
            return None

        return json.loads(response.text)

    def save_transcript(self, recording_id, transcript):
        content = xmltodict.unparse(transcript, pretty=True)

        headers = {
            'X-Veritone-Asset-Type': 'morse',
            'Content-Type': 'application/ttml+xml',
            'Authorization': 'Bearer %s' % self.token,
        }

        url = urllib.parse.urljoin(self.url, 'recording/{}/asset'.format(recording_id))
        response = requests.post(url, headers=headers, data=content, timeout=DEFAULT_REQUEST_TIMEOUT)
        if response.status_code != 200:
            print(response.status_code)
            return False
        return True

    def update_task(self, job_id, task_id, status, output=None):
        if status not in VALID_TASK_STATUS:
            return False
        body = {
            'taskStatus': status,
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.token,
        }
        if output is not None:
            body['output'] = output
        url = urllib.parse.urljoin(self.url, 'job/{}/task/{}'.format(job_id, task_id))
        response = requests.put(url, headers=headers, data=json.dumps(body), timeout=DEFAULT_REQUEST_TIMEOUT)
        if response.status_code != 204:
            print('Failed to update task to {}'.format(status))
            print(response.text)
            print(response.status_code)
            return False

        return True
