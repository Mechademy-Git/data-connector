SELECT sensor_id, value, timestamp
FROM core_sensordata
WHERE timestamp BETWEEN :start AND :end;