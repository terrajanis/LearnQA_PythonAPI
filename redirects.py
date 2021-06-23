import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
redirects = response.history

redirects_number = len(redirects) - 1
last_redirect_url = redirects[redirects_number].url

print(redirects_number)
print(last_redirect_url)