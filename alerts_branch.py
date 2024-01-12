# prior BA rentals telegram bot: https://github.com/rodrigouroz/housing_scrapper
# tutorial: https://www.youtube.com/watch?v=vZtm1wuA2yc

import logging
import random
import asyncio
import telegram
import pandas as pd
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Your bot's token and chat ID
TOKEN = '6826059877:AAFZfrEWXiu05FCrYRDN15xUQIxT6EcsdRs'
CHAT_ID = '464221960'

# Function to read the first row of the CSV and format the message
def format_message_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    data = df.iterrows()
    header = df.columns.tolist()
    messages = []
    for _, row in data:
        message = "\n".join([f"{col}: {row[col]}" for col in header])
        messages.append(message)
    return messages

async def send_message(token, chat_id, message):
    # Initialize bot with token
    bot = telegram.Bot(token)
    
    # Send a message to a user
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == '__main__':
    # Set up the logging module to output diagnostic information
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Create an asyncio event loop
    loop = asyncio.get_event_loop()
    
    # Format the messages from the CSV file
    MESSAGES = format_message_from_csv('listings_clean.csv')

    # Send the messages
    for MESSAGE in MESSAGES:
        loop.run_until_complete(send_message(TOKEN, CHAT_ID, MESSAGE))
