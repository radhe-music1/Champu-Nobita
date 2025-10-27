import asyncio
import uvloop
import pyrogram
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
import config
from ..logging import LOGGER

# ✅ Safe uvloop initialization (fixes "no current event loop" error)
try:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass


class ChampuBot(Client):
    def __init__(self):
        LOGGER(__name__).info("🟢 Starting Champu Bot...")
        super().__init__(
            "ChampuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = get_me.first_name + (f" {get_me.last_name}" if get_me.last_name else "")
        self.mention = get_me.mention

        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ๏",
                        url=f"https://t.me/{self.username}?startgroup=true",
                    )
                ]
            ]
        )

        # 🧾 Send log to LOGGER_ID group
        if config.LOGGER_ID:
            try:
                await self.send_photo(
                    config.LOGGER_ID,
                    photo=config.START_IMG_URL,
                    caption=(
                        f"╔════❰𝗪𝗘𝗟𝗖𝗢𝗠𝗘❱════❍⊱❁۪۪\n║\n"
                        f"║┣⪼🥀ʙᴏᴛ sᴛᴀʀᴛᴇᴅ🎉\n"
                        f"║┣⪼ {self.name}\n"
                        f"║┣⪼🎈ɪᴅ:- `{self.id}` \n"
                        f"║┣⪼🎄@{self.username} \n"
                        f"║┣⪼💖ᴛʜᴀɴᴋs ғᴏʀ ᴜsɪɴɢ😍\n║\n╚════════════════❍⊱❁"
                    ),
                    reply_markup=button,
                )
            except ChatWriteForbidden:
                LOGGER(__name__).error("🚫 Bot cannot write to the log group. Please check permissions.")
            except Exception as e:
                LOGGER(__name__).error(f"⚠️ Error sending log message: {e}")
        else:
            LOGGER(__name__).warning("⚠️ LOGGER_ID is not set, skipping log group notifications.")

        # ⚙️ Set bot commands
        if getattr(config, "SET_CMDS", True):
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("start", "Start the bot"),
                        BotCommand("help", "Show help menu"),
                        BotCommand("ping", "Check if bot is alive"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    [
                        BotCommand("play", "Start playing requested song"),
                        BotCommand("stop", "Stop the current song"),
                        BotCommand("pause", "Pause the current song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("queue", "Check song queue"),
                        BotCommand("skip", "Skip current song"),
                        BotCommand("volume", "Adjust volume"),
                        BotCommand("lyrics", "Get lyrics of the song"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    [
                        BotCommand("start", "✨ Start the bot"),
                        BotCommand("ping", "🍁 Check ping"),
                        BotCommand("help", "🥺 Get help"),
                        BotCommand("play", "🎶 Play a song"),
                        BotCommand("pause", "⏸ Pause song"),
                        BotCommand("resume", "▶ Resume song"),
                        BotCommand("stop", "⛔ Stop music"),
                        BotCommand("queue", "🎧 Show queue"),
                        BotCommand("lyrics", "🎵 Get lyrics"),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).error(f"⚠️ Failed to set bot commands: {e}")

        # 👮‍♂️ Check admin status in logger group
        if config.LOGGER_ID:
            try:
                chat_member = await self.get_chat_member(config.LOGGER_ID, self.id)
                if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error("❌ Please promote bot as admin in LOGGER group.")
            except Exception as e:
                LOGGER(__name__).error(f"⚠️ Error while checking bot status: {e}")

        LOGGER(__name__).info(f"✅ Champu-Nobita Bot started successfully as {self.name}")
