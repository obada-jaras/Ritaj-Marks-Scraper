from utils.config import TELEGRAM_API_TOKEN
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Please enter your student ID (for example 1191234):")
    
    # Wait for user input
    user_id_msg = await context.bot.wait_for(
        'message', 
        check=lambda message: message.chat_id == chat_id and message.text.strip().isdigit()
    )
    user_id = user_id_msg.text
    
    await context.bot.send_message(chat_id=chat_id, text="Please enter your password:")
    
    # Wait for user input
    password_msg = await context.bot.wait_for(
        'message', 
        check=lambda message: message.chat_id == chat_id and message.text.strip().isalnum()
    )
    password = password_msg.text




if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.run_polling()
