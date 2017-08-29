import os
import json
import urllib.parse
import requests
import xmltodict

API_URL = "https://api.veritone.com/v1/"
VALID_TASK_STATUS = ['running', 'complete', 'failed']
DEFAULT_REQUEST_TIMEOUT = 5000

def get_transcript(uri):
    response = requests.get(uri, timeout=DEFAULT_REQUEST_TIMEOUT)
    if response.status_code != 200:
        return None

    return xmltodict.parse(response.text)


class APIClient(object):
    def __new__(cls, token):
        if token is None:
            raise ValueError
        else:
            return super(APIClient, cls).__new__(cls)

    def __init__(self, token):
        self.token = token
        self.url = API_URL
        self.header = {
            'Authorization': 'Bearer %s' % self.token,
        }

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
