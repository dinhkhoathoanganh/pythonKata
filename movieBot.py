from telegram.ext import Updater, CommandHandler,MessageHandler, Filters
import requests

TOKEN='1273060946:AAEdCklP6dAYfqP0cEjDz8rv3kHSpJt6vBM'


def movie(update, context):
    chat_id = update.message.chat_id
    text = update.message.text[7:].strip();

    print(text)
    url = "http://www.omdbapi.com/?apikey=3c5f42ed&"
    contents = requests.get(url+"t={}".format(text)).json()

    if contents['Response']!='False':
        print(contents)

        for key, value in contents.items():
            if(key not in [ 'Response', 'Poster']):
                context.bot.send_message(chat_id=chat_id,text= "{} = {}".format(key,value))


        if contents['Poster']!="N/A":
            context.bot.send_photo(chat_id=chat_id, photo=contents['Poster'])
        else :
            context.bot.send_message(chat_id=chat_id,text= "No poster available for this one")
    else :
        context.bot.send_message(chat_id=chat_id,text= "No movie available for this title = "+text)



def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="/Movie <Moviename>")




def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('movie',movie))
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
