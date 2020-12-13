import os
import pprint
import time
import requests

from urllib.parse import urlparse
from dotenv import load_dotenv

# env vars
load_dotenv(override=True)


def main():
    api_url = "https://api.anymailfinder.com/v4.1/search/company.json"

    # domain = "https://xpay.app/"
    domain = "https://egypt-shops.github.io/xshop-docs/"
    data = {"domain": domain, "company_name": ""}
    headers = {"X-Api-Key": os.getenv("API_KEY")}

    resp = requests.post(api_url, data, headers=headers)

    while resp.status_code == 202:
        print("Accepted")
        pprint.pprint(resp.json(), indent=4)
        time.sleep(2)
        resp = requests.post(api_url, data, headers=headers)

    if resp.status_code == 200:
        print("Found")
        emails = resp.json().get("emails")

        pprint.pprint(resp.json(), indent=4)
        for email in emails:
            row = {
                "Domain": urlparse(domain).netloc,
                "URL": domain,
                "Relevant?": "yes",
                "Email": email,
            }
            pprint.pprint(row, indent=4)


if __name__ == "__main__":
    main()
