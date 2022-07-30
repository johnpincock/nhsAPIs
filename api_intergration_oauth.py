import requests
import uuid
from time import time
import jwt  # https://github.com/jpadilla/pyjwt
import json

BASE_URL = "int.api.service.nhs.uk"
PRIVATE_KEY = "jwtRS512.key"
NHS_DIGITAL_SECRET = "7FoT0YX9z81jZaQOxLjBYvC2AvimCOjW"
OAUTH_ENDPOINT = f"https://{BASE_URL}/oauth2/token"


class NHSAPI:
    def __init__(self):
        self.access_token = self.get_access_token()
        self.payload = None

    def get_access_token(self):
        with open(PRIVATE_KEY, "r") as f:
            private_key = f.read()

        claims = {
            "sub": NHS_DIGITAL_SECRET,
            "iss": NHS_DIGITAL_SECRET,
            "jti": str(uuid.uuid4()),
            "aud": OAUTH_ENDPOINT,
            "exp": int(time()) + 300,  # 5mins in the future
        }

        j_payload = jwt.encode(
            claims, private_key, algorithm="RS512", headers={"kid": "test-1"}
        )
        payload = f"grant_type=client_credentials&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer&client_assertion={j_payload}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.request(
            "POST", OAUTH_ENDPOINT, headers=headers, data=payload
        )

        access_token = json.loads(response.text)["access_token"]
        return access_token

    def get_by_identifiers(self, last_name, gender, birthday):
        response = requests.request(
            "GET",
            f"https://{BASE_URL}/personal-demographics/FHIR/R4/Patient?family={last_name}&gender={gender}&birthdate=eq{birthday}",
            headers={
                "X-Request-ID": "67f5d4c9-2fe1-472d-af4a-85bceb84dda9",
                "Authorization": f"Bearer {self.access_token}",
            },
            data={},
        )
        return response.text

    def get_from_url(self, url):
        response = requests.request(
            "GET",
            url,
            headers={
                "X-Request-ID": "67f5d4c9-2fe1-472d-af4a-85bceb84dda9",
                "Authorization": f"Bearer {self.access_token}",
            },
            data={},
        )
        return response.text


if __name__ == "__main__":
    authorised_access = NHSAPI()
    results = authorised_access.get_by_identifiers("SAXTON", "male", "2010-02-04")
    print("all patient results", results)

    # get our first entry
    patient_url = json.loads(results)["entry"][0]["fullUrl"]
    patient = authorised_access.get_from_url(patient_url)
    print("patient", patient)
