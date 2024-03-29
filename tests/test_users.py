import json
import pytest
import requests
from utils.report import Report
import utils.schema_validation as validation


@pytest.fixture
def base_url():
    return "https://hr-challenge.dev.tapyou.com/api/test"


@pytest.fixture(scope="function")
def report():
    return Report()


@pytest.fixture
def id_list(base_url):
    return id_list


response_schema = {
    "type": "object",
    "required": ["errorCode", "isSuccess", "idList"],
    "properties": {
        "errorCode": {"type": "integer", "format": "int32"},
        "errorMessage": {"type": "string"},
        "isSuccess": {"type": "boolean"},
        "idList": {
            "type": "array",
            "items": {
                "type": "integer",
                "format": "int32"
            }
        }
    }
}


def make_status_code_report(status_code, gender, expected_status_code, report):

    # Status code
    report.append("Status code: " + str(status_code))
    if status_code == expected_status_code:
        report.append("Status code is correct")
    else:
        report.fail("Status code isn't correct")

    return report


def make_check_id_list_report():
    report = []
    report_status = True
    return report_status, report


def get_user_inform(base_url, id_list, gender, report):

    for user_id in id_list:
        url_get = f"{base_url}/user/{user_id}"
        result = requests.get(url_get)

        if result.status_code != 200:
            report.fail(f"User information {user_id} not received.")
            continue
        user_data = result.json().get('user')
        if not user_data:
            report.fail(f"No user information found for id {user_id}")
            continue
        user_gender = user_data.get('gender')
        if not user_gender:
            report.fail(f"Field \"gender\" not found")
            continue
        if user_gender != gender:
            report.fail(f"User with id {user_id} has unexpected gender: {user_gender}. Expected: {gender}")
            continue
        report.append(f"User with id {user_id} has expected gender: {gender}")

    return report


@pytest.mark.parametrize("gender", ["male", "female", "magic", "McCloud"])
def test_get_user_inform(base_url, gender, report):
    # Send request
    url_get = f"{base_url}/users?gender={gender}"
    result = requests.get(url_get)
    if result.status_code != 200:
        report.fail(f"Status code is {result.status_code}")
        report.check()
    # Json body to Python body

    response_body = json.loads(result.text)
    id_list = response_body.get("idList", [])
    print(id_list)

    report = get_user_inform(base_url, id_list, gender, report)
    report.check()


@pytest.mark.parametrize("gender, expected_status_code", [
    ("male", 200),
    ("female", 200),
    ("magic", 200),
    ("McCloud", 200)
                         ])
def test_status_code_id_list(base_url, gender, expected_status_code, report):

    # Send request
    url_get = f"{base_url}/users?gender={gender}"
    result = requests.get(url_get)

    # Json body to Python body

    response_body = json.loads(result.text)
    id_list = response_body.get("idList", [])

    # Checking the report
    report = make_status_code_report(result.status_code, gender, expected_status_code, report)
    # assert report, report
    # print(report)
    report.check()


def test_required_param(base_url, report):

    # Send request
    url_get = f"{base_url}/users?gender"
    result = requests.get(url_get)

    if result.status_code == 400:
        report.append("Status code is correct. Expected 400")
    else:
        report.fail(f"Status code {result.status_code} isn't correct. Expected 400")

    report.check()


@pytest.mark.parametrize("gender", ["test"])
def test_unacceptable_param(base_url, gender, report):

    # Send request
    url_get = f"{base_url}/users?gender"
    result = requests.get(url_get)

    if result.status_code == 400:
        report.append("Status code is correct. Expected 400")
    else:
        report.fail(f"Status code {result.status_code} isn't correct. Expected 400")

    report.check()


@pytest.mark.parametrize("gender", ["male", "female", "magic", "McCloud"])
def test_body_response(base_url, gender, report):
    # Send request
    url_get = f"{base_url}/users?gender={gender}"
    result = requests.get(url_get)
    # The report
    success, message = validation.make_body_report(result.json(), response_schema)
    if success:
        report.append(message)
    else:
        report.fail(message)
    report.check()

