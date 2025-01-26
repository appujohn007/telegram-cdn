from pyrogram import Client, filters
from pyrogram.raw.functions.upload import GetCdnFile
from pyrogram.raw.types import InputDocumentFileLocation

# Your API ID and API Hash
API_ID = "10471716"
API_HASH = "f8a1b21a13af154596e2ff5bed164860"
BOT_TOKEN = "6916875347:AAGo2IamTLCK4fhB5wPzAZFhppJN6GWaFAc"

app = Client("cdn_url_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)



@app.on_message(filters.media & filters.private)
async def get_cdn_url(client, msg):
    if msg.document:
        document = msg.document

        try:
            # Fetch file metadata to get access_hash and file_ref
            file = await client.get_file(document.file_id)

            # Retrieve the file_ref and access_hash
            file_ref = file.file_ref
            access_hash = file.access_hash
            file_id = file.file_id
            dc_id = file.dc_id

            # Request CDN file location
            result = await client.invoke(
                GetCdnFile(
                    location=InputDocumentFileLocation(
                        id=file_id,
                        access_hash=access_hash,
                        file_reference=file_ref
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
