import sys
import json

from api import APIClient, get_transcript
from translator import encode_morse

PAYLOAD_REQUIRED_FIELDS = ['applicationId', 'jobId', 'taskId', 'recordingId']


def usage():
    print('Usage: python engine.py [payload]')


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
    for line in lines:
        line['#text'] = encode_morse(line['#text'])

    if 'head' in transcript['tt'] and 'metadata' in transcript['tt']['head']:
        del transcript['tt']['head']['metadata']


def run(payload_arg):
    client = APIClient()

    with open(payload_arg, 'r') as payload_file:
        payload = load_payload(payload_file.read())
        recording = client.get_recording(payload['recordingId'])

        if 'transcriptAsset' not in recording:
            print('Error: transcriptAsset not found')
            return False

        transcript_asset = recording['transcriptAsset']
        transcript = get_transcript(transcript_asset['_uri'])

        encode_transcript(transcript)
        success = client.save_transcript(payload['recordingId'], transcript)
        print(success)
        return success

    return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    if not run(sys.argv[1]):
        sys.exit(1)
