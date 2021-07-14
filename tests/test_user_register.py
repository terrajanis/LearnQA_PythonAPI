import pytest
import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from models.user import User

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    user_data = [
        (User(None, 'learnqa', 'learnqa', 'learnqa', 'learnqa'), "email"),
        (User(BaseCase().prepare_email(), None, 'learnqa', 'learnqa', 'learnqa'), "password"),
        (User(BaseCase().prepare_email(), 'learnqa', None, 'learnqa', 'learnqa'), "username"),
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa', None, 'learnqa'), "firstName"),
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa', 'learnqa', None), "lastName")
    ]

    user_data_with_short_names = [
        (User(BaseCase().prepare_email(), 'learnqa', 'a', 'learnqa', 'learnqa'), "username"),
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa', 'a', 'learnqa'), "firstName"),
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'a'), "lastName"),
    ]

    user_data_with_long_names = [
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa'.zfill(251), 'learnqa', 'learnqa'), "username"),
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa', 'learnqa'.zfill(251), 'learnqa'), "firstName"),
        (User(BaseCase().prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa'.zfill(251)), "lastName"),
    ]

    def setup(self):
       self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')

    @allure.title("Create a user")
    @allure.description("This test check that a user is successfully created")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data(self.user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Create a user with the existing email")
    @allure.description("This test check that a user isn't created with the existing email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        self.user.email = 'vinkotov@example.com'
        data = self.prepare_registration_data(self.user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{self.user.email}' already exists", f"Unexpected response content {response.content}"

    @allure.title("Create a user with an incorrect email")
    @allure.description("This test check that a user isn't created with an incorrect email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_incorrect_email(self):
        self.user.email = 'vinkotovexample.com'
        data = self.prepare_registration_data(self.user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "Invalid email format", f"Email '{self.user.email}' is accepted"

    @allure.title("Create a user without required params")
    @allure.description("This test check that a user isn't created without required params")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user, param", user_data)
    def test_create_user_without_required_params(self, user: User, param: str):
        data = self.prepare_registration_data(user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {param}", f"Parameter '{param}' becomes unnecessary"

    @allure.title("Create a user with short names")
    @allure.description("This test check that a user isn't created with short names")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user, param", user_data_with_short_names)
    def test_create_user_with_short_name(self, user: User, param: str):
        data = self.prepare_registration_data(user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of '{param}' field is too short", f"Short {param} is accepted"

    @allure.title("Create a user with long names")
    @allure.description("This test check that a user isn't created with long names")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user, param", user_data_with_long_names)
    def test_create_user_with_long_name(self, user: User, param: str):
        data = self.prepare_registration_data(user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of '{param}' field is too long", f"Long {param} is accepted"
