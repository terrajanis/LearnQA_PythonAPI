import requests


class TestCheckCookie:
    def test_check_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookies = response.cookies
        expected_cookie = "hw_value"
        assert "HomeWork" in cookies, "Cookie HomeWork doesn't exist"
        actual_cookie = cookies["HomeWork"]
        assert expected_cookie == actual_cookie, f"{actual_cookie} is not equal to {expected_cookie}"
