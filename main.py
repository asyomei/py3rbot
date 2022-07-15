from dotenv import dotenv_values

from py3rbot import PythonBot


env = dotenv_values()


def getenv(option: str) -> str:
    value = env.get(option)
    if value is None:
        raise KeyError(f"Not found '{value}' in .env")
    return value


def main() -> None:
    api_id = getenv("API_ID")
    api_hash = getenv("API_HASH")
    bot_token = getenv("BOT_TOKEN")

    bot = PythonBot(api_id, api_hash, bot_token)
    bot.run()


if __name__ == "__main__":
    import os

    old_cwd = os.getcwd()
    new_cwd = os.path.dirname(os.path.realpath(__file__))

    try:
        os.chdir(new_cwd)
        main()
    finally:
        os.chdir(old_cwd)
