from datetime import date
from pandas import *
import requests
import random


RANDOMMER_API_KEY = "89a27eb105ab432bbd02f9a2bb6212ff"
RANDOMMER_URL = "https://randommer.io/api/Name"
START_DATE = date(2000, 1, 1)
END_DATE = date(2020, 1, 1)
START_ID = 10000000
END_ID = 100000000
ACCESS_GROUPS = ["GYM", "SCIENCE", "HISTORY", "GENERAL", "MATH"]


def get_names(i):
    randommer_headers = {"X-Api-Key": RANDOMMER_API_KEY}
    randommer_params = {"nameType": "fullname", "quantity": i}
    randommer_response = requests.get(
        url=RANDOMMER_URL, params=randommer_params, headers=randommer_headers
    )
    return randommer_response.json()


def get_student_ids(i):
    ids = random.sample(range(START_ID, END_ID), i)
    return ids


names = get_names(100)
name_parts = [name.split() for name in names]
first_names = [name[0] for name in name_parts]
last_names = [name[1] for name in name_parts]
student_ids = get_student_ids(100)
emails = [
    f"{first_names[i].lower()}.{last_names[i].lower()}@gmail.com"
    for i in range(len(names))
]
access_groups = [random.sample(ACCESS_GROUPS, random.randint(0, 5)) for i in range(100)]

df = DataFrame(
    {
        "firstName": first_names,
        "lastName": last_names,
        "studentId": student_ids,
        "email": emails,
        "accessGroups": access_groups,
    }
)

df.to_csv("data.csv", index=False)
