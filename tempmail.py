import requests
from bs4 import BeautifulSoup

LINK = 'https://tempmailo.com/'
GET_EMAIL_LINK = 'https://tempmailo.com/changemail'
COOKIE_TOKEN_NAME = '.AspNetCore.Antiforgery.dXyz_uFU2og'


def generate_headers(cookie, token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authority': 'tempmailo.com',
        'cookie': f'{COOKIE_TOKEN_NAME}={cookie}',
        'method': 'GET',
        'path': '/changemail?_r=0.010305999329898174',
        'referer': 'https://tempmailo.com/',
        'requestverificationtoken': token,
        'scheme': 'https',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }


class TempMail(object):
    def __init__(self):
        self.email = ''
        self.mails = []
        self.cookie_token = None
        self.verification_token = None
        self.get_tokens()
        self.get_new_email_address()

    def __repr__(self):
        return f'<TempMail [{self.email}]>'

    def get_tokens(self):
        r = requests.get(LINK)
        self.cookie_token = r.cookies[COOKIE_TOKEN_NAME]
        soup = BeautifulSoup(r.content, 'html.parser')
        t = soup.find('input', {'name': '__RequestVerificationToken'})
        self.verification_token = t.get('value')

    def get_new_email_address(self):
        headers = generate_headers(self.cookie_token, self.verification_token)
        r = requests.get(GET_EMAIL_LINK, headers=headers)
        self.email = r.text

    def update_mails(self):
        headers = generate_headers(self.cookie_token, self.verification_token)
        headers['content-type'] = 'application/json;charset=UTF-8'
        payload = {
            "mail": self.email
        }
        r = requests.post(LINK, headers=headers, json=payload)
        self.mails = r.json()
