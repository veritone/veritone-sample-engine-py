import sys
import json

from translator import encode_morse

PAYLOAD_REQUIRED_FIELDS = ['applicationId', 'jobId', 'taskId', 'recordingId']

TEST = 'Hello Veritone Developer'


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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    with open(sys.argv[1], 'r') as payload_file:
        print(load_payload(payload_file.read()))

        print(encode_morse(TEST))
