#!/usr/bin/env python
# encoding: utf-8

import requests
from flask import Flask, request, abort, jsonify, make_response, json
from models import User, ModelValidationError, ReceiverUser, ReceiverSendError, Success

app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 5000
HOST_URL = f'http://{HOST}:{PORT}'


@app.route('/sender', methods=['POST'])
def sender():
    """
    Api endpoint which expects a user payload
    The user payload is being attached to a constructed ReceiverUser payload
    The initial user payload gets logged to STDOUT
    The receiver user payload gets send to the receiver and a response is being evaluated
    as successful
    """
    try:
        # validate the User model for the expected payload
        user = User(**json.loads(request.data))
        # construct message for the receiver
        receiver_user = ReceiverUser(user=user, comment=f"{user.name} is a legend")
        # logging the received payload
        app.logger.info(f"Received message successfully -> {str(user)}")
    except Exception as e:
        # return validation error message, more specific exceptions can be added
        return make_response(ModelValidationError(description=str(e)).json(), 500)
    try:
        # send data to the receiver
        resp = requests.post(f"{HOST_URL}/receiver", data=receiver_user.json())

        if resp.status_code != 200:
            # treat all status code other than 200 as unexpected
            return make_response(
                ReceiverSendError(description="Status from receiver was not Ok").json(), resp.status_code
            )
        # return success message
        return make_response(Success(success=True).json(), 200)
    except Exception as e:
        # treat every exception as api endpoint unavailable, additional status code can be added
        return make_response(ReceiverSendError(description=str(e)).json(), 500)


@app.route('/receiver', methods=['POST'])
def receiver():
    """
    Expects a receiver user payload. On successful validation
    returns status code 200 otherwise Model validation Error
    """
    try:
        # validate the expected receiver user payload
        ReceiverUser(**json.loads(request.data))
    except Exception as e:
        # return validation error message
        return make_response(ModelValidationError(description=str(e)).json(), 500)
    # requests success codes supported for 200
    return make_response(Success(success=True).json(), 200)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
