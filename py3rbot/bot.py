class PythonBot:
    def __init__(self, api_id: str, api_hash: str, bot_token: str) -> None:
        from pyrogram.client import Client
        from pyrogram.enums.parse_mode import ParseMode

        self.app = Client(
            "PythonBot",
            api_id, api_hash,
            bot_token=bot_token,
            parse_mode=ParseMode.DISABLED,
            plugins=dict(root="py3rbot.plugins"),
            in_memory=True,
        )


    def run(self) -> None:
        from pyrogram.methods.utilities.idle import idle

        async def _run() -> None:
            async with self.app:
                print("Bot started")
                await idle()
            print("Goodbye!")

        self.app.run(_run())
