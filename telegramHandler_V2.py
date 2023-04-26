import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from threading import Thread

from utils.config import TELEGRAM_API_TOKEN
from utils.validators import is_valid_user_id, is_valid_email
from main import *


# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


number_of_active_bots = 0
def decrement_number_of_active_bots():
    global number_of_active_bots
    number_of_active_bots -= 1



def start(update, context):
    context.user_data.clear()
    ask_for_id(update, context)




def ask_for_id(update, context):
    update.message.reply_text('Please enter your university ID:')
    context.user_data['state'] = 'waiting_for_id'

def get_user_id(update, context):
    user_id = update.message.text
    if is_valid_user_id(user_id):
        context.user_data['user_id'] = user_id
        ask_for_password(update, context)
    else:
        update.message.reply_text(
            'Invalid user ID. Please enter a valid student ID (for example 1191234):')



def ask_for_password(update, context):
    update.message.reply_text('Please enter your Ritaj password:')
    context.user_data['state'] = 'waiting_for_password'

def get_password(update, context):
    password = update.message.text
    context.user_data['password'] = password
    
    ask_for_email(update, context)





def ask_for_email(update, context):
    update.message.reply_text('Please enter your email:')
    context.user_data['state'] = 'waiting_for_email'

def get_email(update, context):
    email = update.message.text
    if is_valid_email(email):
        context.user_data['email'] = email
        starting_bot(update, context)
    else:
        update.message.reply_text(
            "Invalid email. Please enter a valid email address.")





def starting_bot(update, context):
    global number_of_active_bots

    user_id = context.user_data.get('user_id')
    password = context.user_data.get('password')
    email = context.user_data.get('email')

    save_info_to_file(update, user_id, password, email)
    context.user_data['state'] = 'bot_started'
    update.message.reply_text('Bot started!')
    update.message.reply_text('If you want to modify your information, please use /start command.')


    # Create a new thread for the bot
    number_of_active_bots += 1
    chatID = update.message.chat_id
    thread = Thread(target=run_bot, args=(chatID, user_id, password))
    thread.start()



def save_info_to_file(update, user_id, password, email):
    filename = f"{user_id}.txt"
    filepath = os.path.join("users/info", filename)
    if os.path.exists(filepath):
        # File exists, append to it
        with open(filepath, "a") as file:
            file.write(f"\n------\nPassword: {password}\nEmail: {email}")
    else:
        # File doesn't exist, create new file
        with open(filepath, "w") as file:
            file.write(f"Password: {password}\nEmail: {email}")






def handle_message(update, context):
    state = context.user_data.get('state')
    if state == 'waiting_for_id':
        get_user_id(update, context)
    elif state == 'waiting_for_password':
        get_password(update, context)
    elif state == 'waiting_for_email':
        get_email(update, context)


def numberOfUsers(update, context):
    global number_of_active_bots

    if update.message.chat_id != 6123911846:
        update.message.reply_text('You are not authorized to use this command')
        return
    
    else: 
        update.message.reply_text('Number of all users: ' + str(len(os.listdir('users/info'))))
        update.message.reply_text('number of running threads: ' + str(number_of_active_bots))


def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('admin', numberOfUsers))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
