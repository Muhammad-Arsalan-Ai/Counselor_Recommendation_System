import json
import os
import unittest
from unittest.mock import Mock, patch

import requests

from src.etl_service.extract import get_api_data

urls = {
    "appointment": f"{os.getenv('BASE_URL')}/appointment",
    "councillor": f"{os.getenv('BASE_URL')}/councillor",
    "patient_councillor": f"{os.getenv('BASE_URL')}/patient_councillor",
    "rating": f"{os.getenv('BASE_URL')}/rating",
}


class TestGetApiData(unittest.TestCase):
    def test_get_api_data(self):
        # Mock the requests.get function
        requests.get = Mock()

        # Define the mock response object
        mock_response = Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.status_code = 200

        # Set the mock response for requests.get
        requests.get.return_value = mock_response

        # Call the function to be tested
        result = get_api_data(urls)

        # Assertions
        requests.get.assert_called_once_with(urls)
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, {"key": "value"})

    @patch("requests.get")
    def test_get_api_data_404_error(self, mock_request_get):
        response = requests.Response()
        response.status_code = 404
        mock_request_get.return_value = response

        with self.assertRaises(requests.exceptions.HTTPError) as context:
            get_api_data(urls)

        # Assertions
        requests.get.assert_called_once_with(urls)
        self.assertIn(
            "404 Client Error",
            str(context.exception),
        )

    @patch("requests.get")
    def test_api_all_requests_successful(self, mock_request_get):
        return_json = {
            "test_key": "test_value",
        }
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps(return_json).encode("utf-8")
        mock_request_get.return_value = response

        response_data = get_api_data(urls)

        mock_request_get.assert_called_once_with(urls)
        self.assertEqual(response_data, return_json)


if __name__ == "__main__":
    unittest.main()
