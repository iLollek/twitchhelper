# TwitchHelper - Made by iLollek
# CYBER TRANCE
# "I write better Code", he said. And thus, wrote another unusual Comment Line which will get lost once he compiles. Sad to see to be honest.

# General Imports
import os
import sys
import asyncio
import threading
import time
import logging

# twitchhelper specific imports
import chatreadingmodule
import mediamodule
import twitchapimodule

if getattr(sys, 'frozen', False):
   program_directory = os.path.dirname(os.path.abspath(sys.executable))
else:
   program_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(program_directory)

# Constants
SERVER = 'irc.chat.twitch.tv'
PORT = 6667
NICKNAME = ''
TOKEN = ''
CHANNEL = ''
CLIENT_ID = ""
CLIENT_SECRET = ""

message_counter = 0
viewercount = "0"

# Read configuration from config.txt
config = {
    "silent_mode": False,
    "logging_enabled": True,
    "log_file_path": "twitchhelper.log",
    "log_chatmessages" : False,
    "chatmessage_log_file_path": "chat.log"
}

def read_logfile():
    config_file_path = os.path.join(program_directory, "config.txt")
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as config_file:
            for line in config_file:
                key, value = line.strip().split("=")
                config[key] = value.lower() == "true"
read_logfile()

print(f'========================================\nThank you for using twitchhelper.\nRunning with following Config:\nLogging Enabled: {config["logging_enabled"]}\nSilent Mode: {config["silent_mode"]}\nLog Chatmessages: {config["log_chatmessages"]}\nMade by iLollek\n========================================')

# Initialize logging
if config["logging_enabled"]:
    logging.basicConfig(filename=config["log_file_path"], level=logging.DEBUG)

def threaded_update_viewercount():
    global viewercount
    while True:
        viewercount = twitchapimodule.get_viewer_count(CHANNEL, CLIENT_ID, CLIENT_SECRET)
        if not config["silent_mode"]:
            print(f'Updated Viewercount!')
        if config["logging_enabled"]:
            logging.info('Updated Viewercount!')
        os.system(f'title twitchhelper - Hook: {CHANNEL} - Viewers: {viewercount} - Messages: {message_counter}')
        time.sleep(30)

def threaded_update_media():
    while True:
        information_dictionary = asyncio.run(mediamodule.get_media_info())
        f = open(f'media_info.txt', "w")
        f.write(f'{information_dictionary["artist"]} - {information_dictionary["title"]}')
        f.close()
        if not config["silent_mode"]:
            print(f'Updated Mediafile!')
        if config["logging_enabled"]:
            logging.info('Updated Viewercount!')
        time.sleep(15)


viewercount_thread = threading.Thread(target=threaded_update_viewercount)
viewercount_thread.start()

updatemedia_thread = threading.Thread(target=threaded_update_media)
updatemedia_thread.start()

irc = chatreadingmodule.connect_to_twitch(SERVER, PORT, TOKEN, NICKNAME, CHANNEL)
print("Connection to Twitch IRC Successful.")
token = twitchapimodule.get_oauth_token(CLIENT_ID, CLIENT_SECRET)
print("Connection to Twitch API Successful.")

while True:
    message = irc.recv(2048).decode('utf-8')
    if message.startswith('PING'):
        # (iL) 28.01.2024 - If we don't respond to pings we get disconnected and spammed with empty strings.
        irc.send("PONG\r\n".encode('utf-8'))
        print(f'Sent PONG-Response.')
    parsed_message = chatreadingmodule.parse_message(message, CLIENT_ID, CLIENT_SECRET)
    if parsed_message != None:
        message_counter += 1
        print(parsed_message)
        if config["log_chatmessages"]:
            f = open(config["chatmessage_log_file_path"], "a")
            f.write(f'{parsed_message}\n')
            f.close()
    if config["logging_enabled"]:
        logging.info(parsed_message)
    os.system(f'title twitchhelper - Hook: {CHANNEL} - Viewers: {viewercount} - Messages: {message_counter}')
    