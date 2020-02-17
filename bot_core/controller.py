import time

import telebot
from pip._internal.utils import logging

from bot_core.Config import Configuration
from bot_core.messages_dispaly import Display
from bot_core.model import Model

bot = telebot.TeleBot(Configuration.TOKEN)  # Telegram bot token

display = Display()
model = Model()


# COMMANDS LIST
@bot.message_handler(content_types=['text'])
def search_request(message):
    # try:
        if message.text =='/start':
            bot.reply_to(message, "Hello user\n welcome to my bot \n if u dont now how 2 use it write /info command ")
            display.reg_user(message)

        if message.text == '/search':
            bot.reply_to(message, "Write id of group u want 2 find")  # answer on ur /search command
            bot.register_next_step_handler(message, display.search_result)  # waiting 4 user's response

        if message.text == '/break':
            Configuration.working = False
            bot.reply_to(message, 'ok')

        if message.text == '/go':
            if Configuration.working != True:
                bot.reply_to(message, 'Let\'s go')
                Configuration.working = True
                display.scanning(message)

        if message.text == '/mygroups':
            id = model.get_user(message.from_user.id)[0][0]
            groups = model.get_sub_list(id)
            print(groups)
            for group in groups:
                bot.reply_to(message, group[0])

        if message.text == '/info':
            bot.reply_to(message, Configuration.info)

        if message.text == '/hi' :
            bot.reply_to(message, "Wake da fu*k up \n Samuray")
            print(message)
            # reg_user(message)
            bot.reply_to(message, 'Hi ' + message.from_user.first_name)
    # except Exception:
    #     print(Exception)


@bot.callback_query_handler(func=lambda  call:True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'subscribe':
                bot.reply_to(call.message, "Write emoji or any symbol which will denote ur subscribed group ")
                bot.register_next_step_handler(call.message, display.add_emoji)

            elif call.data == 'unsubscribe':
                display.unsubscribing(Configuration.search_cash['group_id'],Configuration.user_id)

            elif call.data == 'Y':
                pass
            elif call.data == 'N':
                pass

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=". . . ", reply_markup=None)
    except Exception as e:
        print(e)


# Running
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            # logging.error(e)
            time.sleep(5)
            print('Internet error')





