import urllib2
import json
import os


from settings import Settings
from trafficfeed import TrafficFeed

settings = Settings()


class Bot(object):

    def __init__(self):
        #If the seen_items file doesn't exist, lets create it!
        writepath = "seen_items"
        if not os.path.exists(writepath):
            with open(writepath, "w") as f:
                pass


    def run(self):
        """Run the traffic bot
        """
        #Intiate the TrafficFeed object
        traffic = TrafficFeed(
            "http://m.highways.gov.uk/feeds/rss/UnplannedEvents.xml"
                             )

        #Load the traffic items from the feed
        items = traffic.items_within(settings.max_distance,
                                     settings.longitute,
                                     settings.latitude)
        #Get the items we have already seen
        seen = self.check_seen()

        for item in items:
            if item.find("guid").text not in seen:
                #If we haven't seen this item, push to the slack webhook
                self.post_slack(item.find("title").text,
                                item.find("link").text,
                                item.find("description").text,
                                item.find("longitude").text,
                                item.find("latitude").text)
                #The update the seen items
                self.update_seen(item.find("guid").text)
            else:
                pass


    def post_slack(self, title=None, link=None, text=None,
                    longitude=None, latitude=None):
        """Push some JSON to the webhook

        Args:
            title (str): The title of the message.
            link (str): The link the title should go to.
            text (str): The body of the message.
            longitude (str): The longitute for the image.
            latitude (str): The latitude for the image.

        Returns:
            http response: The response of the webhook.
        """
        data = {
                "text": "New traffic item",
                "attachments": [
                    {
                    "title": title if title else "",
                    "title_link": link if link else "",
                    "text": text if text else "",
                    "image_url": (
                        "http://static-maps.yandex.ru/"
                        "1.x/?lang=en-US&ll={},{}&z=12"
                        "&l=map&size=650,350&pt={},{},"
                        "vkgrm").format(
                            longitude, latitude,
                            longitude, latitude) if longitude
                                                 and latitude else ""
                    }
                ]
            }
        request = urllib2.Request(settings.webhook)
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request, json.dumps(data))
        return response


    def update_seen(self, item_id):
        """Updates the seen_items

        Args:
            item_id (str): A unique identifier for the item.
        """
        with open("seen_items", "a+") as f:
            f.write(item_id + "\n")


    def check_seen(self):
        """Get the items from seen_items

        Returns:
            (list): A list of the items in seen_items
        """
        with open("seen_items", "r") as f:
            return f.read().splitlines()



if __name__ == "__main__":
    bot = Bot()
    bot.run()
