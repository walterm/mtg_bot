# Import some necessary libraries.
import socket
import urllib2
import json

# Some basic variables used to configure the bot        
server = "irc.freenode.net" # Server
channel = "#hackNY" # Channel
botnick = "walterbot" # Your bots nick

def printMsg(msg):
  botresp = 'PRIVMSG ' + channel + ' :' + nick + ': ' + msg  + '\r\n'
  ircsock.send(botresp)


def cardDictionary(data):
  cards = {}
  for card in data:
    cardname = card["name"]
    if cardname in cards:
       cards[cardname] += 1
    else: cards[cardname] = 1
  return cards

def printOutCard(card, data):
  carddata = data[0]
  printMsg(card + " | " + (" | ").join(carddata['description'].split("\n")))


def printAmbiguous():
  printMsg("There were too many cards returned! Tell me more things.")

def printClarify(cardname):
  url = "http://api.mtgdb.info/search/" + cardname
  response = urllib2.urlopen(url)
  carddata = json.load(response)
  unique_cards = cardDictionary(carddata)
  printMsg('So this is what I found. ' + (' | ').join(unique_cards.keys()))
  printMsg("Which one did you mean?")

def printNoCards(cardname):
  url = "http://api.mtgdb.info/search/" + cardname
  response = urllib2.urlopen(url)
  carddata = json.load(response)
  unique_cards = cardDictionary(carddata)
  if len(carddata) != 0:
    printClarify(unique_cards)

def commands(nick, channel, message):
    if message.find(botnick+" tellme") != -1:
        msg = message.split(" ")
        cardname = "_".join(msg[msg.index("tellme")+1:])
        url = "http://api.mtgdb.info/cards/" + cardname
        response = urllib2.urlopen(url)
        carddata = json.load(response)
        if len(carddata) == 0:
            printClarify(cardname)
        else:
            printOutCard(carddata[0]["name"], carddata)
        
def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello Mybot"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")
                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
##  print(ircmsg) # Here we print what's coming from the server

  if ircmsg.find(' PRIVMSG ') != -1:
      nick = ircmsg.split('!')[0][1:] # getting the nick of who sent it
      channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
      commands(nick, channel, ircmsg)

  if ircmsg.find(":Hello "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello()
    hello()

  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
    ping()
