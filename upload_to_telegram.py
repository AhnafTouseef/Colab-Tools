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

async def telegram_uploader(group, file):
    """
    Uploads any file (video, pdf, zip, image) to a specified Telegram group without captions.
    
    :param group: The group invite link, username, or numerical chat ID.
    :param file: Absolute or relative system path to the file.
    """
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        print(f"Starting upload for: {file}")
        print("Please wait...")
        
        # Uploads raw media with no caption text
        await client.send_file(
            group, 
            file, 
            supports_streaming=True  # Allows inline video playback
        )
        
        print(f"✅ Successfully uploaded: {file}\n")


# Simply pass the group and the file path
def upload_to_telegram(group, file):
    asyncio.run(telegram_uploader(group, file))

print("Usage: upload_to_telegram(target_group_link, my_media_path)")
