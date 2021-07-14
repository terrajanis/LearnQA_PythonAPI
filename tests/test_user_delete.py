import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from steps.user_steps import UserSteps


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    @allure.title("Delete the user with id 2")
    @allure.description("This test check that the user with id 2 cannot be deleted")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_with_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token":token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", "Can delete user with id 2"

    @allure.title("Delete a user")
    @allure.description("This test check that a created user is successfully deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_created_user(self):
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

        #DELETE
        new_name = "Changed Name"

        response3 = MyRequests.delete(f"/user/{user_id}",
                                   headers={"x-csrf-token":token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token":token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response4, 404)

    @allure.title("Delete a user by another user")
    @allure.description("This test check that a created user cannot be deleted by another user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_by_another_user(self):
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

        #REGISTER ANOTHER USER
        another_email, another_password, user_id, first_name = UserSteps().registrate_user()

        #LOGIN SECOND USER

        login_data = {
            'email': another_email,
            'password': another_password
        }

        response4 = MyRequests.post("/user/login", data=login_data)

        another_auth_sid = self.get_cookie(response4, "auth_sid")
        another_token = self.get_header(response4, "x-csrf-token")

        #DELETE SECOND USER
        new_name = "Changed Name"

        response5 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token":token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response5, 200)

        #GET SECOND USER INFO

        response6 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token":another_token},
            cookies={"auth_sid": another_auth_sid})

        Assertions.assert_code_status(response6, 200)