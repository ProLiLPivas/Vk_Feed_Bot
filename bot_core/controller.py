import telebot
from bot_core.messages_dispaly import *
from bot_core.Config import Configuration

bot = telebot.TeleBot(Configuration.TOKEN)  # Telegram bot token

# COMMANDS LIST
@bot.message_handler(content_types=['text'])
def search_request(message):
    if message.text == '/search':
        bot.reply_to(message, "write id of group u want 2 find")  # answer on ur /search command
        bot.register_next_step_handler(message, get_group_id)  # waiting 4 user's response

    if message.text == '/break':
        Configuration.working = False
        bot.reply_to(message, 'ok')

    if message.text == '/go':
        Configuration.working = True
        scanning(message)

    if message.text == '/reg':
        pass
    if message.text == '/hi' :
        bot.reply_to(message, "Wake da fu*k up \n Samuray")


@bot.callback_query_handler(func=lambda call : True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'subscribe':
                subscribing(Scanner.group_id,Scanner.emoji)
                Scanner.group_id = None
                Scanner.emoji = None
                bot.reply_to(call.message, 'u r successfully subscribe this group')
                print(Scanner.subs_list)

            elif call.data == 'unsubscribe':
                unsubscribing(Scanner.group_number)
                bot.reply_to(call.message, 'u r unsuccessfully subscribe this group')
                Scanner.group_number = None
                print(Scanner.subs_list)

            # removing message after pressed button
            bot.edit_message_text(
                chat_id=call.message.chat.id, message_id=call.message.message_id, text='subscribe', reply_markup=None)
            bot.edit_message_text(
                chat_id=call.message.chat.id, message_id=call.message.message_id, text='unsubscribe', reply_markup=None)
    except Exception as e:
        print(repr(e))

def get_group_id(message):      # collect user's response
    group_id = message.text
    Search.group_id = group_id      # set group_id
    search_result(message)      # causes group_id processing


# Running
bot.polling()

