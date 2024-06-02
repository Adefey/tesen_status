# Автоматическое обновление статуса в ВК

# Что умеет?

Эта программа использует VK access token и все остальные данные, поданные в конфиг чтобы:

- `time` Красиво вывести время
- `year` Красиво вывести процент, на сколько прошел год
- `love_days` Вывести, сколько времени прошло с _особой_ даты ~~(свою дату меняйте сами в исходниках, мне лень)~~
- `motd` Вывести сообщение дня
- `steam` Показать статус стима
- `last_message_status` Показать, от кого и когда было последнее сообщение

# Как создать конфиг?

В конфиге хранится глобально версия VK API и список пользователей, которым нужно ставить статус.

Поля пользователей:

- `name` Ник в стиме
- `vk_token` VK access_token с доступом к статусу
- `display_data` Список информации на вывод
- `mc_server_ip` Адрес своего сервера Minecraft
- `mc_server_name` Название своего сервера Minecraft
- `motds` Список сообщений дня

# Пример конфига и использования

```
{
  "vkapi_version": "5.236",
  "persons": [
    {
      "name": "adefey",
      "vk_token": "vk1.a..."
      "display_data": ["time", "year", "love_days", "motd", "steam", "last_message_status"],
      "mc_server_ip": "mc.adefe.xyz",
      "mc_server_name": "BMSTUCraft",
      "motds": [
        "Man. Nature. Technology",
        "A world not of my making, yet a world of my design",
        "God. Demon. Machine."
    }
  ]
}
```

```
python main.py
```

Можно вызывать каждую минуту по cron'y
