# Report bot for Telegram

This repository contains sources of a small yet rather powerful bot for Telegram, which handles reports from users and passes them to admins. Uses [aiogram](https://github.com/aiogram/aiogram) framework.  
The main goal was to build a bot with no external database needed. Thus, it may lack some features, but hey, it's open source!

#### Screenshots
User reports a message:  
![User reports a message in regular chat](screenshots/users_view.jpg)

Admins take action:  
![Admins get report in a special chat](screenshots/admin_view.jpg)

#### Features
* Handles `/report` command to gather reports from users;  
* Handles `/ro` command to set user "Read-only" and `/textonly` to allow text messages only;
* Removes "user joined" messages;  
* Reacts to short "greetings" messages like "Hey everyone", kindly asking user to proceed to their question or problem directly;  
* Provides a simple interface for admins to choose one of actions on reported message.

#### Requirements
* Python 3.7 and above;  
* Linux is mentioned in the following installation guide, but bot should also work on Windows: no platform-specific code is used;  
* Systemd (you can use it to enable autostart and autorestart).

* Only installed Docker and docker-compose, if you want to launch bot in Docker container.


#### Installation  
1. Go to [@BotFather](https://t.me/telegram), create a new bot, write down its token, add it to your existing group and **make bot an admin**. You also need to give it "Delete messages" permission.  
2. Create a separate chat where report messages will be sent and add all group admins there. Remember: anyone who is in that group may perform actions like "Delete", "Ban" and so on, so be careful.  
3. Clone this repo and `cd` into it;   
4. Create a venv (virtual environment): `python3.7 -m venv venv`;  
5. `source venv/bin/python && pip install aiogram`;  
6. `chmod +x bot.py`;  
7. Copy `config.py.example` to `config.py`, open it and set correct "main" and "reports" chats IDs. To get IDs, add [@ShowJSONbot](https://t.me/showjsonbot) or [@my_id_bot](https://t.me/my_id_bot) to your chats.  
8. Run your bot: `BOT_TOKEN=yourtoken ./bot.py`  

If you want systemd support for autostart and other tasks: open `reportbot.service` file, change relevant options to match yours, enter correct token.  
Now move that file to `/etc/systemd/system` enable it with `systemctl enable reportbot.service` and run it: `systemctl restart reportbot.service`. Easy!


#### Launch in Docker container
1. Go to [@BotFather](https://t.me/telegram), create a new bot, write down its token, add it to your existing group and **make bot an admin**. $
2. Create a separate chat where report messages will be sent and add all group admins there. Remember: anyone who is in that group may perform $
3. Clone this repo and `cd` into it;
4. Copy `config.py.example` to `config.py`, open it and set correct "main" and "reports" chats IDs. To get IDs, add [@ShowJSONbot](https://t.me/showjsonbot) or [@my_id_bot](https://t.me/my_id_bot) to your chats.
5. Copy file `.env_dist` to `.env` and change variable in it.
6. Run your bot by execute `docker-compose up -d` - it build image and launch a container.
