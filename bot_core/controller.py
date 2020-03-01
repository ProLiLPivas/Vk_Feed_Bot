import time

import telebot
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
            m = Model()
            m.set_isSearching(message.from_user.id, 0)
            bot.reply_to(message, 'ok')

        if message.text == '/go':
            m = Model()
            if m.get_user(message.from_user.id)[0][5] != 1:
                bot.reply_to(message, 'Let\'s go')
                m.set_isSearching(message.from_user.id, 1)

        if message.text == '/mygroups':
            display.get_sublist(message)

        if message.text == '/info':
            bot.reply_to(message, Configuration.info)

        if message.text == '/hi' :
            bot.reply_to(message, "Wake da fu*k up \n Samuray")
            print(message)
            bot.reply_to(message, 'Hi ' + message.from_user.first_name)

        if message.text == '/':
            if message.from_user.id == Configuration.Admin:
                print('app is running')
                display.scanning()
                print(message)


    # except Exception:
    #    print('command error ')


@bot.callback_query_handler(func=lambda  call:True)
def callback_inline(call):
    # try:
        if call.message:
            if call.data == 'subscribe':
                bot.reply_to(call.message, "Write emoji or any symbol which will denote ur subscribed group ")
                bot.register_next_step_handler(call.message, display.add_emoji)

            elif call.data == 'unsubscribe':
                display.unsubscribing(Configuration.search_cash['group_id'], Configuration.search_cash['user_id'])

            elif call.data == 'Y':
                pass
            elif call.data == 'N':
                pass
            elif call.data[0] == 'e':
                pass
            elif call.data[0] == 'u':
                pass
            elif call.data[0] == 'c':
                pass

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=". . . ", reply_markup=None)
    # except Exception:
    #     print('buttons error')


# Running
if __name__ == "__main__":
    # while True:
    #     try:
            bot.polling(none_stop=True)


        # except Exception as e:
        #     # logging.error(e)
        #     time.sleep(5)
        #     print('Internet error')








