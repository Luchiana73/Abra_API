import json
import requests
import test_data
from utils.temp_email import generate_temporary_email, get_confirmation_link
from faker import Faker
from utils.extract_token import extract_token


class UserRegistration:
    def __init__(self):
        self.base_url = 'https://api.dev.abra-market.com/'
        self.email = None
        self.api_url = None
        self.reg_token = None

    def register_user_with_generated_email(self, password):
        """Sends a request to the site's Swagger API to create a new supplier user and
        retrieve a unique token and ID based on the generated email and provided password"""

        self.email, self.api_url = generate_temporary_email()
        headers = {'Content-Type': 'application/json'}
        data = {'email': self.email, 'password': password}
        res = requests.post(self.base_url + 'auth/sign-up/supplier', data=json.dumps(data),
                            headers=headers)

        status = res.status_code
        body = res.json()

        if status == 200:
            confirmation_link = get_confirmation_link(self.email, self.api_url)
            print(f'Confirmation link: {confirmation_link}')
            return confirmation_link, self.email, body, status
        else:
            return None, self.email, body, status

    def register_user_with_predefined_email(self, email):
        """Sends a request to the site's Swagger API to create a new supplier user and
        retrieve a unique token and ID based on the provided email and password"""

        headers = {'Content-Type': 'application/json'}
        data = {'email': email, 'password': test_data.valid_reg_password}
        res = requests.post(self.base_url + 'auth/sign-up/supplier', data=json.dumps(data),
                            headers=headers)

        status = res.status_code
        body = res.json()
        print(f"Server response when registering with an invalid email {email}: {body}")

        return email, body, status

    def confirm_email(self):
        """Sends a request to the site's Swagger API to confirm the user's email and
        retrieve the registration token from the response"""

        confirmation_link = get_confirmation_link(self.email, self.api_url)

        token = confirmation_link.split('=')[1]
        print(f"Extracted token: {token}")

        confirm_url = self.base_url + 'auth/sign-up/confirmEmail'
        params = {'token': token}
        res = requests.get(confirm_url, params=params)

        status = res.status_code
        body = res.json()

        cookies = res.headers.get('Set-Cookie')
        self.reg_token = extract_token(cookies, 'access_token_cookie')
        print(f"Token: {self.reg_token}")
        return self.reg_token, status, body

    def send_personal_info(self):
        """Sends a request to the site's Swagger API to submit the user's personal information
        using the registration token"""

        fake = Faker()
        headers = {'Content-Type': 'application/json',
                   'Cookie': f'access_token_cookie={self.reg_token}'}
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "country_id": 7,
            "phone_number": test_data.generate_turkey_phone_number()
        }

        res = requests.post(self.base_url + '/auth/sign-up/account/sendInfo', data=json.dumps(data), headers=headers)
        status = res.status_code
        body = res.json()
        print("Request Data:", data)
        return status, body

    def send_business_info(self):
        """Sends a request to the site's Swagger API to submit the user's business information, including company
        details, license number, and an image file, using the registration token"""

        fake = Faker()
        company = fake.company()
        licence = test_data.generate_licence_number()
        year = test_data.generate_year(1960)
        phone = test_data.generate_turkey_phone_number()
        description = fake.paragraph(nb_sentences=3)
        address = test_data.generate_turkish_address()
        email = test_data.generate_qa_email()

        headers = {
            'accept': 'application/json',
            'Cookie': f'access_token_cookie={self.reg_token}'
        }

        data = {
            'supplier_data_request':
                json.dumps({"license_number": licence}),
            'company_data_request':
                json.dumps({"name": company, "is_manufacturer": True, "year_established": year,
                            "employees_number_id": 1, "description": description, "address": address,
                            "business_email": email, "country_id": 7}),
            'business_sectors_request':
                json.dumps({"business_sectors": [1]}),
            'company_phone_data_request':
                json.dumps({"country_id": 7, "phone_number": phone})
        }

        with open(r'D:\Desktop\PycharmProjects\Abra_API\image.png', 'rb') as file:
            files = {'file': ('image.png', file, 'image/png')}

            res = requests.post(self.base_url + '/auth/sign-up/business/sendInfo',
                                data=data, files=files, headers=headers)

            status = res.status_code
            body = res.json()

        print("Request Data:", data)
        return status, body

    def delete_user(self):
        """Sends a request to the site's Swagger API to delete the user's account using the registration token"""

        headers = {
            'accept': 'application/json',
            'Cookie': f'access_token_cookie={self.reg_token}'
        }
        res = requests.delete(self.base_url + '/users/account/delete', headers=headers)

        status = res.status_code
        body = res.json()
        print(body)

        return status, body

    def get_country_code(self):
        headers = {'accept': 'application/json'}
        res = requests.get(self.base_url + '/common/countries', headers=headers)
        status = res.status_code
        body = res.json()
        print(body)
        return status, body

    def get_option_of_employees_number(self):
        headers = {'accept': 'application/json'}
        res = requests.get(self.base_url + '/common/employeesNumbers', headers=headers)
        status = res.status_code
        body = res.json()
        print(body)
        return status, body

# registration = UserRegistration()
# registration.register_user()
# registration.confirm_email()
# registration.send_personal_info()
# registration.send_business_info()
# registration.delete_user()
# registration.get_country_code()
# registration.get_option_of_employees_number()
