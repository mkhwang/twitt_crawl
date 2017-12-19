import configparser
import os

class Key:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('key.ini')

        self.twitt_consumer_key = config.get('twitt', 'consumer_key')
        self.twitt_consumer_secret = config.get('twitt', 'consumer_secret')
        self.twitt_access_token = config.get('twitt', 'access_token')
        self.twitt_access_token_secret = config.get('twitt', 'access_token_secret')
        self.slack_token = config.get('slack', 'token')
        self.slack_channel = config.get('slack', 'channel')
