import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import ntplib
from datetime import datetime, timedelta, date, time as dt_time
import requests
import opuslib
import opuslib.api
import opuslib.api.encoder
import opuslib.api.decoder
import glob
import os
import traceback
import time
import youtube_dl
import feedparser
from bs4 import BeautifulSoup
from lxml import html
import json


try:
    with open('config.json') as file:
        config = json.load(file)
except EnvironmentError:
    print('File with settings ("config.json") not found.')
    raise SystemExit
if 'PATH' not in config: 
		await client.say('The path to the folder with the script is not specified in the configuration file.')
		raise SystemExit
if 'BOT_TOKEN' not in config:
	await client.say('A token is not specified in the configuration file.')
	raise SystemExit

client = commands.Bot(command_prefix=config['COMMAND_PREFIX'], description=config['BOT_DESCRIPTION'])



@client.event
async def on_ready():
    users = str(len(set(client.get_all_members())))
    servers = str(len(client.servers))
    channels = str(len([c for c in client.get_all_channels()]))
    client.uptime = int(time.perf_counter())
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print(servers + " servers")
    print(channels + " channels")
    print(users + " users")
    print("\n{0} active cogs with {1} commands\n".format(
        str(len(client.cogs)), str(len(client.commands))))
    print('--------------------------------------')
    if discord.opus.is_loaded():
    	print("opuslib is loaded!")
    else:
    	print("opuslib is not loaded, voice not available!")

@client.event
async def on_command_error(error, ctx):
	#print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await client.send_message(ctx.message.channel, 'Hey buddy, problems with command arguments, they are not')
	elif isinstance(error, commands.BadArgument):
		await client.send_message(ctx.message.channel, 'Hey buddy, problems with command arguments, they are not')
	elif isinstance(error, commands.BadArgument):
		await client.send_message(ctx.message.channel, 'Hey buddy, problems with command arguments, they are not')
##################################################################

#music
##################################################################

@client.command(pass_context=True)
async def mus(ctx, arg):
	if not hasattr(mus, 'mus_player'):
		voice = await client.join_voice_channel(get_channel(ctx))
		mus.mus_player = voice.create_ffmpeg_player('mus/' + arg)
		mus.mus_player.start()
	while not mus.mus_player.is_done():
		await asyncio.sleep(1)
	await voice.disconnect()

@client.command(pass_context=True)
async def yt(ctx, arg):
	if not hasattr(yt, 'yt_player'):
		voice = await client.join_voice_channel(get_channel(ctx))
		yt.yt_player = await voice.create_ytdl_player(arg)
		yt.yt_player.start()
		print(yt.yt_player.title)
	while not yt.yt_player.is_done():
		await asyncio.sleep(1)
	#await yt.yt_player.stop()
	await voice.disconnect()

