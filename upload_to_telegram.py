import requests

# Fetch the raw text of whatever script you need
script_url = "https://raw.githubusercontent.com/AhnafTouseef/Colab-Tools/main/colab_file_naviagator.py"
remote_code = requests.get(script_url).text

# Run it immediately into the cell's memory
exec(remote_code)

import subprocess
import asyncio
import nest_asyncio
from telethon import TelegramClient

# Patch the notebook event loop
nest_asyncio.apply()

#copy session tocken
try:
  copy("/content/drive/MyDrive/session_name.session", "/content")
except Exception:
  subprocess.Popen(["gdown", r"https://drive.google.com/uc?id=1WbAFyd9YEF9trypNFFbwQNV5ehIGtTHQ"])
  pass

# Your permanent API keys
API_ID = 32384699         
API_HASH = 'a1c54b28ce028a23b5a1c379620c33f2'


class TelegramUploader:

    def __init__(self, group):
        self.group = group
        self.client = None
        self.entity = None

    async def __aenter__(self):
        self.client = TelegramClient(
            'session_name', API_ID, API_HASH
        )

        await self.client.start()

        # Resolve the destination only once
        if isinstance(self.group, str) and (
            't.me/+' in self.group or 'joinchat/' in self.group
        ):
            invite_hash = self.group.rstrip('/').split('/')[-1]
            invite_hash = invite_hash.lstrip('+')

            result = await self.client(
                CheckChatInviteRequest(invite_hash)
            )

            if isinstance(result, ChatInviteAlready):
                self.entity = result.chat
            else:
                raise ValueError(
                    "Your account is not already a member of this group."
                )
        else:
            self.entity = await self.client.get_entity(self.group)

        print("Telegram connected.")
        print(f"Destination: {getattr(self.entity, 'title', self.entity)}")

        return self

    async def upload(self, file):
        try:
            print(f"Starting upload: {file}")

            await self.client.send_file(
                self.entity,
                file,
                supports_streaming=True
            )

            print(f"Successfully uploaded: {file}\n")

        except FloodWaitError as e:
            print(
                f"Telegram FloodWait: {e.seconds} seconds. "
                "Stopping uploads."
            )
            raise

    async def upload_album(self, files):
        for i in range(0, len(files), 10):
            batch = files[i:i + 10]

            await self.client.send_file(
                self.entity,
                batch,
                supports_streaming=True
            )

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.client:
            await self.client.disconnect()

        print("Telegram disconnected.")


print("""
Usage:

async with TelegramUploader(group) as uploader:
    await uploader.upload(file)
""")
