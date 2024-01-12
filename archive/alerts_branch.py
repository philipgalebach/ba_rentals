# prior BA rentals telegram bot: https://github.com/rodrigouroz/housing_scrapper
# tutorial: https://www.youtube.com/watch?v=vZtm1wuA2yc

import logging
import random
import asyncio
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Your bot's token and chat ID
TOKEN = '6826059877:AAFZfrEWXiu05FCrYRDN15xUQIxT6EcsdRs'
CHAT_ID = '464221960'

# Your message
MESSAGE = 'Hello from your bot!'

# The condition you want to evaluate
condition = 'bet'  # Replace with your actual condition

async def send_message(token, chat_id, message):
    # Initialize bot with token
    bot = telegram.Bot(token)
    
    # Send a message to a user
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == '__main__':
    # Set up the logging module to output diagnostic information
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Check the condition
    if condition == 'bet':  # Replace this with your actual condition check
        # Create an asyncio event loop
        loop = asyncio.get_event_loop()
        
        # Send the message
        loop.run_until_complete(send_message(TOKEN, CHAT_ID, MESSAGE))
# This script sets up a basic bot that responds to the /start command by sending 
    # "Hello from your bot!" to the specified chat. It uses the telegram.ext module to handle commands and messages asynchronously.
