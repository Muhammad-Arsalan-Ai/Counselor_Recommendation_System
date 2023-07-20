import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.matching_service.main import app


class TestCouncillors(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("src.matching_service.main.matching_councillors")
    def test_get_councillors(self, mock_matching_councillors):
        # Mock the matching_councillors function to return a sample result
        sample_result = [
            {"councillor_id": 2909, "average_value": 5},
            {"councillor_id": 8887, "average_value": 5},
        ]

        mock_matching_councillors.return_value = sample_result
        response = self.client.get("/councillors/123/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), sample_result)
        mock_matching_councillors.assert_called_once_with(123)

    @patch("src.matching_service.main.matching_councillors")
    def test_get_specific_councillors(self, mock_matching_councillors):
        sample_result = [
            {"councillor_id": 2909, "average_value": 5},
            {"councillor_id": 8887, "average_value": 5},
        ]
        mock_matching_councillors.return_value = sample_result
        response = self.client.get("/councillors/123/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), sample_result)
        mock_matching_councillors.assert_called_once_with(123, 2)


if __name__ == "__main__":
    unittest.main()
