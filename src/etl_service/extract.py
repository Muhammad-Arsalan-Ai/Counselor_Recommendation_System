import os

import requests  # type: ignore
from dotenv import load_dotenv

from base_logger import logger

load_dotenv()


def get_api_data(url: str) -> dict:
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        err_msg = f"Error {response.status_code} occurred while accessing {url}"
        logger.error(err_msg)
        raise
    return response.json()


urls = {
    "appointment": "http://appointment.us-west-2.elasticbeanstalk.com/appointments",
    "councillor": "http://councelorapp-env.eba-mdmsh3sq.us-east-1.elasticbeanstalk.com/counselor",
    "patient_councillor": "http://appointment.us-west-2.elasticbeanstalk.com/patient_councillor",
    "rating": "http://ratingapp-env.eba-f5gxzjhm.us-east-1.elasticbeanstalk.com/rating",
}


if __name__ == "__main__":
    data = {key: get_api_data(val) for key, val in urls.items()}
