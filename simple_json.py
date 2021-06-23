import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

object_json = json.loads(json_text)

second_message = object_json.get("messages")[1].get("message")

print(second_message)