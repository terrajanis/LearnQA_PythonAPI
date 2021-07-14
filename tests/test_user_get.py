import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from steps.user_steps import UserSteps


@allure.epic("Get user data cases")
class TestUserGet(BaseCase):

    data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }

    @allure.title("Get user data without authorization")
    @allure.description("This test check that only username field is returned without authorization")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Get user data")
    @allure.description("This test check receiving the user data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_details_auth_as_same_user(self):

        response1 = MyRequests.post("/user/login", data=self.data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token":token},
            cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Get user data by another user")
    @allure.description("This test check that only username field is returned when another user asj for data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_details_auth_as_another_user(self):
        #REGISTER
        email, password, user_id, first_name = UserSteps().registrate_user()

        #LOGIN
        response2 = MyRequests.post("/user/login", data=self.data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #GET INFO
        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token":token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response3, "username")
        Assertions.assert_json_has_not_key(response3, "email")
        Assertions.assert_json_has_not_key(response3, "firstName")
        Assertions.assert_json_has_not_key(response3, "lastName")