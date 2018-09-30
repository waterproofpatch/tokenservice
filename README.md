# Token Service

Allows users to generate secret tokens they may use to exchange data with other users in posession of the token.

## Installation (using virtualenv)

```bash
pip3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Start the server:

    ```bash
    python main.py
    ```

2. Get a token:

    ```python
    requests.get("http://127.0.0.1:5000/get_token").json()
    ```

3. Put some data for a token:

    ```python
    requests.post("http://127.0.0.1:5000/put", json=json.dumps({"token":"77d5e805d51b0cdc4088b1b5dde12c519241bb90e98b787023c33f63064d1774", "data":"some new data 123!"})).json()
    ```

4. Get some data for a token:

    ```python
    requests.post("http://127.0.0.1:5000/poll", json=json.dumps({"token":"77d5e805d51b0cdc4088b1b5dde12c519241bb90e98b787023c33f63064d1774"})).json()
