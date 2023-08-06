#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

import roomie_bot.expenses.expenses as expenses
from roomie_bot.database.database import Database

from telegram.ext import Updater, CommandHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers.
def start(update, context):
    update.message.reply_text(
        '''
        Hi! I am roomie, a bot with tools to make life easier between roommates.
        \nI can help you tracking your expenses or organizing tasks
        \nFirst, every user should /register (you should have a username set up)
        \n\nSend /help for a list of commands
        '''
    )


def register(update, context):
    if update.effective_user.username is None:
        update.message.reply_text('You need an username to /register'
                                  '\n\nTo set up one go to settings in'
                                  ' telegram and select "username"')
    else:
        db = Database()
        db.register_user(update.effective_user.id, update.effective_user.username)
        db.close()

        update.message.reply_text('Successfully registered with username ' + update.effective_user.username)


def pay(update, context):
    errors = ''

    # Check argument size and format
    if len(context.args) >= 2:
        # Check correct format for money
        if expenses.is_number(context.args[0]):
            money = float(context.args[0])
        else:
            errors += 'Error: {} is not an amount of money\n'.format(context.args[0])

        db = Database()
        # Check payer is registered
        if db.get_username(update.effective_user.id) is None:
            errors += 'Error: You are not registered\n'

        # Check debtors are registered
        debtors_id = []

        for debtor in context.args[1:]:
            userid = db.get_userid(debtor[1:])
            if userid is None:
                errors += 'Error: {} is not registered\n'.format(debtor)
            else:
                debtors_id.append(userid)
        db.close()
    else:
        errors += 'Format: /pay money @debtor1 [@debtor2..]'

    if errors:
        if errors.split()[0] != 'Format:':
            errors += 'Format: /pay money @debtor1 [@debtor2..]'
        update.message.reply_text(errors)
    else:
        expenses.new_payment(update.effective_user.id, update.message.chat_id,
                             money, debtors_id, context.args[1:])

        update.message.reply_text('Payment added succesfully'
                                  '\nCheck new debts with /debts')


def history(update, context):
    history = expenses.get_payments(update.effective_chat.id)

    if history == '':
        update.message.reply_text("No history yet")
    else:
        update.message.reply_text(history)


def debts(update, context):
    debts = expenses.get_debts(update.effective_chat.id)

    if debts == "":
        update.message.reply_text("No debts yet")
    else:
        update.message.reply_text(debts)


def help(update, context):
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Initialize database
    db = Database()
    db.setup()
    db.close()

    # Create the Updater and pass it bot's token.
    TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("pay", pay))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(CommandHandler("debts", debts))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until interrupted
    updater.idle()


if __name__ == '__main__':
    main()
