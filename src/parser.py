import logging
import os

from bs4 import BeautifulSoup
import requests

from dotenv import load_dotenv

from src.save import update_username, update_recent_game, update_games, update_last_2_week


class AccountParser:
    def __init__(self):
        load_dotenv()
        rec = requests.get(os.getenv("USER_LINK"))

        self.soup = BeautifulSoup(rec.text, 'html.parser')


    def update(self):
        load_dotenv()

        logging.info("Updating userdata")

        rec = requests.get(os.getenv("USER_LINK"))

        self.soup = BeautifulSoup(rec.text, 'html.parser')

        self.__parse_user_data()
        self.__parse_last_2_week()
        self.__parse_game_activity()


    def __parse_user_data(self):
        username = self.soup.find('span', class_='actual_persona_name')

        update_username(username.text)


    def __parse_last_2_week(self):
        last_2_week = self.soup.find('div', class_='recentgame_quicklinks recentgame_recentplaytime')
        last_2_week = last_2_week.div.text.split()[0]

        update_last_2_week(last_2_week)


    def __parse_game_activity(self):
        all_recents = self.soup.find_all('div', class_='recent_game')
        recent_activity = []

        for block in all_recents:
            game = block.find('a', class_='whiteLink')
            time = block.find('div', class_='game_info_details')

            lines = time.get_text(separator='\n', strip=True).split('\n')
            hours_str = lines[0]
            hours = hours_str.split(' ')[0]

            recent_activity.append({game.text: hours})

        update_recent_game(recent_activity[0])
        update_games(recent_activity)


ap = AccountParser()
ap.update()
