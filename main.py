import discord
import os
import requests
import json
from pprint import pprint
from math import floor
import random
from keep_alive import keep_alive

client = discord.Client()
#---------------------------------------------------------------
random_quotes = "https://zenquotes.io/api/random"


def get_random_quote():
    response = requests.get(random_quotes)
    data = json.loads(response.text)
    rand_quote = data[0]['q'] + " ~ " + data[0]['a']
    return (rand_quote)


#---------------------------------------------------------------
movie_stuff = "http://www.omdbapi.com/?i=tt3896198&apikey=5c9a5372"

#---------------------------------------------------------------
Forecast = "https://community-open-weather-map.p.rapidapi.com/forecast"
Forecast_query = {"q": "Graz,at"}
Forecast_headers = os.getenv('Forecast_headers')

Weather = "https://community-open-weather-map.p.rapidapi.com/weather"
Weather_query = {"q": "Graz,at", "lang": "-de", "units": "metric"}
Weather_headers = os.getenv('Weather_headers')



def get_forecast():
    response = requests.request("GET",
                                Forecast,
                                headers=Forecast_headers,
                                params=Forecast_query)
    data = json.loads(response.text)
    times = []
    max_temp = []
    min_temp = []
    rain_prop = []
    for timestamp in data['list']:
        times.append(timestamp['dt_txt'])
        max_temp.append(timestamp['main']['temp_max'] - 273.15)
        min_temp.append(timestamp['main']['temp_min'] - 273.15)
        rain_prop.append(timestamp['pop'] * 100)
    return (times, max_temp, min_temp, rain_prop)


#---------------------------------------------------------------


def get_weather():
    Weather_data = requests.request("GET",
                                    Weather,
                                    headers=Weather_headers,
                                    params=Weather_query)
    data = json.loads(Weather_data.text)
    pprint(data)
    temp = data['main']['temp']
    hum = data['main']['humidity']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    windir = (data['wind']['deg'])
    windv = (data['wind']['speed'])
    temp_feel = data['main']['feels_like']
    print(str(temp) + " " + str(hum))
    return (temp, hum, temp_min, temp_max, windir, windv, temp_feel)


#---------------------------------------------------------------
def get_movie_quote():
    lines = open('movie.csv').read().splitlines()
    return random.choice(lines)


def get_quote():
    lines = open('quotes.txt').read().split("----")
    return random.choice(lines)
  
def get_disc_quote():
  lines = open('disc_zitate.txt').read().split("----")
  return random.choice(lines)

# print(get_movie_quote())
# print(get_quote())
#---------------------------------------------------------------

#---------------------------------------------------------------


@client.event
async def on_ready():
    print("Bot is logged in to Discord as {0.user}".format(client))

commands = {'filmzitat':'Schickt ein zufälliges Filmzitat','zitat':'Schickt ein zufälliges Zitat','wetter':'Schickt dir das aktuelle Wetter in Graz','wetterbericht':'Prototype, Wetterbericht'}
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$sprich'):
        await message.channel.send('Hide the pain')
    if message.content.startswith('$filmzitat'):
        await message.channel.send(get_movie_quote())
    if message.content.startswith('$zitat'):
        if (random.random() < 0.5):
            await message.channel.send(get_random_quote())
        else:
            if(random.random()<0.2):
              await message.channel.send(get_disc_quote())
            else:
              await message.channel.send(get_quote())
    # if message.content.startswith('$roast'):
    #   await message.channel.send(roast())
    if message.content.startswith('$wetterbericht'):
        retrun_forecast = get_forecast()
        msg = "Wetter für die nächsten Tage:"
        i = 0
        for item in retrun_forecast:
            msg += "\n\t"
            for entry in item:
                if(i%8):
                  msg += " " + str(entry) + " "
                i+=1
        await message.channel.send(msg)
    if message.content.startswith('$wetter'):
        wr = get_weather()
        dirs = ['Ochsen', 'Neun', 'Whiskey', 'Saufen']
        winddir = wr[4]
        winddir = dirs[floor(winddir / 360)]
        print(winddir)
        mod = ""
        if (wr[6] < 0):
            mod = " Older es is oasch kolt!"
        msg = ("Das Wetter heute in Graz:\n\tTemperatur: " + str(wr[0]) +
               " °K - Fühlt sich an wie: " + str(wr[6]) + " °K " + mod +
               "\n\tHumidity: " + str(wr[1] * 10) + "‰\n\tMin: " + str(wr[2]) +
               " °G\tMax: " + str(wr[3]) + " °B\n\tDer Wind kommt heute aus " +
               winddir + " mit " + str(wr[5] / 300000000) + " c.")
        await message.channel.send(msg)
    if message.content.startswith('$help'):
      msg = "Verfügbare Commands: \n"
      for key, value in commands.items():
        msg+=("\n\t-) $"+str(key)+": "+str(value))
      await message.channel.send(msg)

keep_alive()
client.run(os.getenv('TOKEN'))
