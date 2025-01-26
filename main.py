import telebot
import requests
import os

# Bot Configuration
BOT_TOKEN = "6916875347:AAGo2IamTLCK4fhB5wPzAZFhppJN6GWaFAc"  # Replace with your bot token

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def download_file(url, file_name):
    """Download file with progress tracking."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(file_name, 'wb') as file:
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                progress = (downloaded_size / total_size) * 100 if total_size else 0
                print(f"\rDownloading: {progress:.2f}%", end='')

    print("\nDownload Complete:", file_name)

@bot.message_handler(content_types=['photo', 'document', 'video', 'audio'])
def handle_files(message):
    """Handles incoming files of any type."""
    try:
        chat_id = message.chat.id
        file_id = None

        # Determine the file type and extract the file ID
        if message.photo:
            file_id = message.photo[-1].file_id  # Highest resolution photo
        elif message.document:
            file_id = message.document.file_id
        elif message.video:
            file_id = message.video.file_id
        elif message.audio:
            file_id = message.audio.file_id

        if not file_id:
            bot.send_message(chat_id, "Could not retrieve the file.")
            return

        # Get file information
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Construct the direct file URL
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        print("File URL:", file_url)

        # Download the file
        file_name = os.path.basename(file_path)
        download_file(file_url, file_name)

        bot.send_message(chat_id, "File downloaded successfully!")
    except Exception as e:
        print("Error:", str(e))
        bot.send_message(chat_id, "An error occurred while processing the file.")

# Run the bot
bot.polling(none_stop=True)
