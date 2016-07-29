import os
import time
from slackclient import SlackClient

from actions import actions


def process(messages):
    for message in messages:
        if message.get('text'):
            for action, options in actions.items():
                match = options['regex'].match(message['text'])
                if match:
                    print('match on {}'.format(action))
                    args = (message, match.group('owner'), match.group('repo'))
                    try:
                        reply = options['callback'](*args)
                    except Exception as e:
                        print('exception', e)
                        reply = '{}'.format(e)
                    if reply:
                        channel_id = message['channel']
                        channel = client.server.channels.find(channel_id)
                        print(reply)
                        channel.send_message(reply)


token = os.environ['SLACK_TOKEN']
client = SlackClient(token)
if client.rtm_connect():
    print('Listening')
    while True:
        process(client.rtm_read())
        time.sleep(1)
else:
    print('Connection Failed')