@client.command(pass_context=True)
async def down_yt(ctx, arg):
	print(config['PATH'] + 'download_yt/',)
	ydl_opts = {
	'format': 'bestaudio/best', 
	'extractaudio' : True,     
	'outtmpl': config['PATH'] + '/download_yt/%(title)s.mp3',   
	'noplaylist' : True,
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([arg])
	channel = get_channel(ctx)
	arr_names = glob.glob(config['PATH'] +"/download_yt/*")
	for name in arr_names:
		await client.send_file(channel, name)
	print (' \n title       : %s' %(meta['title']))


@client.command(pass_context=True)
async def mus_q():
	arr_names = glob.glob(config['PATH'] + "/mus/*.mp3")
	arr_clear_names = []
	for x in arr_names:
		x = os.path.basename(x)
		arr_clear_names.append(x)
	await client.say('Command format: "?mus file" \nThe following files are available on the server: ' + (', '.join(arr_clear_names)) )

@client.command(pass_context=True)
async def mus_pause(ctx):
	if hasattr(mus, 'mus_player'):
		if mus.mus_player.is_playing():
			mus.mus_player.pause()
			await client.send_message(ctx.message.channel, ' Пауза')
	if hasattr(yt, 'yt_player'):
		if yt.yt_player.is_playing():
			yt.yt_player.pause()
			await client.send_message(ctx.message.channel, yt.yt_player.title + ' Пауза')

@client.command(pass_context=True)
async def mus_resume(ctx):
	if hasattr(mus, 'mus_player'):
		if not mus.mus_player.is_playing():
			mus.mus_player.resume()
			await client.send_message(ctx.message.channel, ' Продолжение')
	if hasattr(yt, 'yt_player'):
		if not yt.yt_player.is_playing():
			yt.yt_player.resume()
			await client.send_message(ctx.message.channel, yt.yt_player.title + ' Продолжение')

@client.command(pass_context=True)
async def mus_stop(ctx):
	if hasattr(mus, 'mus_player'):
		if mus.mus_player.is_playing():
			mus.mus_player.stop()
			await voice.disconnect()
			await client.send_message(ctx.message.channel, ' Продолжение')
	if hasattr(yt, 'yt_player'):
		if yt.yt_player.is_playing():
			yt.yt_player.stop()
			await voice.disconnect()
			await client.send_message(ctx.message.channel, yt.yt_player.title + ' Продолжение')

##########################################################

#news yandex
##################################################################
@client.command(pass_context=True)
async def news_msk(self):
    all_news = feedparser.parse('https://news.yandex.ru/Moscow/index.rss')#добавить проверку еси вернётся пустой результат!!
    #all_news = feedparser.parse('https://geektimes.ru/rss/hubs/all/')
    d = {}
    count = 0
    for news in all_news.entries:
        d["news_msk#" + str(count) ] = {"Title" : news.title, "Link" : news.link}
        count = count + 1
    count = 0
    for count in range(len(all_news)): #сделать счетчик на количество новостей в словаре!!
       	await client.say(d['news_msk#'+ str(count)]['Title'] + '\n' + short_links(d['news_msk#' + str(count)]['Link']) + '\n')
       	count = count + 1
    d.clear()
    count = 0
    all_news = None

@client.command(pass_context=True)
async def news_found(self, arg):
	news = {}
	count = 1
	if 'RSS_FEED' not in config:
		await client.say('The rss list is not specified in the configuration file.')
		return 1	
	news = news_search(arg)
	if (len(news) == 0) or (news == 1):
		await client.say('News on request yet, please try again later! Or, specify the word to search for.')
		return 0
	await client.say('__Всего новостей: ' + str(len(news)) + '__')
	for count in range(len(news)):
		await client.say(news['news#'+ str(count)]['Title'] + '\n' +
			short_links(news['news#' + str(count)]['Link']) + '\n')
		count = count + 1
	news = None

def news_search(text):
	news_found= {}
	count = 0
	for feed in config['RSS_FEED']:
		all_news = feedparser.parse(feed)
		if all_news.bozo == 1:
			return 1
		for news in all_news.entries:
			if (news.summary.find(text) != -1) or (news.title.find(text) != -1):
				news_found["news#" + str(count) ] = {"Title" : news.title, "Link" : news.link}
				count = count + 1
	count = 0
	return news_found

def short_links(link):
	if 'RSS_FEED' in config:
		r = requests.post('https://www.googleapis.com/urlshortener/v1/url?key=' + config['GOOGLE_TOKEN'], json={"longUrl": link})
		if r.status_code == 200:
			req_json = r.json()
			return req_json['id']
		else:
			return link
	else:
		return link

#news yandex
##################################################################

# output time and weather
##################################################################
def header():
	headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
	return headers


@client.command(pass_context=True)
async def timeLS(ctx):
	url = 'https://time.is/Las_Vegas'
	r = requests.get(url, headers = header())
	if r.status_code == 200:
		html = r.text
		soup = BeautifulSoup(html, "html.parser")
		time = soup.find('div', {'id': 'twd'})
		date = soup.find('div', {'id': 'dd'})
		time = time.string
		date = date.string
		data_weather = weather("Las Vegas, US")
	else:
		time = datetime.now()
		data_weather = weather("Las Vegas, US")
		time = time + timedelta(hours = -11)	
		time = time.strftime('%y-%m-%d %H:%M:%S')
		date = ''
	await client.say("Local time in Las Vegas: " + time + ', ' + date)
	if data_weather != 1:
		await client.say("Weather in Las Vegas: " + '\n' + 
			"conditions:" + data_weather['weather'][0]['description'] + '\n' +
			"temp:" + repr(data_weather['main']['temp']) + '\n' + 
			"temp_min:" + repr(data_weather['main']['temp_min']) + '\n' + 
			"temp_max:" + repr(data_weather['main']['temp_max']) + '\n')
	else:
		await client.say("The weather is not yet available" )

@client.command(pass_context=True)
async def timeM(ctx):
	url = 'https://time.is/Moscow'
	r = requests.get(url, headers = header())
	if r.status_code == 200:
		html = r.text
		soup = BeautifulSoup(html, "html.parser")
		time = soup.find('div', {'id': 'twd'})
		date = soup.find('div', {'id': 'dd'})
		time = time.string
		date = date.string
		data_weather = weather("Moscow, RU")
	else:
		time = datetime.now()
		data_weather = weather("Las Vegas, US")
		time = time + timedelta(hours = -11)	
		time = time.strftime('%y-%m-%d %H:%M:%S')
		date = ''
	await client.say("Local time in Moscow: " + time + ', ' + date)
	if data_weather != 1:
		await client.say("Weather in Moscow: " + '\n' + 
			"conditions:" + data_weather['weather'][0]['description'] + '\n' +
			"temp:" + repr(data_weather['main']['temp']) + '\n' + 
			"temp_min:" + repr(data_weather['main']['temp_min']) + '\n' + 
			"temp_max:" + repr(data_weather['main']['temp_max']) + '\n')
	else:
		await client.say("The weather is not yet available" )

##################################################################

@client.event
async def wait_until_login():
    await client.change_presence(game=discord.Game(name='something goes here'))

#weather
##################################################################
def weather(city):
	s_city = city
	city_id = 0
	appid = "521a0d5a231883a557b7f6ae9146fa85"
	try:
		res = requests.get("http://api.openweathermap.org/data/2.5/find",params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
		data = res.json()
		cities = ["{} ({})".format(d['name'], d['sys']['country'])
              	for d in data['list']]
		print("city:", cities)
		city_id = data['list'][0]['id']
		print('city_id=', city_id)
	except Exception as e:
		print("Exception (find):", e)
		return 1
		pass
	try:
		res = requests.get("http://api.openweathermap.org/data/2.5/weather",
						params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
		data = res.json()
		#print("conditions:", data['weather'][0]['description'])
		#print("temp:", data['main']['temp'])
		#print("temp_min:", data['main']['temp_min'])
		#print("temp_max:", data['main']['temp_max'])
	except Exception as e:
		print("Exception (weather):", e)
		return 1
	return data
##################################################################


##################################################################
def get_channel(ctx):
	channel = ctx.message.author.voice.voice_channel
	return channel

@client.command(pass_context=True)
async def close(ctx):
	await client.close()


##################################################################	

client.run(config['BOT_TOKEN'])


