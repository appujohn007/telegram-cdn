from pyrogram import Client, filters
from pyrogram.raw.functions.upload import GetCdnFile
from pyrogram.raw.types import InputDocumentFileLocation

# Your API ID and API Hash
API_ID = "10471716"
API_HASH = "f8a1b21a13af154596e2ff5bed164860"
BOT_TOKEN = "6916875347:AAGo2IamTLCK4fhB5wPzAZFhppJN6GWaFAc"

app = Client("cdn_url_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


from pyrogram import Client, filters
from pyrogram.types import Message

@app.on_message(filters.media & filters.private)
async def get_cdn_url(client: Client, msg: Message):
    if msg.document:
        try:
            # Extract file details directly from the message
            document = msg.document
            file_id = document.file_id

            # Retrieve file metadata using get_file() and ensure proper handling
            file = await client.get_file(file_id)

            # If the file has file_ref and access_hash, generate a CDN URL
            access_hash = file.access_hash
            file_ref = file.file_ref

            # Now you have access_hash and file_ref
            # Example of generating CDN URL
            # (If pyrogram supports directly getting the CDN URL, this can be done more easily with their method)
            file_url = f"https://api.telegram.org/file/bot{client.token}/{file.file_path}"

            await msg.reply(f"CDN URL:\n{file_url}")
        except Exception as e:
            await msg.reply(f"Error: {e}")
    else:
        await msg.reply("Please send a document or media file to retrieve the CDN URL.")
        

# Start the bot
if __name__ == "__main__":
    app.run()
