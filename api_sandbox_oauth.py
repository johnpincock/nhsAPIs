import requests
import json

BASE_URL = "sandbox.api.service.nhs.uk"
API_KEY = "7FoT0YX9z81jZaQOxLjBYvC2AvimCOjW"
OAUTH_ENDPOINT = f"https://{BASE_URL}/oauth2/token"

url = f"https://{BASE_URL}/personal-demographics/FHIR/R4/Patient/9000000009"

headers = {"X-Request-ID": "", "apikey": API_KEY}

response = requests.request("GET", url, headers=headers, data={})

content = json.loads(response.content)

print(content["gender"])
print(content["birthDate"])
print(content["name"][0]["given"][0])
print(" \nand the rest... \n")
print(response.content)
