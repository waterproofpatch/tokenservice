sudo pip3 install flask
Get a token:
    requests.get("http://127.0.0.1:5000/get_token").json()

Put some data for a token:
    requests.post("http://127.0.0.1:5000/put", json=json.dumps({"token":"77d5e805d51b0cdc4088b1b5dde12c519241bb90e98b787023c33f63064d1774", "data":"some new data123!"})).json()

Get some data for a token:
    requests.post("http://127.0.0.1:5000/poll", json=json.dumps({"token":"77d5e805d51b0cdc4088b1b5dde12c519241bb90e98b787023c33f63064d1774"})).json()


