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
from pyrogram.raw import GetCdnFile, InputDocumentFileLocation

@app.on_message(filters.media & filters.private)
async def get_cdn_url(client: Client, msg: Message):
    if msg.document:
        try:
            # Extract file details directly from the message
            document = msg.document

            file_id = document.file_id
            file_unique_id = document.file_unique_id
            file_name = document.file_name
            file_size = document.file_size
            mime_type = document.mime_type

            # Use the file_id and file_unique_id to get the CDN URL
            # Request CDN file location
            result = await client.invoke(
                GetCdnFile(
                    location=InputDocumentFileLocation(
                        id=file_id,
                        access_hash=msg.document.access_hash,  # You need to have access_hash for this
                        file_reference=msg.document.file_ref   # You need to ensure file_ref is available
                    ),
                    offset=0,
                    limit=1024  # Specify the chunk size (1024 bytes in this case)
                )
            )

            # Output CDN URL or related information
            if result:
                await msg.reply(f"CDN URL retrieved:\n\n{result.url}")
            else:
                await msg.reply("Failed to retrieve the CDN URL for this file.")
        except Exception as e:
            await msg.reply(f"Error: {e}")
    else:
        await msg.reply("Please send a document or media file to retrieve the CDN URL.")



# Start the bot
if __name__ == "__main__":
    app.run()
