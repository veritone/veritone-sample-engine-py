import json
import requests
import xmltodict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from http import HTTPStatus

VALID_TASK_STATUS = ['running', 'complete', 'failed']
DEFAULT_REQUEST_TIMEOUT = 5000


def get_transcript(uri):
    response = requests.get(uri, timeout=DEFAULT_REQUEST_TIMEOUT)
    if response.status_code != 200:
        return None

    return response.content.decode('utf-8')

class APIClient(object):
    def __new__(cls, baseUrl, token):
        if token is None:
            raise ValueError
        else:
            return super(APIClient, cls).__new__(cls)

    def __init__(self, baseUrl, token):
        self.base_url = baseUrl + '/v3/graphql'
        self.headers = {
            'Authorization': 'Bearer %s' % token,
        }
        transport = RequestsHTTPTransport(self.base_url, headers=self.headers,
                                          use_json=True, timeout=DEFAULT_REQUEST_TIMEOUT)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def get_recording(self, recording_id, asset_type):
        query = gql('''
            query{
              temporalDataObject(id:"%s"){
                assets(assetType:%s) {
                  records  {
                    id
                    assetType
                    contentType
                    createdDateTime
                    signedUri
                  }
                }
              }
            }
            ''' % (recording_id, asset_type))
        try:
            response = self.client.execute(query)
            return {
                'assets': response['temporalDataObject']['assets']['records']
            }
        except Exception as e:
            print('Failed to find {} for recording_id {} due to: {}'.format(asset_type, recording_id, e))
            return None

    def save_transcript(self, recording_id, assetType, contentType, transcript):
        if assetType == 'text':
            filename = 'translation.txt'
            file_content = transcript
        else:
            filename = 'translation.ttml'
            file_content = xmltodict.unparse(transcript, pretty=True)

        query = '''
            mutation {
              createAsset(
                input: {
                    containerId: "%s",
                    assetType: "%s",
                    contentType: "%s"
                }) {
                id
                signedUri
              }
            }
            ''' % (recording_id, assetType, contentType)

        data = {
            'query': query,
            'filename': filename
        }

        files = {
            'file': (filename, file_content.encode('utf-8'))
        }

        try:
            response = requests.post(self.base_url, data=data, files=files, headers=self.headers)
            return response.status_code == HTTPStatus.OK
        except Exception as e:
            print('Failed to create asset for recording: {} due to: {}'.format(recording_id, e))
            return False

    def update_task(self, job_id, task_id, status, output=None):
        if status not in VALID_TASK_STATUS:
            return False

        if output is None:
            output = {}

        query = gql('''
            mutation {
              updateTask(input: {id: "%s", jobId: "%s", status: %s, output: %s}) {
                id
                status
              }
            }
        ''' % (task_id, job_id, status, json.dumps(output)))
        try:
            self.client.execute(query)
        except Exception as e:
            print('Failed to update task {} status to {} due to: {}'.format(task_id, status, e))
            return False
