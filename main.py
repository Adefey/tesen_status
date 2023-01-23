import random
import schedule
import time
from datetime import datetime, date, timezone
import pytz
import json
import requests
import logging
logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="[%(asctime)s] %(levelname)s - %(message)s",
)
CONFIG_PATH = "config.json"


def get_time_status(**kwargs):

    def get_time_of_day_with_description(hour):
        hourr = 0
        hour_word = "часов"
        time_of_day = ""

        if hour < 6 or hour > 21:
            time_of_day = "ночи"
        elif 5 < hour < 12:
            time_of_day = "утра"
        elif 11 < hour < 18:
            time_of_day = "дня"
        elif 17 < hour < 22:
            time_of_day = "вечера"
        if hour < 1:
            hourr = 12
        elif hour > 12:
            hourr = hour - 12

        if hourr == 1:
            hour_word = "час"
        elif 1 < hourr < 5:
            hour_word = "часа"

        return f"{hourr} {hour_word} {time_of_day}"

    time_tmp = datetime.now()
    if time_tmp.minute == 0:
        time_res = f"В Москве {get_time_of_day_with_description(time_tmp.hour)}"
    else:
        time_res = "В Москве: " + time_tmp.strftime("%H:%M")
    dict_clock = {"3": "3⃣", "4": "4⃣", "5": "5⃣", "6": "6⃣", "7": "7⃣",
                  "8": "8⃣", "9": "9⃣", "0": "0⃣", "1": "1⃣", "2": "2⃣"}
    for old, new in dict_clock.items():
        time_res = time_res.replace(old, new)
    return time_res


def get_year_status(**kwargs):
    timenow = datetime.now()
    current_year = timenow.year
    unixtime_now = time.mktime(timenow.timetuple())
    unixtime_year_start = time.mktime(date(current_year, 1, 1).timetuple())
    passed_time = unixtime_now - unixtime_year_start
    year_time_value = time.mktime(
        date(current_year + 1, 1, 1).timetuple()) - unixtime_year_start
    percent = (passed_time / year_time_value * 100).__round__(3)
    result_string = f"{current_year} прошел на {percent}%"
    if (percent < 0.6):
        result_string = f"{current_year-1} прошел на 100.00%"
    return result_string


def get_love_days_status(**kwargs):

    def get_random_emoji():
        emojies = ["😁", "😗", "🤥", "👊", "😻", "👅", "💚", "🐍", "🐅", "🐦", "🐸", "🐾", "🌍", "🦊", "🦆", "🍠", "🍻", "🍺", "🍹",
                   "🥝", "🍰", "🍯", "🍩", "🍎", "🍏", "🍇", "🍆", "⚾", "🌟", "🎈", "🎄", "🎩", "🎁", "👑", "🎺", "🎻", "👞", "💻", "🔆"]
        return random.choice(emojies)

    love_start_date = datetime(2022, 12, 11, 2, 45, 0)
    timenow = datetime.now()
    passed_time = timenow - love_start_date
    passed_days = passed_time.days
    return f"{get_random_emoji()} {passed_days} дн."


def get_motd_status(**kwargs):
    motds = ["Man. Nature. Technology.",
             "A world not of my making, yet a world of my design.",
             "God. Demon. Machine.",
             "The cloud is no longer harmful",
             "Fully self-hosted", ]
    motd = random.choice(motds)
    return motd


def get_steam_status(**kwargs):
    name = kwargs["name"]
    steam_html_page = requests.get(
        f"https://steamcommunity.com/id/{name}/").text
    online_status = steam_html_page[steam_html_page.find(
        "profile_in_game_header") + 34:steam_html_page.find(
        "profile_in_game_header") + 100]
    online_status = online_status[:online_status.find("<")]
    if online_status == "Online":
        online_status = "✅ В сети"
    if online_status == "Offline":
        online_status = "⛔ Оффлайн"
    if online_status == "In-Game":
        online_status = "🎮 "
        game_name = steam_html_page[steam_html_page.find(
            "profile_in_game_name") + 22:steam_html_page.find(
            "profile_in_game_name") + 100]
        game_name = game_name[:game_name.find("<")]
        known_game_shortcuts = {"Grand Theft Auto V": "GTA V",
                                "Counter-Strike: Global Offensive": "CS:GO"}
        if game_name in known_game_shortcuts:
            game_name = known_game_shortcuts[game_name]
        online_status += game_name
    return f"Steam: {online_status}"


def set_status(token, version, text):
    params = {"access_token": token, "v": version, "text": text}
    try:
        response = requests.get(
            f"https://api.vk.com/method/status.set", params=params)
    except Exception as e:
        logging.error(f"{e}")
        return None
    logging.info("Request fulfilled")
    return response.json()


def main():
    response_scheme = {
        "time": get_time_status, "year": get_year_status, "love_days": get_love_days_status, "motd": get_motd_status, "steam": get_steam_status}
    with open(CONFIG_PATH, "r", encoding="UTF-8") as file:
        config = json.load(file)
    vkapi_version = config["vkapi_version"]
    for person in config["persons"]:
        statuses = [response_scheme[data](
            name=person["name"]) for data in person["display_data"]]
        status_string = " | ".join(statuses)
        logging.info(f"Made a status for {person['name']}: {status_string}")
        token = person["vk_token"]
        set_status(token, vkapi_version, status_string)


if __name__ == "__main__":
    schedule.every(5).seconds.do(main)
    while 1:
        schedule.run_pending()
        time.sleep(5)
