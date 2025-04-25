
![recommendation system](https://github.com/qadeerbangash/AnxietyDepressionDocRec/assets/64665560/cdb708dd-1bf7-48dc-980c-4c02d150f694)

## Project Description

The project is a recommendation system for counselors. It aims to recommend the best counselor based on the given specialization. The system utilizes data from different sources, performs data transformation, and loads the transformed data into Redis, periodically using a cronjob.

The main components of the project include:
- **ETL Service:** Extracts data from various sources, transforms it, and loads it into Redis.
- **Matching Service:** Provides the recommendation functionality by querying the transformed data in Redis.

The recommendation system uses PySpark for data processing and analysis. It leverages Redis as an in-memory data store for efficient querying and retrieval of counselor recommendations.

## Getting Started

1. Create the required .env files:
    For the ETL service, create a .env file inside the src/services/etl directory with the following contents:

        REDIS_HOST=redis-server
        REDIS_PORT=6379

2. For the matching service, create a .env file inside the src/services/matching directory with the same contents as above.
   Note: Make sure you have a Redis server running with the specified host and port.

3. Build and start the Docker containers using Docker Compose:
   docker-compose up --build

   This command will build and start the necessary containers defined in the docker-compose.yml file.


Please note that these instructions assume you have Docker and Docker Compose installed and running on your machine.
