# veritone-sample-engine-py

This project demonstrates how to create an engine using Python for running on Veritone's platform.

## API Usage

All communication with Veritone should be done using the Veritone API. The engine can expect to be passed an API token in the `payload.json` file which is provided via the `PAYLOAD_FILE` environment variable during an engine run.

Please see `src/api.py` for examples on how to make Veritone API calls.

## Input/Output

The engine can expect a `-payload` argument when run - the location of a payload file. This argument can be passed on command line or through the `PAYLOAD_FILE` environment variable. The command line argument is provided solely for convenience - when an engine is deployed to Veritone, payloads are passed using the environment variable. A sample payload can be found in `test/payload.json`. The engine should then use the API to retrieve the relevant asset(s) for its task.

When completed, the engine should use the API to submit its result.

While running, the engine can call the API to report on task status. Valid statuses are: `running`, `completed`, `failed`.

## Running Locally

### Get API Token

Please read [Get a User Session or API Token](https://veritone-developer.atlassian.net/wiki/spaces/DOC/pages/13959365/Get+a+User+Session+or+API+Token) in our documentation to get an API token to test your engine with. Once you have a token, include it in your test `payload.json` using the key `token`.

### Install Dependencies

```
make ve
```

### Run

```
PAYLOAD_FILE=test/payload.json make run
```

# License
Copyright 2017, Veritone Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
