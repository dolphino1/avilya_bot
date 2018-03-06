#
from flask import Flask, jsonify, request
from rasa_core.agent import Agent
from flask_script import Manager
from rasa_core.channels.channel import OutputChannel


class CustomChannel(OutputChannel):
    def __init__(self):
        self.message = None

    def send_text_message(self, recipient_id, message):
        self.message = ({"recipient_id": recipient_id,
                         "response_text": message})

    def send_custom_message(self, recipient_id, elements):
        message = elements[0]
        message.update({"recipient_id": recipient_id})
        self.message = message

    def latest_output(self):
        return self.message

# instantiate the app
app = Flask(__name__)

# set config
#app.config.from_object('config.DevelopmentConfig')
core_model = "rasa_api/models/dialogue"
nlu_model = "rasa_api/models/nlu/current"
channel = CustomChannel()

my_agent = Agent.load(core_model, interpreter=nlu_model)


@app.route('/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_text = data['user_text']
    send_id = data['channel_id']
    my_agent.handle_message(user_text,
                            output_channel=channel,
                            sender_id=send_id)
    return jsonify(channel.latest_output())


manager = Manager(app)


if __name__ == '__main__':
    manager.run()
