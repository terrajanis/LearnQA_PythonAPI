import requests


class TestCheckHeader:
    def test_check_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        headers = response.headers
        expected_header = "Some secret value"
        assert "x-secret-homework-header" in headers, "Header x-secret-homework-header  doesn't exist"
        actual_header = headers["x-secret-homework-header"]
        assert expected_header == actual_header, f"{actual_header} is not equal to {expected_header}"
