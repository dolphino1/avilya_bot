import unittest
from unittest.mock import patch
from slack_bot.slack_bot import SlackBot
from websocket import WebSocketConnectionClosedException


class FakeSlackClient():
    """
        Fake class for slack client.
    """
    def __init__(self):
        self.messages = []
        self.connected = False

    def rtm_connect(self):
        self.connected = True

    def api_call(self, post_type, channel, text, as_user):
        self.post_type = post_type
        self.channel = channel
        self.text = text
        self.as_user = as_user


class SlackBotTestCase(unittest.TestCase):

    def setUp(self):
        self.fake_client = FakeSlackClient()
        self.bot = SlackBot(self.fake_client, 'fake_bot', 'fake_api_string')

    @patch('requests.post')
    def test_handle_command(self, mock_api_call):
        """"
            Messages passed to the handle_command function must post to the
            ai api.
        """
        self.bot.handle_command('fake message', 'fake_channel')
        mock_api_call.assert_called_with('fake_api_string',
                                         json={'user_text': 'fake message'})

    def test_parse_slack_output_empty_single_input(self):
        """
            Empty slack output must produce (None, None)
        """
        self.assertEquals((None, None), self.bot.parse_slack_output({}))

    def test_parse_slack_output_single_input(self):
        """
            Single message from a channel directed at the bot must return
            (message, channel)
        """
        fake_rtm_input = [{'text': '<@fake_bot>fake message',
                           'type': 'message',
                           'channel': 'fake_channel'}]

        self.assertEquals(('fake message', 'fake_channel'),
                          self.bot.parse_slack_output(fake_rtm_input))

    def test_parse_slack_single_input_not_for_bot(self):
        """
            Single message from a channel not directed at the bot must return
            (None, None)
        """
        fake_rtm_input = [{'text': 'fake message',
                           'type': 'message',
                           'channel': 'fake_channel'}]
        self.assertEquals((None, None),
                          self.bot.parse_slack_output(fake_rtm_input))

    def test_parse_slack_output_empty_multiple_input(self):
        """
            Multiple empty input must return (None, None)
        """
        fake_rtm_inputs = [{}, {}, {}]
        self.assertEquals((None, None),
                          self.bot.parse_slack_output(fake_rtm_inputs))

    def test_parse_slack_multiple_inputs(self):
        """
            define behaviour for this.
        """
        pass

    @patch('time.sleep')
    def test_run_cycle_sleeps(self, mock_sleep_call):
        self.bot.client.rtm_read = lambda: [{}]
        self.bot.run_cycle()
        mock_sleep_call.assert_called_with(self.bot.READ_WEBSOCKET_DELAY)

    @patch('time.sleep')
    def test_run_cycle_websocket_fail_causes_reconnect(self, mock_sleep):
        """

        """
        def raise_web_closed():
            raise WebSocketConnectionClosedException()

        self.bot.client.connected = False

        self.bot.client.rtm_read = raise_web_closed
        self.assertTrue(self.bot.client.rtm_connect)
