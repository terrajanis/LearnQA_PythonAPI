
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from models.user import User


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        #REGISTER
        self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = self.prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
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

    def test_edit_unauthorized_user(self):
        #REGISTER
        self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = self.prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        #EDIT
        new_name = "Changed Name"

        response2 = MyRequests.put(f"/user/{user_id}",
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == f"Auth token not supplied", "Can change the user data without authorization"

    def test_edit_another_user(self):
        #REGISTER
        self.user = User(self.prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = self.prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        #LOGIN FIRST USER

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #REGISTER ANOTHER USER
        self.user2 = User(self.prepare_email(), 'learnqa2', 'learnqa2', 'learnqa2', 'learnqa2')
        register_data2 = self.prepare_registration_data(self.user2)
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        original_first_name = register_data2['firstName']
        another_email = register_data2['email']
        another_password = register_data2['password']
        another_user_id = self.get_json_value(response2, "id")

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

    def test_edit_user_with_incorrect_email(self):
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

        #EDIT
        new_email = "emailemail.com"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token":token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == "Invalid email format", f"Email '{new_email}' is accepted"

    def test_edit_user_with_short_first_name(self):
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

        #EDIT
        new_first_name = "a"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token":token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName":  new_first_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error",
                                             "Too short value for field firstName", "Short first name is accepted")

