import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from models.user import User


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

    def test_create_user_successfully(self):
        data = self.prepare_registration_data(self.user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        self.user.email = 'vinkotov@example.com'
        data = self.prepare_registration_data(self.user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{self.user.email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        self.user.email = 'vinkotovexample.com'
        data = self.prepare_registration_data(self.user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "Invalid email format", f"Email '{self.user.email}' is accepted"

    @pytest.mark.parametrize("user, param", user_data)
    def test_create_user_without_required_params(self, user: User, param: str):
        data = self.prepare_registration_data(user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {param}", f"Parameter '{param}' becomes unnecessary"

    @pytest.mark.parametrize("user, param", user_data_with_short_names)
    def test_create_user_with_short_name(self, user: User, param: str):
        data = self.prepare_registration_data(user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of '{param}' field is too short", f"Short {param} is accepted"

    @pytest.mark.parametrize("user, param", user_data_with_long_names)
    def test_create_user_with_long_name(self, user: User, param: str):
        data = self.prepare_registration_data(user)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of '{param}' field is too long", f"Long {param} is accepted"
