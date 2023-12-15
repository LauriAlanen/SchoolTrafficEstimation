""" Fetches the calendar information from the . """
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def get_calendar_cookie(php_session_id, date_from, date_to):
    """ Uses the PHP session cookie to get the calendar information from the API."""
    url = "https://lukkarit.vamk.fi/rest/basket/0/events"

    headers = {
        "cookie": f"PHPSESSID={php_session_id}",
    }

    data = {
        "dateFrom": f"{date_from}",
        "dateTo": f"{date_to}",
        "eventType": "visible"
    }

    response = requests.post(url, headers=headers, json=data, verify=False, timeout=10)
    return response
