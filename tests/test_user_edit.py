import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from steps.user_steps import UserSteps


@allure.epic("Edit user data cases")
class TestUserEdit(BaseCase):
    @allure.title("Edit a created user")
    @allure.description("This test check that a created user is successfully edit")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user(self):
        email, password, user_id, first_name = UserSteps().registrate_user()

        #LOGIN

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                 headers={"x-csrf-token":token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token":token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    @allure.title("Edit a created user by an unauthorized_user")
    @allure.description("This test check that a created user cannot be edited by an unauthorized user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_unauthorized_user(self):
        #REGISTER
        email, password, user_id, first_name = UserSteps().registrate_user()

        #EDIT
        new_name = "Changed Name"

        response2 = MyRequests.put(f"/user/{user_id}",
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == f"Auth token not supplied", "Can change the user data without authorization"

    @allure.title("Edit a created user by another user")
    @allure.description("This test check that a created user cannot be edited by another user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_another_user(self):
        #REGISTER
        email, password, user_id, first_name = UserSteps().registrate_user()

        #LOGIN FIRST USER

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #REGISTER ANOTHER USER
        another_email, another_password, another_user_id, original_first_name = UserSteps().registrate_user()

        #EDIT SECOND USER
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{another_user_id}",
                                   headers={"x-csrf-token":token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        #LOGIN SECOND USER

        login_data = {
            'email': another_email,
            'password': another_password
        }
        response4 = MyRequests.post("/user/login", data=login_data)

        another_auth_sid = self.get_cookie(response4, "auth_sid")
        another_token = self.get_header(response4, "x-csrf-token")

        #GET SECOND USER INFO

        response5 = MyRequests.get(
            f"/user/{another_user_id}",
            headers={"x-csrf-token": another_token},
            cookies={"auth_sid":  another_auth_sid})

        Assertions.assert_json_value_by_name(response5, "firstName", original_first_name, "First name is changed after edit")

    @allure.title("Edit a created user with an incorrect email")
    @allure.description("This test check that a created user cannot be edited with an incorrect email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user_with_incorrect_email(self):
        #REGISTER
        email, password, user_id, first_name = UserSteps().registrate_user()

        #LOGIN

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_email = "emailemail.com"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token":token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == "Invalid email format", f"Email '{new_email}' is accepted"

    @allure.title("Edit a created user with a short first name")
    @allure.description("This test check that a created user cannot be edited with a short first name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user_with_short_first_name(self):
        #REGISTER
        email, password, user_id, first_name = UserSteps().registrate_user()

        #LOGIN

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_first_name = "a"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token":token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName":  new_first_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error",
                                             "Too short value for field firstName", "Short first name is accepted")

