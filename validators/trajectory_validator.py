trajectory_schema_validator = {
    "$JsonSchema": {
        "bsonType": "object",
        "required": ["_id", "description", "type", "number_of_products", "distance"],
        "properties": {
            "_id": {"bsonType": "integer"},
            "description": {"bsonType": "string"},
            "type": {"bsonType": "string"},
            "number_of_products": {"bsonType": "integer"},
            "distance": {
                "bsonType": "integer",
                "unit": "meter"
            }
        }}}