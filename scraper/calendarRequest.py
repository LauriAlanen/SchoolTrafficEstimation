import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_calendar_cookie(php_session_id):
    url = "https://lukkarit.vamk.fi/rest/basket/0/events"

    headers = {
        "cookie": f"PHPSESSID={php_session_id}",
    }

    data = {
        "dateFrom": "2023-12-02",
        "dateTo": "2023-12-11",
        "eventType": "visible"
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    return response 