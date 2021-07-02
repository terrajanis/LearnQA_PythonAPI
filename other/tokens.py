import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

response = requests.get(url)
json_object = response.json()

token = json_object.get("token")
seconds = json_object.get("seconds")

response2 = requests.get(url, params={"token": token})
assert response2.json().get("status") == "Job is NOT ready"
assert response2.json().get("result") is None

time.sleep(seconds + 1)

response3 = requests.get(url, params={"token": token})
assert response3.json().get("status") == "Job is ready"
assert response3.json().get("result") is not None
