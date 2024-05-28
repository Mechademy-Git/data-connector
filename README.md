# Turbomechanica Data Connector

This is the README file for the Data Connector. It provides instructions on how to run the project.

## Prerequisites

Before running the project, make sure you have the following installed:

- [Docker](https://www.docker.com)

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:Mechademy-Git/data-connector.git
    ```

2. Change to the project directory:

    ```bash
    cd data-connector
    ```

3. Create a `.env` file in the project's root directory right next to example.env and provide the required environment variables.

    ```bash
    # Celery settings
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0

    # API key for authentication
    API_KEY=<your_secure_api_key>

    # Database
    DATABASE_URL=<your_db_url>

    # Endpoint to post data
    POST_DATA_ENDPOINT=<turbomechanica_post_data_endpoint>
    POST_DATA_API_KEY=<turbomechanica_api_key>

    # Scheduler Config
    FETCH_DATA_INTERVAL=1
    BATCH_SIZE=30
    ```


4. Start the project using docker compose:

    This project support two profiles. `Request` and `Schedule` Mode.

    - To start the project in request mode:

        ```bash
        docker compose --profile request up --build
        ```
    
    - To start the project in schedule mode:

        ```bash
        docker compose --profile schedule up --build
        ```

    - To enable both:

        ```bash
        docker compose --profile request --profile schedule up --build
        ```

## Custom Implementation

### Implement [fetch_helper](./app/utils.py) function
To customize the way the fetch_data task queries data from the database, you need to implement the fetch_helper function. This function will be called by the fetch_data task to retrieve data based on the provided start_time and end_time.

#### Example Implementation
Querying data from a SQL (Relational) Database.

1. Make sure you have passed the correct value `DATABASE_URL` e.g. `postgresql+psycopg2://username:password@localhost/dbname`

2. Udpate the [SensorDataTable](./app/models.py) class as per the structure of your external data table.
    ```python
    class SensorDataTable(Base):
        __tablename__ = "sensor_data"

        id = Column(Integer, primary_key=True, index=True)
        sensor = Column(String, index=True)
        value = Column(Integer)
        timestamp = Column(DateTime)
    ```

3. Update the [fetch_helper](./app/utils.py) like so:
    ```python
    from datetime import datetime
    from typing import List
    from .models import SensorDataTable, SensorData
    from .db import get_db

    def fetch_helper(start_time: str, end_time: str) -> List[SensorData]:
        db = get_db()
        start_time_dt = datetime.fromisoformat(start_time)
        end_time_dt = datetime.fromisoformat(end_time)
        sensor_data = db.query(SensorDataTable).filter(
            SensorDataTable.timestamp >= start_time_dt,
            SensorDataTable.timestamp <= end_time_dt
        ).all()
        return sensor_data

    ```


## Note
> For more details visit: [Turbomechanica Docs](https://docs.turbomechanica.ai)
