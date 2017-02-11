import os
import json


if not os.path.exists("settings.json"):
    with open("settings.json", "w") as f:
        json.dump(
        {"webhook": "https://hooks.slack.com/your-url",
         "location": {"longitude": -0.126236,
                      "latitude": 51.500152},
         "max_distance": 1},
         f)


class Settings(object):

    def __init__(self):

        with open("settings.json", "r") as f:
            jsettings = json.load(f)
        self.webhook = jsettings["webhook"]
        self.location = jsettings["location"]
        self.max_distance = jsettings["max_distance"]
