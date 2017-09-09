from flask import Flask, request
from pymessenger import Bot
from utils import fetch_reply

app = Flask(__name__)

FB_ACCESS_TOKEN = "YOUR PAGE ACCESS TOKEN"

bot = Bot(FB_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == "page":
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					query = messaging_event['message']['text']
					reply = fetch_reply(query, sender_id)

					if reply['type'] == 'text':
						bot.send_text_message(sender_id, reply['data'])
	return "ok", 200



def log(msg):
	print(msg)


if __name__ == "__main__":
	app.run(port=8000, use_reloader=True)