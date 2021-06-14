import logging
import aiogram as tl
from aiogram import asyncio
import time

from bs4 import BeautifulSoup as bs
import requests

logging.basicConfig(level=logging.INFO)

bot = tl.Bot(token = "put your token here")
dp = tl.Dispatcher(bot)

def parse():
    Url = 'https://stopgame.ru/review/new'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.01) AppleWebKit/531.3.3 (KHTML, like Gecko) Version/4.1 Safari/531.3.3'}

    response = requests.get(Url, headers=HEADERS)
    soup = bs(response.content, 'html.parser')
    items = soup.findAll('div', class_='item article-summary')
    info = []

    for i in items:
        name_div = i.find('div', class_="caption caption-bold")
        
        Url = "https://stopgame.ru" + name_div.find('a').attrs["href"]
        response = requests.get(Url, headers=HEADERS)
        soup = bs(response.content, 'html.parser')
        grade = ""
        if soup.findAll('div', class_='score score-1') != []:
            grade = "Мусор👎"
        if soup.findAll('div', class_='score score-2') != []:
            grade = "Проходняк😐"
        if soup.findAll('div', class_='score score-3') != []:
            grade = "Похвально👌"
        if soup.findAll('div', class_='score score-4') != []:
            grade = "Изумительно👍"
        spec = ""

        for j in soup.findAll('div', class_='game-spec'):
            spec += j.get_text(strip=True) + "\n"
        info.append([name_div.find('a').get_text(strip=True), name_div.find('a').attrs["href"], grade, spec])
    return info

@dp.message_handler(commands=['start_channel'])
async def run(message : tl.types.message):
    old = parse()
    new = parse()
    while 1:
        await asyncio.sleep(5)
        old = new
        print("Good")
        new = parse()
        if old != new:
            await bot.send_message("@put name of channel here", parse()[0][0] + " \n\n" + parse()[0][2] + " \n\n" + parse()[0][3] + "\n" + "https://stopgame.ru" + parse()[0][1])

if __name__ == '__main__':
    tl.executor.start_polling(dp, skip_updates=True)