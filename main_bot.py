# TODO: run main_bot.py and send messages to the bot on your Telegram app

import requests  # make web requests to interact with Telegram API
import json  # parse the JSON response from Telegram into Python dictionaries in order to extract the data we need
import time  # specify the time interval between requests

TOKEN = "1092583779:AAH5twuJGIo3MXmVUM3aL0SF2p0q5WdbOm4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)  # create a basic URL that will be used in all requests to the API


# 1. a function to download content from a URL and give us a string
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")  # decode("utf8") is to ensure text compatibility
    return content


# 2. a function to take the string from get_url and parse it into a Python dictionary
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# 3. a function to retrieve all the messages recently sent to our bot using getUpdates command from Telegram API
def get_updates(offset=None):  # offset is to let Telegram API know we don't want any messages with IDs smaller than this
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# 4. a function to find out the highest update ID so far, to be passed to get_updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# 5. a function for bot to reply the user using sendMessage command from Telegram API
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


# 6. a function to go through each new message and send a reply using send_message
# def reply_all(updates):
#     for update in updates["result"]:
#         text = update["message"]["text"]
#         chat_id = update["message"]["chat"]["id"]
#         if text == "/start":
#             send_message("Hello, do you want to listen to music? Please type Yes/No", chat_id)
#         elif text == "/done":
#             send_message("See you again friend :)", chat_id)
#         elif text == "No" or text == "no":
#             send_message("Please visit @movieS4Bot to check out movie recommendations!", chat_id)
#         elif text == "Yes" or text == "yes":
#             send_message("Please visit @spotybot to play some Spotify songs!", chat_id)


# # 6. a function to echo every message that you send to the bot
def echo(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        send_message(text, chat_id)


# 7. put all pieces together
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)  # retrieve messages that we haven't seen before
        print(updates)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo(updates)       # the bot sends a response to each new message
        time.sleep(0.5)         # wait for half sec before checking for new message again


if __name__ == '__main__':
    main()
