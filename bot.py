import os
from telebot import TeleBot, types
from flask import Flask, request

TOKEN = '783413098:AAFrVmHoECsxej5FnpiTLTDetn_3EsP8Vko'
bot = TeleBot(token=TOKEN)
GROUP_ID = -1001081775670
MOELLE_CHAT_ID = 263179251

server = Flask(__name__)


@bot.message_handler(content_types=['text'])
def bug_handler(message):
    if message.text == "#bug":
        if message.reply_to_message is not None:
            bot.reply_to(message,
                         f"Thanks for reporting a bug {message.from_user.first_name},"
                         + " I shall take care of it from here.")
            bot.forward_message(MOELLE_CHAT_ID, GROUP_ID, message.reply_to_message.message_id)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route('/shutdown')
def shutdown():
    bot.remove_webhook()
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dd-bugbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
