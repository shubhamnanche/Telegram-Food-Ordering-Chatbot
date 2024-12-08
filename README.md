# Telegram Food Ordering Chatbot

### Steps to follow:

- `git clone https://github.com/shubhamnanche/Telegram-Food-Ordering-Chatbot.git`
- Go to Telegram app and create a new _Chat Bot_ alongside generating a token from `@BotFather` (Follow steps online)
- Create `/start`, `/help` and optionally a `/custom` command using `@BotFather` or navigating to your _Bot_'s settings
- Create a file `.env` in the root directory of the project and paste the token generated in the above steps `BOT_TOKEN=<generated-token>` in it.
- Install requirements by running `pip install -r requirements.txt` in the project root directory inside terminal, for installing the required dependencies.
- Run `python main.py` in the project root directory inside terminal.
- Now, select (or write in chat) `/start` from the command menu in your _Bot_'s chat window.
- Done, the _Telegram Bot_ can now answer to your orders!