#!/usr/bin/env python
# encoding: utf-8
import json
from unittest import mock
from unittest.mock import MagicMock

from app import app, HOST_URL
from models import User, ReceiverUser, Success, ModelValidationError, ReceiverSendError

USER = User(name='test', dob='2021-01-23')
RECEIVER_USER = ReceiverUser(user=USER, comment='test comment')


@mock.patch('requests.post')
def test_sender_success(mock_requests):
    """
    Test that a success message is returned when the user payload is valid
    And the subsequent call to the receiver is successful
    """
    # mock the response object
    mock_response = MagicMock()
    # mock the response code/ separate check to our custom success message
    mock_response.status_code = 200
    mock_requests.return_value = mock_response
    # create a user payload
    # send request to the /sender api endpoint
    resp = app.test_client().post(
        '/sender',
        data=USER.json(),
        content_type='application/json',
    )
    # mock the subsequent call to the receiver
    mock_requests.assert_called_with(
        f'{HOST_URL}/receiver',
        data=ReceiverUser(
            user=USER,
            comment=f"{USER.name} is a legend"
        ).json(),
    )
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == Success(success=True).json()


@mock.patch('requests.post')
def test_sender_validation_error(mock_requests):
    """
    Test that a validation error is raised when the user payload is invalid
    """
    resp = app.test_client().post(
        '/sender',
        data='not a user'
    )
    mock_requests.assert_not_called()
    resp_data = ModelValidationError(**json.loads(resp.data))
    expected_resp = ModelValidationError(description='Expecting value: line 1 column 1 (char 0)')
    # expecting response to be default ModelValidationError with json
    # parsing exception as description
    assert resp_data.status_code == expected_resp.status_code
    assert resp_data.description == expected_resp.description
    assert resp_data.name == expected_resp.name


@mock.patch('requests.post')
def test_sender_send_receive_failure(mock_requests):
    """
    Test that a failure message is returned when the receiver returns a failure
    """
    # return a magicMock to handle the response function calls
    mock_requests.return_value = MagicMock()
    # send request to the /sender api endpoint
    resp = app.test_client().post(
        '/sender',
        data=USER.json(),
        content_type='application/json',
    )
    # mock the subsequent call to the receiver
    mock_requests.assert_called_with(
        f'{HOST_URL}/receiver',
        data=ReceiverUser(
            user=USER,
            comment=f"{USER.name} is a legend"
        ).json(),
    )
    # The main request succeeds and propagates the failed response from the receiver
    assert resp.status_code == 500
    assert resp.get_data(as_text=True) == ReceiverSendError(description='Invalid status argument').json()


def test_receiver_success():
    """
    Test that a success message is returned when the user payload is valid
    """
    # send request to the /sender api endpoint
    resp = app.test_client().post(
        '/receiver',
        data=RECEIVER_USER.json(),
        content_type='application/json',
    )
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == Success(success=True).json()


def test_receiver_failure():
    """
    Test that a failure message is returned when the user payload is invalid
    """
    # send request to the /sender api endpoint
    resp = app.test_client().post('/receiver', data='not a user')
    assert resp.status_code == 500
    assert resp.get_data(as_text=True) == ModelValidationError(
        description="Expecting value: line 1 column 1 (char 0)"
    ).json()
