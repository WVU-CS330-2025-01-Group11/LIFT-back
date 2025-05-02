"""
-------------------------------------------
Information about Mocking
-------------------------------------------
This test class inherits all real functionality from APICLient
implements get_weather_data
tests _make_request

test_make_request tests the happy path where the request works
it creates a mock http response that looks successful status 200
makes the mock return sample (fake) json data ({"key": "value})
calls the real _make_request method
verifies we get back exactly what the mock returned
this ensures that the method is correctly handling successful api calls
"""
import pytest
from unittest.mock import patch, MagicMock
from APIClient import APIClient
import requests

# since this class can't be instantiated directly
# needs to be a concrete test version of APIClient
class TestAPIClient(APIClient):
    def get_weather_data(self, *args, **kwargs):
        return {"test": "data"}


# Test Case 1, Successful request to the api
@patch.object(requests.Session, 'get')
def test_make_request_success(mock_get):
    """
    Testts that _make_request correctly handles a successful api response
    verifies that parsed json is properly returned when request succeeds
    verifies that it properly passes through the response
    """
    # I'm mocking which I don't fully understand just yet
    # TODO Delete this comment above when we're done testing
    # Setup test client and mock response
    client = TestAPIClient()
    # configures mock response object
    mock_response = MagicMock()
    mock_response.status_code = 200 # this simulates the success status
    mock_response.json.return_value = {"key": "value"} # This mocks the JSON resopnse
    # calls method
    mock_get.return_value = mock_response
    
    # verifies results
    result = client._make_request("http://test.com")
    assert result == {"key": "value"}

# Test Case 2, Failed api request
@patch.object(requests.Session, 'get')
def test_make_request_failure(mock_get):
    """
    Tests that _make_request correctly handles request failures
    verifies that it returns nthing when the request fails
    verifies that it properly catches and handles exceptions
    """
    # Setup test clinet
    client = TestAPIClient()
    # config mock to give exception
    mock_get.side_effect = requests.exceptions.RequestException("Failed")
    # calls the method being tested
    result = client._make_request("http://test.com")
    # verifies the result
    assert result is None