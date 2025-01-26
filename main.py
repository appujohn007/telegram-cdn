from pyrogram import Client, filters

# Bot Configuration
API_ID = 10471716  # Replace with your API ID
API_HASH = "f8a1b21a13af154596e2ff5bed164860"  # Replace with your API HASH
BOT_TOKEN = "6916875347:AAGo2IamTLCK4fhB5wPzAZFhppJN6GWaFAc"  # Replace with your bot token

# Initialize Pyrogram Client (Fully Synchronous)
bot = Client("GetFileURLBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.document | filters.video | filters.audio | filters.photo)
def get_file_url(client, message):
    """Handles incoming files and generates a direct download URL"""
    try:
        # Get the correct file object
        file = message.document or message.video or message.audio or (message.photo[-1] if message.photo else None)

        if not file:
            message.reply_text("❌ No valid file found!")
            return

        file_id = file.file_id
        print(f"📂 File ID: {file_id}")

        # Fully synchronous get_file()
        file_info = client.get_file(file_id)  # No 'await' needed
        file_path = file_info.file_path

        # Construct direct download URL
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # Send the file URL
        message.reply_text(f"📥 **Download Link:**\n{file_url}")

    except Exception as e:
        message.reply_text(f"❌ Error: {e}")
        print(f"Error: {e}")

# Run the bot
if __name__ == "__main__":
    bot.run()
