
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from models.user import User


class TestUserDelete(BaseCase):


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

    def test_delete_created_user(self):
        #REGISTER
        self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = self.prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

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

    def test_delete_user_by_another_user(self):
        #REGISTER
        self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = self.prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        #LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #REGISTER ANOTHER USER

        self.user2 = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data2 = self.prepare_registration_data(self.user2)
        response3 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        another_email = register_data2['email']
        another_password = register_data2['password']
        user_id = self.get_json_value(response3, "id")

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