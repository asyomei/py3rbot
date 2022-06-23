from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.methods.utilities.idle import idle


class PythonBot:
    def __init__(self, api_id: str, api_hash: str, bot_token: str) -> None:
        self._app = Client(
            type(self).__name__,
            api_id, api_hash,
            bot_token=bot_token,
            parse_mode=ParseMode.DISABLED,
            in_memory=True,
        )
        self.__registered = False


    def run(self) -> None:
        self.__register_handlers()

        app = self._app

        async def _run() -> None:
            async with app:
                print("Bot started")
                await idle()
            print("Goodbye!")

        app.run(_run())


    def __register_handlers(self) -> None:
        from ..handlers import handlers

        if self.__registered:
            return

        app = self._app
        for handler in handlers:
            app.add_handler(*handler)

        self.__registered = True
