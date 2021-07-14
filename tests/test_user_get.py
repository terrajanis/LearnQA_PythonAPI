
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from models.user import User


class TestUserGet(BaseCase):

    data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

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

    def test_get_user_details_auth_as_another_user(self):
        #REGISTER
        self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = self.prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

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