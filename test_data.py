from datetime import datetime
import random
from faker import Faker

fake = Faker()

invalid_login_emails = ['suplier1@gmail.com', 'supplier!@gmail.com', 'supplier1gmail.com', 'supplier1@mail.com',
                        'seler1@gmail.com', 'seller1!@gmail.com', 'seller1@gmail.ru', 'seller1|gmail.com', ' ']

invalid_login_passwords = ['Password1', 'Pasword1!', 'Password12', 'password1!', 'PASSWORD1!', ' ',
                           ' Password1!', 'Password1@!', 'Password.1']

valid_reg_password = '14MIH!GG66RFk+'

invalid_reg_emails = ['', 'luchianagmail.com', 'luchiana@gmail', '@gmail.com',
                      'luchiana.sv@gm#ail.com', 'luchiana@sv@gmail.com']

invalid_reg_passwords = ['', 'Pass1*', 'PASSWORD2*', 'password3!', 'PassWord123',
                         'PassWord+!$', 'Пассворд1!']


def generate_turkey_phone_number():
    first_digit = str(random.choice(['+902', '+903', '+904', '+905']))
    return first_digit + fake.numerify('#######')


def generate_licence_number():
    return fake.numerify('### - ## - ####')


def generate_year(start_year, current_year=datetime.now().year):
    return random.randint(start_year, current_year)


def generate_turkish_address():
    fake_tr = Faker('tr_TR')
    country = "Turkey"
    full_address = f"{fake_tr.address().replace('\n', ' ')}, {country}"
    return full_address


def generate_qa_email():
    email = fake.email()
    qa_email = "qa_" + email.split('@')[0] + "@" + email.split('@')[1]
    return qa_email
