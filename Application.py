from flask import request, redirect, Flask
import json
import random
import string
import threading
import time

from idna import valid_contextj

# Classes
class Response:
    def __init__(self, message, data=None):
        self.message = message
        if data is None:
            self.error = True
        else:
            self.data = data
            self.error = False

    def __repr__(self):
        return json.dumps({"message": self.message, "data": self.data if not self.error else ""})

class Error(Response):
    def __init__(self, message):
        super().__init__(message)

class Token:
    def __init__(self, token):
        self.token = token
        Valid_Tokens.append(self.token)
        self.internal_thread = threading.Thread(target=self.invalidate_token)
        self.internal_thread.start()

    def invalidate_token(self):
        time.sleep(160) # May have to change this, different tokens cold  have different invalidation times.
        Valid_Tokens.pop(Valid_Tokens.index(self.token))
        self.token = None
        
        del self

    def __repr__(self):
        return self.token


# Utility
Valid_Tokens = []
def generatore_random_token():
    _TT = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    _TC = Token(_TT)
    return _TC

# JSON Actions
def get_json_data():
    return json.loads(open("data.json").read())
    
def set_json_key(key, value):
    data = get_json_data()
    data[key] = value
    with open("data.json", "r+") as f:
        f.write(json.dumps(data))
        f.close()

# Flask Config
API = Flask(__name__)

# Flask Routes
@API.route("/getkey")
def get_key():
    Token = request.args.get("token")
    Key = request.args.get("key")
    if Token in Valid_Tokens:
        if Key in get_json_data():
            return Response("Success", data={
                "content": get_json_data()[Key]
            }).__repr__()
        else:
            return Error("Key not found").__repr__()
    else:
        return Error("Invalid Token").__repr__()

@API.route("/setkey")
def set_key():
    token = request.args.get("token")
    key = request.args.get("key")
    data = request.args.get("data")
    
    if token in Valid_Tokens:
        set_json_key(key, data)
        return Response("Sucess", data={
            "details": "Successfully set key: " + key + " to: " + data}
        ).__repr__()
    else:
        return Error("Invalid Token").__repr__()


@API.route('/token')
def index():
    Passphrase = request.args.get('passphrase')
    if Passphrase == "" or Passphrase is None:
        _Error = Error("Passphrase is empty")
        return _Error.__repr__()

    Data = get_json_data()
    if Data["passphrase"] == Passphrase: # may have to improve security at this point.
        _Response = Response(message="Token Generated", data={
            "token": generatore_random_token().__repr__()
        })

        Valid_Tokens.append(_Response.data["token"])
        return _Response.__repr__()
    else:
        _Error = Error("Passphrase is incorrect")
        return _Error.__repr__()


# Flask Run
if __name__ == '__main__':
    API.run(debug=True)
    