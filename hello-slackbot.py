import os
import time
from slackclient import SlackClient

#bot name
BOT_NAME = 'hello-slackbot'

#get bot id
BOT_ID = os.environ.get('SLACK_BOT_ID')

#get slack bot token
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

#set slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)


# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

def parse_slack_output(slack_rtm_output):
	output_list = slack_rtm_output

	if output_list and len(output_list) > 0:
		for output in output_list:
			if len(output.keys()) < 9:
				if output and 'text' in output and AT_BOT in output['text']:
					# return text after the @ mention, whitespace removed
					return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
				elif output and 'text' in output and output['channel'].startswith('D'):
					return output['text'].strip().lower(), output['channel']
	return None, None


def handle_command(command, channel):
	response = "Not sure what you mean. Please use the " + EXAMPLE_COMMAND + "* command with numbers"
	if command.startswith(EXAMPLE_COMMAND):
		response = "Sure...write some more code then I can do that!"
	elif command == "hello":
		response = "Hi there! I'm " + BOT_NAME

	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)



if __name__ == '__main__':
	READ_WEBSOCKET_DELAY = 0.5 #per second
	if slack_client.rtm_connect():
		print(BOT_NAME + " connected and running!")
		while True:
			rtm = slack_client.rtm_read()

			command, channel = parse_slack_output(rtm)

			if command and channel:
				handle_command(command, channel)

			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print(BOT_NAME+ " not connected!")