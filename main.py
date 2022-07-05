import os
import sys

from decouple import config

from py3rbot import PythonBot


def config_str(option: str) -> str:
    return str(config(option, cast=str, default=str()))


def main() -> None:
    api_id = config_str("API_ID")
    api_hash = config_str("API_HASH")
    bot_token = config_str("BOT_TOKEN")

    bot = PythonBot(api_id, api_hash, bot_token)
    bot.run()


if __name__ == "__main__":
    # fix Pyrogram's smart plugins path
    old_cwd = os.getcwd()
    new_cwd = os.path.dirname(os.path.realpath(__file__))
    try:
        os.chdir(new_cwd)
        main()
    finally:
        os.chdir(old_cwd)
