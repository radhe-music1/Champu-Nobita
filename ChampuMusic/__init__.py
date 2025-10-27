import asyncio
from ChampuMusic.core.bot import ChampuBot
from ChampuMusic.core.dir import dirr
from ChampuMusic.core.git import git
from ChampuMusic.core.userbot import Userbot
from ChampuMusic.misc import dbb, heroku, sudo
from .logging import LOGGER
from .platforms import *

# Initialize setup
EMOJIS = [
    "PPLAY_1", "PPLAY_2", "PPLAY_3", "PPLAY_4", "PPLAY_5",
    "PPLAY_6", "PPLAY_7", "PPLAY_8", "PPLAY_9", "PPLAY_10",
    "PPLAY_11", "PPLAY_12", "PPLAY_13", "PPLAY_14", "PPLAY_15",
    "PPLAY_16", "PPLAY_17"
]

dirr()
git()
dbb()
heroku()
sudo()

# Initialize APIs
YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}

# Proper event loop fix for Python 3.10+
async def main():
    app = ChampuBot()
    userbot = Userbot()
    await app.start()
    await userbot.start()
    LOGGER(__name__).info("✅ Champu-Nobita Bot successfully started!")
    await asyncio.get_event_loop().create_future()  # Keeps bot running

if __name__ == "__main__":
    asyncio.run(main())
