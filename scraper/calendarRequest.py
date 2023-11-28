import requests

def get_calendar_with_cookie(php_session_id):
    url = "https://lukkarit.vamk.fi/rest/basket/0/events"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"PHPSESSID={php_session_id}",
        "Referer": "https://lukkarit.vamk.fi/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    data = {
        "dateFrom": "2023-11-27",
        "dateTo": "2023-12-04",
        "eventType": "visible"
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    return response