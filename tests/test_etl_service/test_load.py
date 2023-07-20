import json
import unittest
from unittest.mock import MagicMock, Mock, patch

import redis
from redis import Redis

from src.etl_service.load import load_data_to_redis


class TestLoadDataToRedis(unittest.TestCase):
    def test_load_data_to_redis(self):
        # Mock the required dependencies
        redis_client_mock = Mock()
        specializations_dfs_mock = {
            "specialization1": {"key1": "value1"},
            "specialization2": {"key2": "value2"},
        }

        # Patch the necessary functions for mocking
        with patch(
            "src.etl_service.load.get_redis_client", return_value=redis_client_mock
        ), patch(
            "src.etl_service.transform.data_transformations",
            return_value=specializations_dfs_mock,
        ):
            # Call the function to be tested
            result = load_data_to_redis(redis_client_mock, specializations_dfs_mock)

            # Assertions
            redis_client_mock.set.assert_called()
            self.assertEqual(result, specializations_dfs_mock)

    @patch("requests.get")
    def test_load_data_to_redis_404_error(self, mock_json_dumps):
        # Create a mock Redis client that raises a ConnectionError when `set` method is called
        redis_client = MagicMock(spec=Redis)
        redis_client.set.side_effect = ConnectionError("404 Not Found")

        # Create a mock specializations_dfs dictionary
        specializations_dfs = {
            "specialization1": {"data": "value1"},
            "specialization2": {"data": "value2"},
        }

        # Patch the logger.info method to avoid actual logging during the test
        with patch("src.etl_service.base_logger.logger.info"):
            with self.assertRaises(ConnectionError) as cm:
                # Call the function under test
                load_data_to_redis(redis_client, specializations_dfs)

            # Assert the error message in the ConnectionError
            self.assertEqual(str(cm.exception), "404 Not Found")

    @patch("requests.get")
    def test_load_data_to_redis_successful(self, mock_request_get):
        redis_client = redis.Redis()
        specializations_dfs = {
            "key1": {"data1": "value1"},
            "key2": {"data2": "value2"},
        }
        load_data_to_redis(redis_client, specializations_dfs)

        for key, val in specializations_dfs.items():
            self.assertEqual(
                str(redis_client.get(key), "utf-8"), json.dumps(val, indent=2)
            )


if __name__ == "__main__":
    unittest.main()
