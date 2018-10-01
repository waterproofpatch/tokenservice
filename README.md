# Token Service

Allows users to generate secret tokens they may use to exchange data with other users in posession of the token.

## Installation (using virtualenv)

```bash
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Start the server:

    ```bash
    python main.py
    ```

2. Get a token:

    ```bash
    curl http://localhost:5000/get_token
    ...
    {"token":"ae74934b75b0a388bd8194aff3f565dcf2a0ca8eec980b0eddf464af55744891"}
    ```

3. Put some data for a token:

    ```bash
    curl --header "Content-Type: application/json" --data '{"token": "ae74934b75b0a388bd8194aff3f565dcf2a0ca8eec980b0eddf464af55744891", "data": "some data"}' http://localhost:5000/put
    ...
    {"did_insert":true}
    ```

4. Get some data for a token:

    ```bash
    curl --header "Content-Type: application/json" --data '{"token": "ae74934b75b0a388bd8194aff3f565dcf2a0ca8eec980b0eddf464af55744891"}' http://localhost:5000/poll
    ...
    "some data"
    ```

## Test

To run the unit tests:

```bash
pytest
```