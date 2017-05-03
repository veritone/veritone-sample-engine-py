# vda-sample-engine-py

This project demonstrates how to create an engine using Python for running on Veritone's platform.

## API Usage

All communication with Veritone should be done using the Veritone API. The engine can expect several environment variables to be set for engine access:

```
API_URL: where to find API
API_TOKEN: authorization token to use on API requests

API_USERNAME: API username
API_PASSWORD: API password

if API_TOKEN is not set, then use username/password to login to API, and get a token from the login result.
```

Please see `src/api.py` for examples on how to use these environment variables and make API calls.

## Input/Output

The engine can expect a single argument when run - the location of a payloads doc. A sample payload can be found in `test/payload.json`. The engine should then use the API to retrieve the relevant asset(s) for its task.

When completed, the engine should use the API to submit its result.

While running, the engine can call the API to report on task status. Valid statuses are: `running`, `completed`, `failed`.
