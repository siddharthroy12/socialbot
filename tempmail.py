import requests

LINK = 'https://tempmailo.com/'
GET_EMAIL_LINK = 'https://tempmailo.com/changemail'
TOKEN_NAME='.AspNetCore.Antiforgery.dXyz_uFU2og'

# to get the verification token
# document.getElementsByName("__RequestVerificationToken")[0].value

def generate_headers(token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'authority': 'tempmailo.com',
        'cookie': f'{TOKEN_NAME}={token}',
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
        self.token = None
        self.get_token()
        self.get_email_address()

    def __repr__(self):
        return f'<TempMail [{self.email}]>'

    def get_token(self):
        r = requests.get(LINK)
        self.token = r.cookies[TOKEN_NAME]

    def get_email_address(self):
        print(generate_headers(self.token))
        r = requests.get(GET_EMAIL_LINK, headers=generate_headers(self.token))
        print(r.status_code)
        self.email = r.text
        return r

    def get_mailbox(self):
        headers = generate_headers('CfDJ8Eg0UXBf4GFKnlq0xAV8GmN0PchciDeWXdp40xM10pFC3-eHhjaFfTlo35_pcSCC5PFRHCTcd5oUX3OrbgYAVS2ws4xSo2RwHjDWqXv1P534iSF_AcIR6dnsY8pu2PvNNYv6n2Ghj-8sz3K4hd9Ou4M')
        headers['content-type'] = 'application/json;charset=UTF-8'
        payload = {
            "mail": self.email
        }
        r = requests.post(LINK, headers=headers, data=payload)
        self.mails = r.json()
