import pytest
import requests

import utils.schema_validation as validation


@pytest.fixture
def base_url():
    return "https://hr-challenge.dev.tapyou.com/api/test/user/"


# JSON schema
response_schema = {
    "type": "object",
    "required": ["errorCode", "isSuccess", "user"],
    "properties": {
        "errorCode": {"type": "integer", "format": "int32"},
        "errorMessage": {"type": ["string", "null"]},
        "isSuccess": {"type": "boolean"},
        "user": {
            "type": "object",
            "required": ["age", "city", "gender", "id", "name", "registrationDate"],
            "properties": {
                "age": {"type": "integer", "format": "int32"},
                "city": {"type": "string"},
                "gender": {"type": "string", "enum": ["male", "female", "magic", "McCloud"]},
                "id": {"type": "integer", "format": "int32"},
                "name": {"type": "string"},
                "registrationDate": {"type": "string", "format": "date-time"}
            }
        }
    }
}


def make_status_code_report(status_code, json_data, user_id, expected_status_code):
    report = []
    report_status = True

    # Status code
    report.append("Status code: " + str(status_code))
    if status_code == expected_status_code:
        report.append("Status code is correct")
    else:
        report.append("Status code isn't correct")
        report_status = False

    return report_status, report


def make_id_report(json_data, user_id):
    report = []
    report_status = True

    id_value = json_data.get('user', {}).get('id')
    if id_value == int(user_id):
        report.append(f"Value of 'id' - {user_id}")
    else:
        report_status = False
        report.append(f"Value of 'id' isn't {user_id}")

    return report_status, report


@pytest.mark.parametrize("user_id, expected_status_code", [
    ("10", 200),
    ("2147483647", 200),
    ("1", 200)
])
def test_correct_status_code(base_url, user_id, expected_status_code):

    # Send request
    url_get = base_url + user_id
    result = requests.get(url_get)

    report_status, report = make_status_code_report(result.status_code, result.json(), user_id, expected_status_code)

    # Checking the report
    assert report_status, report
    print(report)


@pytest.mark.parametrize("user_id, expected_status_code", [
    ("2147483648", 400),
    ("0", 400)
])
def test_invalid_id(base_url, user_id, expected_status_code):
    # Send request
    url_get = base_url + user_id
    result = requests.get(url_get)

    report_status, report = make_status_code_report(result.status_code, result.json(), user_id, expected_status_code)

    # The report
    assert report_status, report
    print(report)


@pytest.mark.parametrize("user_id, expected_status_code", [
    ("2147483646", 404),
    ("", 404)
])
def test_status_code_not_found(base_url, user_id, expected_status_code):
    # Send request
    url_get = base_url + user_id
    result = requests.get(url_get)

    report_status, report = make_status_code_report(result.status_code, result.json(), user_id, expected_status_code)

    # Checking the report
    assert report_status, report
    print(report)


@pytest.mark.parametrize("user_id", ["10", "2147483647", "1"])
def test_body_response(base_url, user_id):

    # Send request
    url_get = base_url + user_id
    result = requests.get(url_get)
    # The report
    report_status, report = validation.make_body_report(result.json(), response_schema)
    assert report_status, report
    print(report)


@pytest.mark.parametrize("user_id", ["10", "2147483647", "1"])
def test_id_response(base_url, user_id):

    # Send request
    url_get = base_url + user_id
    result = requests.get(url_get)

    # The report
    report_status, report = make_id_report(result.json(), user_id)
    assert report_status, report
    print(report)
