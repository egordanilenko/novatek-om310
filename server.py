#!/usr/bin/env python3
import json
from flask import Flask
from om310 import Om310

app = Flask(__name__)
om310 = Om310('Thread-1', 'Om310', 0)


@app.route("/state.json", methods=['GET'])
def stat():
    return json.dumps(om310.electric, sort_keys=True, indent=4)


if __name__ == '__main__':
    om310.start()
    app.run(port=80, host='0.0.0.0', use_reloader=False, debug=False)
