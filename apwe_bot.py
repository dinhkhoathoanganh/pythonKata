from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TOKEN = "1092583779:AAH5twuJGIo3MXmVUM3aL0SF2p0q5WdbOm4"


def start(update, context):
    welcome_line = "Hello from APWE group!"
    update.message.reply_text(welcome_line)    # adds the reply only to the specific chat where the /start command was sent.

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))  # execute function start when the user sends "/start"

    dispatcher.add_handler(MessageHandler(Filters.text, echo))  # Filters.text is to handle texts only, because the user can send other things such as gif, stickers, etc

    updater.start_polling() # start polling for any Telegram updates
    updater.idle()  # block the script until user sends a command to stop


if __name__ == '__main__':
    main()