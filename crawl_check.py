import requests

url = "http://example.com/robots.txt"
response = requests.get(url)
print(response.text)