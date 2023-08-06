# RTCCafe Signaller Python

A collection of implementations of the RTCCafe Signalling Server for various python server implementations.


# Installation

```
pip install rtc-cafe-signaller
```

# Setup

For all server implementations, simply pass your server instance into one of the supplied wrappers.

## Flask-SocketIO

```
import os

import flask
from flask_socketio import SocketIO
from rtc_cafe_signaller.wrappers import flask_socketio_wrapper

app = flask.Flask(__name__)
socketio = SocketIO(app, message_queue=os.environ.get("REDIS_URL"), engineio_logger=True)
flask_socketio_wrapper.wrap(socketio)
```
