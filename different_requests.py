import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

response = requests.post(url)
print(response.text)

response2 = requests.patch(url, data = {"method": "PATCH"})
print(response2.text)

response3 = requests.get(url, params = {"method": "GET"})
print(response3.text)

method_types = ["GET", "POST", "PUT", "DELETE"]

for type in method_types:
    response = requests.get(url, params={"method": type})
    response2 = requests.post(url, data={"method": type})
    response3 = requests.put(url, data={"method": type})
    response4 = requests.delete(url, data={"method": type})
    if (type == "GET"):
        assert response.text == '{"success":"!"}', f"Для GET-запроса неуспешный результат с параметром {type}"
        assert response2.text == "Wrong method provided", f"Для POST-запроса успешный результат с параметром {type}"
        assert response3.text == "Wrong method provided", f"Для PUT-запроса успешный результат с параметром {type}"
        assert response4.text == "Wrong method provided", f"Для DELETE-запроса успешный результат с параметром {type}"
    elif(type == "POST"):
        assert response.text == "Wrong method provided", f"Для GET-запроса успешный результат с параметром {type}"
        assert response2.text == '{"success":"!"}', f"Для POST-запроса неуспешный результат с параметром {type}"
        assert response3.text == "Wrong method provided", f"Для PUT-запроса успешный результат с параметром {type}"
        assert response4.text == "Wrong method provided", f"Для DELETE-запроса успешный результат с параметром {type}"
    elif(type == "PUT"):
        assert response.text == "Wrong method provided", f"Для GET-запроса успешный результат с параметром {type}"
        assert response2.text == "Wrong method provided", f"Для POST-запроса успешный результат с параметром {type}"
        assert response3.text == '{"success":"!"}', f"Для PUT-запроса неуспешный результат с параметром {type}"
        assert response4.text == "Wrong method provided", f"Для DELETE-запроса успешный результат с параметром {type}"
    elif(type == "DELETE"):
        assert response.text == "Wrong method provided", f"Для GET-запроса успешный результат с параметром {type}"
        assert response2.text == "Wrong method provided", f"Для POST-запроса успешный результат с параметром {type}"
        assert response3.text == "Wrong method provided", f"Для PUT-запроса успешный результат с параметром {type}"
        assert response4.text == '{"success":"!"}', f"Для DELETE-запроса неуспешный результат с параметром {type}"
