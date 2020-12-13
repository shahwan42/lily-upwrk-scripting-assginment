import os
import pprint
import time
import csv
import requests
import sqlite3

from urllib.parse import urlparse
from dotenv import load_dotenv

# env vars
load_dotenv(override=True)


def get_emails(domain: str):
    api_url = "https://api.anymailfinder.com/v4.1/search/company.json"
    data = {"domain": domain, "company_name": ""}
    headers = {"X-Api-Key": os.getenv("API_KEY")}

    resp = requests.post(api_url, data, headers=headers)

    while resp.status_code == 202:
        print("Accepted")
        pprint.pprint(resp.json(), indent=4)
        time.sleep(2)
        resp = requests.post(api_url, data, headers=headers)

    result = []
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
            result.append(row)

    return result


def main():
    # open db connection
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    with open("sheet.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("Column names are: ")
                print(f"{', '.join(row)}")
                line_count += 1
            else:
                print("Processing: ", row)
                domain = row[0]
                relevant = row[1]

                if relevant == "yes":
                    result = get_emails(domain)
                    for el in result:
                        print("Saving: ", el)
                        # save el in db
                        cursor.execute(
                            "INSERT INTO result ('Domain','URL','Relevant?','Email') VALUES (?, ?, ?, ?)",
                            (
                                el.get("Domain"),
                                el.get("URL"),
                                el.get("Relevant?"),
                                el.get("Email"),
                            ),
                        )
                line_count += 1

    # commit changes & close db
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
