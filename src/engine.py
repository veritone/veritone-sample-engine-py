import sys
import os
import json
import argparse

from api import APIClient, get_transcript
from translator import encode_morse

PAYLOAD_REQUIRED_FIELDS = ['applicationId', 'jobId', 'taskId', 'recordingId']
PAYLOAD_ENV = 'PAYLOAD_FILE'


def load_payload(payload_raw):
    try:
        loaded = json.loads(payload_raw)
        for field in PAYLOAD_REQUIRED_FIELDS:
            if field not in loaded:
                return None
        return loaded
    except ValueError:
        return None


def encode_transcript(transcript):
    lines = transcript['tt']['body']['div']['p']
    if '#text' in lines:
        lines['#text'] = encode_morse(lines['#text'])
    else:
        for line in lines:
            line['#text'] = encode_morse(line['#text'])

    if 'head' in transcript['tt'] and 'metadata' in transcript['tt']['head']:
        del transcript['tt']['head']['metadata']


def run(payload_arg):
    with open(payload_arg, 'r') as payload_file:
        payload = load_payload(payload_file.read())
        client = APIClient(payload['token'])

        recording = client.get_recording(payload['recordingId'])
        if recording is None or 'transcriptAsset' not in recording:
            print('Error loading transcript asset from recording')
            client.update_task(payload['jobId'], payload['taskId'], 'failed')
            return False

        client.update_task(payload['jobId'], payload['taskId'], 'running')

        transcript_asset = recording['transcriptAsset']
        transcript = get_transcript(transcript_asset['_uri'])

        encode_transcript(transcript)
        success = client.save_transcript(payload['recordingId'], transcript)

        if not success:
            print('Failed to save transcript')
            client.update_task(payload['jobId'], payload['taskId'], 'failed')
        else:
            client.update_task(payload['jobId'], payload['taskId'], 'complete')

        return success

    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Veritone Developer sample python engine - Morse encoder')
    parser.add_argument('-payload', type=str)
    args = parser.parse_args()
    payload = vars(args).get('payload', '')
    if os.getenv(PAYLOAD_ENV) is not None:
        payload = os.getenv(PAYLOAD_ENV)

    if payload is None:
        parser.print_help()
        sys.exit(1)

    if run(payload):
        print('Successfully ran engine!')
        sys.exit(0)
    else:
        sys.exit(1)
