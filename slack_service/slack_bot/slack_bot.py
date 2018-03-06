import time
import requests
from websocket import WebSocketConnectionClosedException

#Default for the websocket read delay
READ_DELAY = 1


class SlackBot():
    """
        Class for connecting to a slack team and persisting. While connected
        user messages to @"name_of_bot_in_team" or direct messages to the bot
        will be posted via http to the ai_api (currently the rasa_service).
        This api will return a response message, which will in turn be passed
        back to the user in the correct
        slack channel.
    """
    def __init__(self, slack_client, bot_id, ai_api,
                 READ_WEBSOCKET_DELAY=READ_DELAY):
        """
            Args:
                slack_client: slack client object
                bot_id:
                ai_api:
                READ_WEBSOCKET_DELAY: (float) how long to wait in seconds
                    before refreshing

            Attr:
                client: slack client object that has connection methods
                at_bot_str: string used tell if the user is talking to the bot
                ai_api: string containing the url of the api that will do
                    the natural lanaguage processing. The api accepts post
                    requests with user text input and resonds with json
                    containing the bots response
        """
        self.client = slack_client
        self.bot_id = bot_id
        self.at_bot_str = "<@" + bot_id + ">"
        self.ai_api = ai_api
        self.READ_WEBSOCKET_DELAY = READ_WEBSOCKET_DELAY

    def handle_command(self, command, channel):
        """
            This method takes in a user message, posts it to the ai_api
            and then posts the message to the slack client.

            Args:
                command: (string) text user has send to bot
                channel: not sure the type
        """
        ai_response = requests.post(self.ai_api, json={'user_text': command,
                                                       'channel_id': channel})
        response = ai_response.json()
        # TODO: Validate JSON and handle errors

        if('response_text' in response):
            response_text = response['response_text']
            self.client.api_call("chat.postMessage", channel=channel,
                                 text=response_text, as_user=True)

        if('file_upload_name' in response):
            file_name = response['file_upload_name']
            self.client.api_call('files.upload',
                                 filename=file_name,
                                 channels=channel,
                                 file=open(file_name, 'rb'))

    def clean_text(self, text):
        """
            Removes any text with with the bot string in it.
            Eg.
                clean_text('@botname Hello') = 'Hello'

            TODO: get it to remove emoji icons

        """
        if self.at_bot_str in text:
            return text.split(self.at_bot_str)[1].strip().lower()
        else:
            return text

    @staticmethod
    def valid_message(message_dict):
        """
            Returns:
                True if message is valid
                False otherwise
        """
        if message_dict:
            if 'text' in message_dict and 'channel' in message_dict:
                return True
        return False

    def message_for_bot(self, message_dict):
        """

        """
        assert('text' in message_dict)
        assert('channel' in message_dict)

        is_direct_message = message_dict['channel'][0] == 'D'
        is_at_bot = self.at_bot_str in message_dict['text']

        directed_at_bot = is_direct_message or is_at_bot

        is_other_bot = 'bot_id' in message_dict
        is_this_bot = ('user' in message_dict and
                       message_dict['user'] == self.bot_id)
        # TODO: Write extra conditions like is not slackbot ect.
        is_type_message = ('type' in message_dict and
                           message_dict['type'] == 'message')
        is_ephemeral = ('is_ephemeral' in message_dict
                        and message_dict['is_ephemeral'])
        # User messages the bot in a direct message channel

        if (directed_at_bot and
                not is_other_bot and
                not is_ephemeral and
                not is_this_bot and
                is_type_message):
            return True

        return False

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.

            Args:
                slack_rtm_output: (I don't know what exactly what this looks
                    like it would be great if an example could be inserted)

            Returns:
                (command, channel): The text sent by the user followed by the
                    channel from which it was sent in tuple form.
                    If there was no user message sent to the bot then
                    (None, None) is returned.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if self.valid_message(output):
                    if self.message_for_bot(output):
                        cleaned_text = self.clean_text(output['text'])
                        return (cleaned_text, output['channel'])

        return (None, None)

    def run_cycle(self):
        """
            Performs 1 run cycle.
            1st:
                Checks the output of the slack rtm and if there is user text
                directed at the bot then the bot will respond to them.
            2nd:
                Waits for 1 second.
        """
        try:
            rtm_output = self.client.rtm_read()
            command, channel = self.parse_slack_output(rtm_output)
            if command and channel:
                self.handle_command(command, channel)
            time.sleep(self.READ_WEBSOCKET_DELAY)

        except WebSocketConnectionClosedException as e:
            print(e)
            print('Caught websocket disconnect, reconnecting...')
            time.sleep(self.READ_WEBSOCKET_DELAY)
            # TODO: make sure it keeps trying to connect
            self.client.rtm_connect()
        except Exception as e:
            print(e)
            time.sleep(self.READ_WEBSOCKET_DELAY)
            self.client.rtm_connect()

    def run(self):
        """
            This method connects to the team slack channel and persists.
            The slack rtm (real time message api), is checked every second
            and if there is user text directed at the bot then the bot will
            respond to them.
        """
        if self.client.rtm_connect():
            while True:
                self.run_cycle()
        else:
            print("Connection failed. Invalid Slack token or bot ID.")
