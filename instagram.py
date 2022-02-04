import requests
import json
from datetime import datetime

link = 'https://www.instagram.com/accounts/login/'
email_signup = 'https://www.instagram.com/accounts/emailsignup/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
signup_url = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'
sendemail_url = 'https://i.instagram.com/api/v1/accounts/send_verify_email/'
confirm_code_url = 'https://i.instagram.com/api/v1/accounts/check_confirmation_code/'
force_signup_url = 'https://www.instagram.com/accounts/web_create_ajax/'


def generate_headers(csrf_token):
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
        "x-csrftoken": csrf_token
    }


class Instagram(object):
    def __init__(self):
        self.verfied = False
        self.session_id = '' # This is when logged in
        self.username = ''
        self.name = ''
        self.password = ''
        self.device_id = ''
        self.email = ''
        self.csrf_token = ''
        self.get_device_id_and_csrf_token()

    def login(self, username, password):
        self.username = username
        self.password = password
        time = int(datetime.now().timestamp())

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_response = requests.post(login_url,
                                       data=payload,
                                       headers=generate_headers(self.csrf_token))

        json_data = json.loads(login_response.text)
        print(json_data)

        if json_data["authenticated"]:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            csrf_token = cookie_jar['csrftoken']
            session_id = cookie_jar['sessionid']

            this.session_id = session_id
            this.csrf_token = csrf_token

        else:
            raise Exception("Failed to login")

    def signup(self, name, email, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

        time = int(datetime.now().timestamp())

        payload = {
            'email': email,
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'first_name': name,
            'client_id': self.device_id,
            'seamless_login_enabled': 1,
            'opt_into_one_tap': False
        }

        response = requests.post(signup_url,
                                 data=payload,
                                 headers=generate_headers(self.csrf_token))

        if response.status_code != 200:
            raise Exception('Failed to signup, signup info may be not valid')

        self.send_confirm_email()

    def send_confirm_email(self):
        """ Send confirmation email after sending signup info"""

        payload = {
            'email': self.email,
            'device_id': self.device_id
        }

        response = requests.post(sendemail_url,
                                 data=payload,
                                 headers=generate_headers(self.csrf_token))

        json_data = json.loads(response.text)

        if "email_sent" not in json_data:
            raise Exception('Failed to send email')

    def confirm_code(self, code):
        """ After signup complete run this to verify the account """

        payload = {
            'code': code,
            'device_id': self.device_id,
            'email': self.email
        }

        cookies = {
            'csrftoken': self.csrf_token
        }

        response = requests.post(confirm_code_url,
                                 data=payload,
                                 cookies=cookies,
                                 headers=generate_headers(self.csrf_token))

        json_data = json.loads(response.text)

        if "signup_code" not in json_data:
            raise Exception('Failed to confirm code')
        else:
            self.signup_code = json_data['signup_code']

    def force_signup(self):
        payload = {
            "enc_password": f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            "email": self.email,
            "username": self.username,
            "first_name": self.name,
            "month": 9,
            "day": 4,
            "year":  1975,
            "client_id": self.client_id,
            "seamless_login_enabled": 1,
            "tos_version": "row",
            "force_sign_up_code": self.signup_code
        }

        cookies = {
            "csrf_token": self.csrf_token,
            "mid": self.device_id
        }

        response = requests.post(force_signup_url,
                                 data=payload,
                                 cookies=cookies,
                                 headers=generate_headers(self.csrf_token))
        return response

    def get_device_id_and_csrf_token(self):
        """ Get device_id and csrf_token from cookies for authentication """

        response = requests.get(link)
        self.csrf_token = response.cookies['csrftoken']
        self.device_id = response.cookies['mid']
