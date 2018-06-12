import sys
import os
import json
import argparse
import xmltodict

from api import APIClient, get_transcript
from translator import encode_morse

PAYLOAD_REQUIRED_FIELDS = ['veritoneApiBaseUrl', 'token', 'jobId', 'taskId', 'recordingId']
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

    try:
        if isinstance(lines, dict):
            lines['#text'] = encode_morse(lines['#text'])
            transcript['tt']['body']['div']['p'] = lines
        else:
            for i,line in enumerate(lines):
                line['#text'] = encode_morse(line['#text'])
                lines[i] = line
        
        if 'head' in transcript['tt'] and 'metadata' in transcript['tt']['head']:
            del transcript['tt']['head']['metadata']

    except Exception as e:
        print('Failed to encode transcript... {}'.format(e))
        raise

    return transcript

def encode_text(text):
    lines = ''

    for line in text:
        lines += encode_morse(line)

    return lines


def run(payload_arg):
    payload_file = open(payload_arg, 'r')
    payload = load_payload(payload_file.read())
    payload_file.close()

    try:
        client = APIClient(payload['veritoneApiBaseUrl'], payload['token'])

        client.update_task(payload['jobId'], payload['taskId'], 'running')

        recording = client.get_recording(payload['recordingId'], json.dumps(['text','transcript']))

        if recording is None or not recording['assets']:
            print('Error loading asset for the recordingId: {}'.format(payload['recordingId']))
            print('Expected asset with contentType of "text/plain" or "application/ttml+xml"')
            client.update_task(payload['jobId'], payload['taskId'], 'failed')
            return False

        oldestAsset = min(recording['assets'], key=lambda asset: asset['createdDateTime'])

        transcript = get_transcript(oldestAsset['signedUri'])

        if oldestAsset['contentType'] == 'application/ttml+xml':
            print('translating transcript file...')
            transcript = encode_transcript(xmltodict.parse(transcript))

        elif oldestAsset['contentType'] == 'text/plain':
            print('translating text file...')
            transcript = encode_text(transcript)
        else:
            print('Invalid contentType found. Expected contentType of "text/plain" or "application/ttml+xml"')
            client.update_task(payload['jobId'], payload['taskId'], 'failed')
            return False

        success = client.save_transcript(payload['recordingId'], oldestAsset['assetType'], oldestAsset['contentType'], transcript)

        if not success:
            print('Failed to save transcript')
            client.update_task(payload['jobId'], payload['taskId'], 'failed')
            return False
        else:
            client.update_task(payload['jobId'], payload['taskId'], 'complete')

        return success

    except Exception as e:
        print('Failed to Successfully run engine due to {}...'.format(e))
        client.update_task(payload['jobId'], payload['taskId'], 'failed')
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Veritone Developer sample python engine - Translation Morse encoder')
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
