import json
from os import getenv
from urllib.parse import urlparse

import requests
from pprint import pprint
from calendly import Calendly

access_token = getenv("PERSONAL_ACCESS_TOKEN")


def create_scheduling_link(event_type):
    p = requests.post(
        url="https://api.calendly.com/scheduling_links",
        headers={
            "authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {"max_event_count": 1, "owner": event_type, "owner_type": "EventType"}
        ),
    )
    return p.json()


def authenticate_organization(token):
    url = "https://api.calendly.com/users/me"
    r = requests.get(url=url, headers={"authorization": f"Bearer {token}"})
    request = r.json()
    return request["resource"]["current_organization"]


if __name__ == "__main__":
    cal = Calendly(access_token)

    organization = authenticate_organization(access_token)

    event_types = cal.event_types(organization=organization)

    print("--all event types--")
    pprint(event_types)
    print("\n\n")

    uuid_event_type = str(
        urlparse(event_types["collection"][1]["uri"]).path.strip("/").split("/")[-1]
    )
    get_event_type = cal.get_event_type(uuid=uuid_event_type)

    print("--single event type--")
    pprint(get_event_type)
    print("\n\n")

    event_list = cal.list_events(organization=organization)

    print("--event list--")
    pprint(event_list)
    print("\n\n")

    uuid_event = str(
        urlparse(event_list["collection"][0]["uri"]).path.strip("/").split("/")[-1]
    )
    event_details = cal.get_event_details(uuid=uuid_event)

    print("--event details--")
    pprint(event_details)
    print("\n\n")

    scheduling_link = create_scheduling_link(event_details["resource"]["event_type"])

    print("--create scheduling link--")
    pprint(scheduling_link)
    print("\n\n")

    breakpoint()
