from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Paste your own token in the variable below
TOKEN = ""


def dog_picture_handler(update, context):
    print("\n====== entered dog_picture_handler ======")
    chat_id = update.message.chat_id
    
    # enter the url below in browser to take a look
    # this url is a API that returns you a randowm dog picture
    contents = requests.get("https://random.dog/woof.json").json()
    print("====== contents: " + str(contents))
    dog_picture_url = contents["url"]
    print("====== dog_picture_url: " + dog_picture_url)
    
    # send the image url link back to user
    context.bot.send_message(chat_id=chat_id, text=dog_picture_url)
    # send as a photo instead
    # context.bot.send_photo(chat_id=chat_id, photo=dog_picture_url)

def movie_handler(update, context):
    print("\n====== entered movie_handler ======")
    chat_id = update.message.chat_id
    
    print("====== movie_handler update.message.text: " + update.message.text)
    # TODO No.1: 
    # get the movie name entered by the user from the variable update.message.text
    # and store it in the variable movie_name
    movie_name = update.message.text[7:].strip()
    print("====== movie_name: " + movie_name)

    # TODO No.2:
    # Given a API, use the API to retrieve information related to movie name
    # http://www.omdbapi.com/?apikey=3c5f42ed&t=<movie_name>
    # Example: http://www.omdbapi.com/?apikey=3c5f42ed&t=minions
    constructed_url = "http://www.omdbapi.com/?apikey=3c5f42ed&t=" + movie_name
    print("====== constructed_url: " + constructed_url)
    contents = requests.get(constructed_url).json()
    print("====== contents: " + str(contents))

    # TODO No.3: 
    # Retrieve the field Response from the contents
    response = contents["Response"]
    print("====== response: " + response)
    
    # TODO No.4: 
    # Given successul query will have the response as True, unsuccessul query will have response as False
    # write a if else condition
    # for failed query: send back a message to notify user that there is no information found
    # for success query: send back the Title and Year
    if response == "False":
        context.bot.send_message(chat_id=chat_id,text= "No movie available for this title: " + movie_name)
    else:
        title = contents["Title"]
        year = contents["Year"]
        context.bot.send_message(chat_id=chat_id,text="Title: " + title + ". Year: " + year)
        
        # TODO No.5:
        # add on to the response True branch that we have written
        # return the Poster field as photo to the user
        if contents["Poster"]!="N/A":
            context.bot.send_photo(chat_id=chat_id, photo=contents["Poster"])
        else:
            context.bot.send_message(chat_id=chat_id,text="No poster available for this one")
            
        # TODO No.6:
        # Open ended question. Return whichever field in whichever format you want.
        # teachers can go through the example below
        for key, value in contents.items():
            if(key not in ["Response", "Poster"]):
                constructed_text = key + ": " + str(value)
                context.bot.send_message(chat_id=chat_id,text=constructed_text)

def fallback_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Please try with: ")
    context.bot.send_message(chat_id=update.effective_chat.id, text="/movie <movie_name>")


def main():
    print("====== starting bot program ======")
    
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # example dog_picture_handler to be demonstrated by teacher
    dispatcher.add_handler(CommandHandler("dog", dog_picture_handler))

    # movie_handler to be filled in by student
    dispatcher.add_handler(CommandHandler("movie", movie_handler))
    
    # Optional content - fallback handler
    dispatcher.add_handler(MessageHandler(Filters.all, fallback_handler))
    
    updater.start_polling()
    updater.idle()
    

if __name__ == "__main__":
    main()
