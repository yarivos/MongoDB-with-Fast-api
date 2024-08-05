schedule_schema_validator = {
    "$JsonSchema": {
        "bsonType": "object",
        "required": ["_id", "drone_id", "mission_id", "start_time", "end_time", "status"],
        "properties": {
            "_id": {"bsonType": "integer"},
            "drone_id": {"bsonType": "integer"},
            "mission_id": {"bsonType": "integer"},
            "start_time": {"bsonType": "date"},
            "end_time": {"bsonType": "date"},
            "status": {
                "enum": ["Not Scheduled", "Scheduled", "InProgress", "Completed"],
            },
        }}}