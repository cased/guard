import pytest
from cguard.test.util import mock_requests
from cguard.requestor import HTTPClient

import requests

import responses
from responses import GET, POST, PATCH, PUT, DELETE, HEAD


class TestHTTPClient(object):
    @responses.activate
    def test_http_client_get(self):
        mock_requests("/sessions", method=GET)

        assert (
            HTTPClient.make_request(
                "get",
                "https://example.com/sessions",
            ).status_code
            == 200
        )

    @responses.activate
    def test_http_client_post(self):
        mock_requests("/sessions", method=POST)

        assert (
            HTTPClient.make_request(
                "post", "https://example.com/sessions", data={"foo": "bar"}
            ).status_code
            == 200
        )

    @responses.activate
    def test_http_client_put(self):
        mock_requests("/sessions", method=PUT)

        assert (
            HTTPClient.make_request(
                "put", "https://example.com/sessions", data={"foo": "bar"}
            ).status_code
            == 200
        )

    @responses.activate
    def test_http_client_patch(self):
        mock_requests("/sessions", method=PATCH)

        assert (
            HTTPClient.make_request(
                "patch", "https://example.com/sessions", data={"foo": "bar"}
            ).status_code
            == 200
        )

    @responses.activate
    def test_http_client_head(self):
        mock_requests("/sessions", method=HEAD)

        assert (
            HTTPClient.make_request(
                "head",
                "https://example.com/sessions",
            ).status_code
            == 200
        )

    @responses.activate
    def test_http_client_delete(self):
        mock_requests("/sessions", method=DELETE)

        assert (
            HTTPClient.make_request(
                "delete",
                "https://example.com/sessions",
            ).status_code
            == 200
        )
