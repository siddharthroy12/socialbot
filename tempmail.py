import requests

GET_EMAIL_LINK = 'https://api.internal.temp-mail.io/api/v3/email/new'
GET_MESSAGES_LINK = 'https://api.internal.temp-mail.io/api/v3/email/target/messages'


class TempMail(object):
    def __init__(self):
        self.email = ''
        self.mails = []
        self.get_new_email_address()

    def __repr__(self):
        return f'<TempMail [{self.email}]>'

    def get_new_email_address(self):
        r = requests.post(GET_EMAIL_LINK)
        json_data = r.json()

        if "email" in json_data:
            self.email = json_data['email']
        else:
            raise Exception('Failed to get email')

    def update_mails(self):
        r = requests.get(GET_MESSAGES_LINK.replace('target', self.email))
        self.mails = r.json()
