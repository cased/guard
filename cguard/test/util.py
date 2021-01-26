try:
    from unittest import mock
except ImportError:
    import mock

import requests
import responses

import cguard

# HTTP Response Mock
def mock_response(
    status_code=200, content="response content", headers={}, json_data=None, **params
):
    mock_res = mock.Mock()
    mock_res.status_code = status_code
    mock_res.content = content
    mock_res.headers = headers

    if json_data:
        mock_res.json = mock.Mock(return_value=json_data)

    return mock.patch.object(
        cguard.requestor.HTTPClient, "make_request", return_value=mock_res
    )


def mock_requests(
    path, response={}, content_type="application/json", status=200, method=responses.GET
):
    """
    Mock the requests library.
    ONLY use this for testing the low-level HTTPClient itself — it should not be used
    for testing any guard API routes. Instead use mock_response().
    """
    url = "https://example.com" + path
    responses.add(method, url, json=response, status=status, content_type=content_type)
