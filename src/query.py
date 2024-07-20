import yaml
from .db import get_db
from sqlalchemy import text
import os

def construct_query(start_time, end_time) -> str:
    # Load configuration from YAML file
    query_file_path = os.path.join(os.getcwd(), 'queries', 'sample_query.sql')
    with open(query_file_path, 'r') as f:
        query = f.read()
    
    # session = get_db()
    # try:
    #     sql_statement = text(query)
    #     result = session.execute(sql_statement, {'start': start_time, 'end': end_time})
    #     rows = result.fetchall()

    #     for row in rows:
    #         print(row)
    # except Exception as e:
    #     print(f"An error occured while executing the query: {e}")

    return text(query)
