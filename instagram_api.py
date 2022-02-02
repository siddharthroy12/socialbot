import requests
import json
from datetime import datetime

link = 'https://www.instagram.com/accounts/login/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
signup_url = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'
sendemail_url = 'https://i.instagram.com/api/v1/accounts/send_verify_email/'

# Need a method to get this
device_id = 'YfptlgAEAAF3YdL7N_0DXZMplxB_'


def send_email(email):
    response = requests.get(link)
    time = int(datetime.now().timestamp())
    csrf = response.cookies['csrftoken']

    payload = {
        'email': email,
        'device_id': device_id
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "x-csrftoken": csrf
    }

    response = requests.post(sendemail_url, data=payload, headers=header)
    json_data = json.loads(response.text)

    print(json_data)
    if json_data["email_sent"]:
        print("Email sent")
    else:
        raise Exception('Failed to send email')


def signup(email, username, firstname, password):
    response = requests.get(link)
    time = int(datetime.now().timestamp())
    csrf = response.cookies['csrftoken']

    payload = {
        'email': email,
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'first_name': firstname,
        'client_id': device_id,
        'seamless_login_enabled': 1,
        'opt_into_one_tap': False
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/emailsignup/",
        "x-csrftoken": csrf
    }

    response = requests.post(signup_url, data=payload, headers=header)

    if response.status_code != 200:
        raise Exception('Failed to signup, signup info may be not valid')

    print(json.loads(response.text))
    send_email(email)


def login(username, password):
    response = requests.get(link)
    time = int(datetime.now().timestamp())
    csrf = response.cookies['csrftoken']

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=header)
    json_data = json.loads(login_response.text)

    if json_data["authenticated"]:
        cookies = login_response.cookies
        cookie_jar = cookies.get_dict()
        csrf_token = cookie_jar['csrftoken']
        session_id = cookie_jar['sessionid']

        return {
            "csrf_token": csrf_token,
            "session_id": session_id
        }
    else:
        raise Exception("Failed to login")
