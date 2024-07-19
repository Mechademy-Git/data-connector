import yaml


def construct_query(config_path="../fetch_query.yaml"):
    # Load configuration from YAML file
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    tags = ",".join(config["tags"])
    database_name = config["database"]["name"]
    function_name = config["database"]["function"]
    tag_name_field = config["fields"]["tag_name"]
    timestamp_field = config["fields"]["timestamp"]
    value_field = config["fields"]["value"]

    # Parameterized SQL query
    query = f"""
    SELECT {tag_name_field} AS tag_name, {timestamp_field} AS timestamp, {value_field} AS value, quality AS ts_quality 
    FROM {database_name}.dbo.{function_name}(
        '{tags}', 
        GETDATE() - 1, 
        GETDATE(), 
        1, 
        ','
    ) AS {function_name}_1 
    WHERE quality = 192
    """

    return query
