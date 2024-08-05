drone_schema_validator = {
    "$JsonSchema": {
        "bsonType": "object",
        "required": ["_id", "name", "available", "curr_mission_id", "awaiting_missions_id"],
        "properties": {
            "_id": {"bsonType": "integer"},
            "name": {"bsonType": "string"},
            "status": {"bsonType": "string"},
            "current_mission_id": {"bsonType": "integer"},
            "possible_missions_ids": {"bsonType": "array"}
        }}}