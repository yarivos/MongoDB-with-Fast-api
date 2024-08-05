mission_schema_validator = {
    "$JsonSchema": {
        "bsonType": "object",
        "required": ["_id", "trajectory_id", "duration", "priority"],
        "properties": {
            "_id": {"bsonType": "integer"},
            "trajectory_id": {"bsonType": "integer"},
            "duration": {
                "bsonType": "integer",
                "minimum": 0
            },
            "priority": {
                "bsonType": "integer",
                "minimum": 0,
                "maximum": 10
            },
        }}}