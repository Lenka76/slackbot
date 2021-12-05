import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import string

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"],"/slack/events",app)

client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
BOT_ID = client.api_call("auth.test")["user_id"]

#key words to search in message
clue_words1 = ["požadavek na přidání distributora"]
clue_words2 = ["požadavek na export dat"]
clue_words1a = ["země", "ičo", "název distributora"]
clue_words2a = ["důvod", "země", "období", "něco navíc", "struktura dat"]

def check_if_clue_words1(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans(" ", " ", string.punctuation))

    return any(word in msg for word in clue_words1)

def check_if_clue_words1a(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans(" ", " ", string.punctuation))

    return all(word in msg for word in clue_words1a)

def check_if_clue_words2(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans(" ", " ", string.punctuation))

    return any(word in msg for word in clue_words2)

def check_if_clue_words2a(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans(" ", " ", string.punctuation))

    return all(word in msg for word in clue_words2a)



@slack_event_adapter.on("message")
def message(payLoad):
    event = payLoad.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

#check message and reply accordingly
    if BOT_ID != user_id:
        ts = event.get("ts")
        if check_if_clue_words1(text) == True:
            if check_if_clue_words1a(text) == False:
                client.chat_postMessage(
                channel=channel_id, 
                thread_ts = ts, 
                text="Text goes here")
        elif check_if_clue_words2(text) == True:
            if check_if_clue_words2a(text) == False:
                client.chat_postMessage(
                channel=channel_id, 
                thread_ts = ts, 
                text="Text goes here")                
        else: client.chat_postMessage(
                channel=channel_id, 
                thread_ts = ts, 
                text="Text goes here")

if __name__ == "__main__" :
    app.run(debug=True)