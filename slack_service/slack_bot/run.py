from slackclient import SlackClient
from slack_bot import SlackBot
import os

if __name__ == "__main__":

    SLACK_KEY = os.environ['SLACK_KEY']
    RASA_API_URL = 'http://rasa-service:5000/chat'

    client_obj = SlackClient(SLACK_KEY) 
    bot_id = client_obj.api_call("auth.test")["user_id"]

    bot = SlackBot(client_obj, bot_id, RASA_API_URL)
    bot.run()
