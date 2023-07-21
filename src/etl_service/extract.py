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
    "appointment": f"{os.getenv('APPOINTMENTS')}",
    "councillor": f"{os.getenv('COUNCELOR')}",
    "patient_councillor": f"{os.getenv('PATIENT_COUNCILLOR')}",
    "rating": f"{os.getenv('RATING')}",
}


if __name__ == "__main__":
    data = {key: get_api_data(val) for key, val in urls.items()}
