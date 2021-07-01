import pytest
import requests

class TestUserAgent:

    user_agent = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
         "Mobile",
         "No",
         "Android"
         ),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
         "Mobile",
         "Chrome",
         "iOS"
         ),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         "Googlebot",
         "Unknown",
         "Unknown"
         ),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
         "Mobile",
         "No",
         "iPhone"
         ),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
         "Web",
         "Chrome",
         "No"
         )
    ]

    @pytest.mark.parametrize("user_agent, platform, browser, device", user_agent)
    def test_user_agent(self, user_agent, platform, browser, device):
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent}
        )
        response_json = response.json()
        assert "user_agent" in response_json, "The response doesnt' contain user_agent field"
        assert "platform" in response_json, "The response doesnt' contain platform field"
        assert "browser" in response_json, "The response doesnt' contain browser field"
        assert "device" in response_json, "The response doesnt' contain device field"

        actual_user_agent = response_json["user_agent"]
        actual_platform = response_json["platform"]
        actual_browser = response_json["browser"]
        actual_device = response_json["device"]

        assert  actual_user_agent == user_agent, f"Actual user agent is {actual_user_agent}, but expected is {user_agent}"
        assert  actual_platform == platform, f"Actual platform is {actual_platform}, but expected is {platform}"
        assert actual_browser == browser, f"Actual browser is {actual_browser}, but expected is {browser}"
        assert actual_device == device, f"Actual devices is {actual_device}, but expected is {device}"