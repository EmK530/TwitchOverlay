import time
import random
import datetime
import math
try:
   import websocket
except ImportError:
   from os import system
   system('pip install websocket-client')
   import websocket
from threading import Thread
from Render import messages,launched
import random

success=False
nonce = ""
running=[False]
old=print
username='justinfan%i' % random.randint(10000, 99999)
def print(string):
   old("[TwitchSocket] "+string)

channel = input("[1/3] Input name of account to track: ")
#channel = "EmK530"
start = time.time()
channel=channel.lower()
def write(string):
   global messages
   messages.append(string)

def send_message(ws, msg):
   global nonce
   ws.send("@client-nonce="+nonce+" PRIVMSG #"+channel+" :"+msg)

def on_message(ws, message):
   global success
   global launched
   global lifetime
   global nonce
   global write
   global handle_message
   global running
   #print(message)
   if "Welcome, GLHF!" in message:
      ws.send("JOIN #"+channel+"")
      #print("Client welcomed, joining channel")
      print("Twitch connection opened!")
      running[0] = True
      nonce = ("%032x" % random.getrandbits(128))
      #ws.send("@client-nonce="+nonce+" PRIVMSG #"+channel+" :"+"Server is now online, hello world!")
   elif "PRIVMSG" in message and (not "client-nonce=" in message or message.split("client-nonce=")[1].split(";")[0] != nonce):
      msg = message.split("PRIVMSG")[1].split(":")[1].split("\r")[0]
      name = message.split("display-name=")[1].split(";")[0]
      write(name+": "+msg)
   elif "NOTICE" in message:
      msg=message.split("NOTICE")[1].split(":")[1]
      print("NOTICE: "+msg)
   elif "authentication failed" in message:
      print("Login failed.")
      ws.close()
   elif "PING" in message:
      if launched[0]:
         print("Twitch PING PONG")
      ws.send("PONG")

def on_error(ws, error):
   print("ERROR! '"+str(error)+"'")
   running[0] = False
   ws.close()

def on_close(ws,a,b):
   print("Connection closed")

def on_open(ws):
   print("Authenticating...")
   ws.send('CAP REQ :twitch.tv/tags twitch.tv/commands')
   ws.send('PASS SCHMOOPIIE')
   ws.send('NICK '+username)
   ws.send('USER '+username+' 8 * :'+username)
   print("Login sent")
def run():
   while True:
      print("Connecting to Twitch...")
      websocket.enableTrace(False)
      ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv/",
      on_message = on_message,
      on_error = on_error,
      on_close = on_close,
      header = {
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-US,en;q=0.7',
         'Cache-Control': 'no-cache',
         'Connection': 'Upgrade',
         'Pragma': 'no-cache',
         'Host': 'irc-ws.chat.twitch.tv',
         'Origin': 'https://www.twitch.tv',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
      })
      ws.on_open = on_open
      ws.run_forever()
