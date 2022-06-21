from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.methods.utilities.idle import idle

from ..handlers import handlers


class PythonBot:
    def __init__(self, api_id: str, api_hash: str, bot_token: str) -> None:
        self._app = app = Client(
            type(self).__name__,
            api_id, api_hash,
            bot_token=bot_token,
            parse_mode=ParseMode.DISABLED,
            in_memory=True,
            ipv6=True,
        )
        for handler in handlers:
            app.add_handler(*handler)


    def run(self) -> None:
        app = self._app

        async def _run() -> None:
            async with app:
                print("Bot started")
                await idle()
            print("Goodbye!")

        app.run(_run())
