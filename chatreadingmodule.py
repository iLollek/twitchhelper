# The Chat Reading Module (chatreadingmodule.py) is needed to read Chat messages. It is an existential part of twitchhelper.
# Made by iLollek

from datetime import datetime
import socket
import re
import twitchapimodule

user_colors = {}

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("[%H:%M:%S]")
    return timestamp

def print_colored_text(text, color_code):
    # ANSI escape code for setting text color
    color_format = "\033[38;2;{};{};{}m"
    
    # Extract RGB values from HTML color code
    r = int(color_code[1:3], 16)
    g = int(color_code[3:5], 16)
    b = int(color_code[5:7], 16)

    # Construct the color format string
    color_format = color_format.format(r, g, b)

    # ANSI escape code for resetting text color
    reset_format = "\033[0m"

    return color_format + text + reset_format

# Function to connect to Twitch IRC
def connect_to_twitch(SERVER, PORT, TOKEN, NICKNAME, CHANNEL):
    irc = socket.socket()
    irc.connect((SERVER, PORT))
    
    # Authentication
    irc.send(f"PASS {TOKEN}\n".encode('utf-8'))
    irc.send(f"NICK {NICKNAME}\n".encode('utf-8'))
    irc.send(f"JOIN #{CHANNEL}\n".encode('utf-8'))
    
    return irc

# Function to parse Twitch messages
def parse_message(message, CLIENT_ID, CLIENT_SECRET):
    # Example: ":username!username@username.tmi.twitch.tv PRIVMSG #channel :message"
    pattern = re.compile(r'^:([^!]+)![^ ]+ PRIVMSG #[^ ]+ :(.+)$')
    match = pattern.match(message)
    
    if match:
        username = match.group(1)
        message_text = match.group(2)
        try:
            if username in user_colors.keys():
                return f"{get_timestamp()} {print_colored_text(username, user_colors[username])}: {message_text}"
            else:
                user_color = twitchapimodule.get_user_chat_color(twitchapimodule.get_user_id_by_name(username, CLIENT_ID, CLIENT_SECRET), CLIENT_ID, CLIENT_SECRET)
                user_colors[username] = str(user_color)
                return f"{get_timestamp()} {print_colored_text(username, user_colors[username])}: {message_text}"
        except KeyError:
                user_color = twitchapimodule.get_user_chat_color(twitchapimodule.get_user_id_by_name(username, CLIENT_ID, CLIENT_SECRET), CLIENT_ID, CLIENT_SECRET)
                user_colors[username] = str(user_color)
                return f"{get_timestamp()} {print_colored_text(username, user_colors[username])}: {message_text}"
    
    return None