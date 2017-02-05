# Traffic Bot :oncoming_automobile:

Traffic Bot is a [slack](https://slack.com/) bot for traffic alerts in the UK. Data is pulled from an xml feed from [highways.gov.uk](http://www,highways.gov.uk), and then pushed to your slack webhook.

[data.gov.uk link](https://data.gov.uk/dataset/live-traffic-information-from-the-highways-agency-road-network/resource/7b941228-e805-4933-b417-a4eb6fb0fa77)

![example image](http://i.imgur.com/mBw7RwW.png)

## Installation

Simply download this project:

```bash
git clone https://github.com/alxwrd/slack-traffic-uk.git
```

Configure `settings.py`:

```python
webhook = "https://hooks.slack.com/your/hook/address"
location = {"longitude": -0.1556985,
            "latitude": 51.5195499}
max_distance = 50
```

Then run `traffic_bot.py`

```bash
cd slack-traffic-uk
python traffic_bot.py
```

Traffic Bot will run once, and post any new items to your webhook. To run automatically, add it to your crontab.


## Contributors

Contributions are welcome! Please raise an [issue](https://github.com/alxwrd/slack-traffic-uk/issues/new) with any problems or suggestions. Or submit a pull request!
