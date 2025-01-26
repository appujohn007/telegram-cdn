import telebot
import requests

# Bot Configuration
BOT_TOKEN = "6916875347:AAGo2IamTLCK4fhB5wPzAZFhppJN6GWaFAc"  # Replace with your bot token
IMG_BB_API_KEY = "your_imgbb_api_key"  # Replace with your ImgBB API Key

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['photo'])
def get_file_url(message):
    """Handles incoming images and generates a direct download URL"""
    try:
        chat_id = message.chat.id
        photo = message.photo[-1]  # Get the highest resolution photo
        file_id = photo.file_id

        # Get file info synchronously
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Construct direct file URL
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # Upload image to ImgBB
        img_bb_url = f"https://api.imgbb.com/1/upload?key={IMG_BB_API_KEY}&image={file_url}"
        response = requests.get(img_bb_url).json()

        if "data" in response and "url" in response["data"]:
            img_url = response["data"]["url"]
            bot.send_chat_action(chat_id, "upload_photo")
            bot.send_message(chat_id, f"☑️ Image Uploaded Successfully\n🔗 URL: {img_url}")
        else:
            bot.send_message(chat_id, "❌ Upload failed. Please try again.")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")
        print(f"Error: {e}")

# Run the bot
bot.polling(none_stop=True)
