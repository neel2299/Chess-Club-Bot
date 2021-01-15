import discord
import os
from replit import db
import requests 
import re
from webser import webser
def rating_finder(rat_type,user):
  URL="https://api.chess.com/pub/player/"+user+"/stats"
  r = requests.get(URL) 
  conten=r.content.decode('utf-8')
  if rat_type == 'rapid':
    pattern = re.compile(r'chess_rapid')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  if rat_type == 'blitz':
    pattern = re.compile(r'chess_blitz')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  if rat_type == 'bullet':
    pattern = re.compile(r'chess_bullet')
    matches = pattern.finditer(conten)
    for match in matches:
      x=match.span()[1]+20
      if(conten[x+3]==','):
        return conten[x:x+3]
      return(conten[x:x+4])
  return '0'

def update_members(username):
  if "members" in db.keys():
    members = db["members"]
    members.append(username)
    db["members"] = members
  else:
    db["members"] = [username]


def delete_members(username):
  members = db["members"]
  if username in members:
    index=members.index(username)
    del members[index]
    db["members"] = members


def show_data(members,parameter):
  dic = {}
  for member in members:
    dic[member]=int(rating_finder(parameter, member))
  rat_list = sorted(dic.values(),reverse=True)
  bigdic = {}
  for i in rat_list:
    for k in dic.keys():
        if dic[k] == i:
            bigdic[k] = dic[k]
            break
  k=1
  msg=''
  for i in bigdic:
    msg=msg+str(k)+"\t"+i+"\t"+str(bigdic[i])+"\n"
    k=k+1
  return msg


members_starter=['vedantttt','ID_15','pawn_2222','neelk22','XREVERBX']
client=discord.Client()


@client.event
async def on_ready():
  print('Hi there, this is{0.user}'.format(client) )
@client.event
async def on_message(message):
  if message.author==client.user:
    return
  msg = message.content
  if msg.startswith('$show'):
    parameter = msg.split("$show ",1)[1]
    members_all=db["members"]+members_starter
    out_msg = show_data(members_all, parameter)
    await message.channel.send(out_msg)
  if msg.startswith("$add"):
    username = msg.split("$add ",1)[1]
    update_members(username)
    await message.channel.send("New username added.")
  if msg.startswith("$remove"):
    username = msg.split("$remove ",1)[1]
    delete_members(username)
    await message.channel.send("Username removed.")
webser()
client.run(os.getenv('TOKEN'))
