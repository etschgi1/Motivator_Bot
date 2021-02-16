import discord
import os
import requests
import json

client = discord.Client()
movie_quotes = "https://juanroldan1989-moviequotes-v1.p.rapidapi.com/api/v1/quotes"
random_quotes = "https://zenquotes.io/api/random"
querystring = {"actor":"Al Pacino"}
headers = {
    'authorization': "Token token=yd8WzkWNEEzGtqMSgiZBrwtt",
    'x-rapidapi-key': "c7503a43f4msh8782077191ee4d8p10a4a5jsnea9a70866ccd",
    'x-rapidapi-host': "juanroldan1989-moviequotes-v1.p.rapidapi.com"
    }

response = requests.request("GET",movie_quotes,headers=headers,params=querystring)

print(response.text)


def get_random_quote():
  response = requests.get(random_quotes)
  data = json.loads(response.text)
  rand_quote = data[0]['q'] + " ~ "+data[0]['a']
  return(rand_quote)

@client.event
async def on_ready():
  print("Bot is logged in to Discord as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$sprich'):
    await message.channel.send('Hide the pain')
  if message.content.startswith('$zitat'):
    await message.channel.send(get_random_quote())

client.run(os.getenv('TOKEN'))
