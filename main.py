import time
from faker import Faker
from instagram import Instagram
from tempmail import TempMail

DESCLAIMER_NOTE = """
Please Note that this is a research project.
I am by no means responsible for any usage of this tool.
Use on your own behalf.
I'm also not responsible if your accounts get banned
due to extensive use of this tool.
"""


def generate_user_info():
    fake = Faker()

    return {
        "name": fake.name(),
        "username": fake.user_name() + '454',
        "password": fake.password()
    }


def main():
    Faker.seed(time.time())
    print(DESCLAIMER_NOTE)
    print("---Generating mass accounts---")
    user_info = generate_user_info()
    print(f"Creating account for {user_info['username']}")

    try:
        mail = TempMail()
        user = Instagram()
        user.signup(user_info['name'],
                    mail.email,
                    user_info['username'],
                    user_info['password'])

        while (len(mail.mails) == 0):
            time.sleep(1) # Have mercy on the server
            mail.update_mails()
        code = mail.mails[0]['subject'][0:6]
        user.confirm_code(code)
        print(f"Account: {user_info['username']} {user_info['password']} created successfully")
    except Exception as e:
        print(e)
        print(f"Failed to create account for {user_info['username']}")

if __name__ == '__main__':
    main()
