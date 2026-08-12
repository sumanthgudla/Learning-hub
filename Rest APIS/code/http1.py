import requests

response = requests.get("https://example.com")

print(response.status_code)
print(response.text)