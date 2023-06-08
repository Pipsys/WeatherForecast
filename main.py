import telebot 
from config import TOKEN, API
import requests
import json

bot = telebot.TeleBot(TOKEN)
API = API

@bot.message_handler(commands=['start'])
def start(message):
    hello_msg = f'Привет, {message.from_user.first_name}!\n☁️Чтобы узнать погоду, напиши название своего города и бот выдаст точный прогноз погоды ☁️'
    bot.send_animation(message.chat.id,r'https://gazeta-schekino.ru/upload/iblock/1c3/1c3d6b6dd72630bcd8a364b2cc36208e.gif', caption = hello_msg)
    
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Чтобы узнать прогноз погоды, просто напиши название своего города")

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    data = json.loads(res.text)
    temp = data["main"]["temp"]
    msg_weather=f'На данный момент, погода в городе {city}: {temp}'
    
    image = "/Pictures/Good_weather.png" if temp  > 20.0 else "/Pictures/bad_weather.png"
    file = open("./" + image, 'rb')
    bot.send_photo(message.chat.id, file, caption = msg_weather)

bot.polling(none_stop=True)