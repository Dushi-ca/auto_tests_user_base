from jsonschema import validate
from jsonschema.exceptions import ValidationError


def make_body_report(json_data, response_schema):
    message = str
    report_status = True
    try:
        validate(json_data, response_schema)
        message = "There are required fields"
    except ValidationError as e:
        report_status = False
        message = f"Required fields are missing, {e.message}"

    return report_status, message
