import yaml
from .db import get_db
from sqlalchemy import text
import os
from .config import settings
import pandas as pd
import json
from typing import List, Dict, Any


def construct_query(start_time, end_time) -> str:
    # Load configuration from YAML file
    query_file_path = os.path.join(
        os.getcwd(), settings.query_folder, settings.query_name
    )
    with open(query_file_path, "r") as f:
        query = f.read()

    return text(query)


def execute_query(start_time, end_time) -> List[Dict[str, Any]]:
    sql_query = construct_query(start_time, end_time)

    with get_db() as session:
        try:
            result = session.execute(sql_query, {"start": start_time, "end": end_time})
            rows = result.fetchall()
            column_names = result.keys()
            df = pd.DataFrame(rows, columns=column_names)
            print(df.head())
            json_result = df.to_json(orient="records")
            return json.loads(json_result)
        except Exception as e:
            print(f"An error occured: {e}")
