from flask import request, redirect, Flask
import json

# Classes
class Response:
    def __init__(self, message, data=None):
        self.message = message
        if data is None:
            self.error = True
        else:
            self.error = False

    def __repr__(self):
        return json.dumps({"message": self.message, "data": self.data if not self.error else ""})

class Error(Response):
    def __init__(self, message):
        super().__init__(message)


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
@API.route('/token')
def index():
    Passphrase = request.args.get('passphrase')
    if Passphrase == "" or Passphrase is None:
        _Error = Error("Passphrase is empty")
        return _Error.__repr__()


# Flask Run
if __name__ == '__main__':
    API.run(debug=True)
    