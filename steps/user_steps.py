import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from models.user import User


class UserSteps:

    @allure.step("Resgistrate a user")
    def registrate_user(self):
        self.user = User(BaseCase().prepare_email(), 'learnqa', 'learnqa', 'learnqa', 'learnqa')
        register_data = BaseCase().prepare_registration_data(self.user)
        response1 = MyRequests.post("/user/", data= register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email =  register_data['email']
        password = register_data['password']
        user_id = BaseCase().get_json_value(response1, "id")
        first_name =  register_data['firstName']
        return email, password, user_id, first_name