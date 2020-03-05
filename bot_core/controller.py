import time

import telebot
from bot_core.Config import Configuration
from bot_core.messages_dispaly import Display
from bot_core.model import Model

from telebot import types

bot = telebot.TeleBot(Configuration.TOKEN)  # Telegram bot token

display = Display()
model = Model()


# COMMANDS LIST
@bot.message_handler(content_types=['text'])
def search_request(message):
    # try:

        if message.text =='/start':
            # keyboard
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            go_btn = types.KeyboardButton('Go')
            search_btn = types.KeyboardButton('Search')
            sub_list_btn = types.KeyboardButton('My Subs')

            markup.add(go_btn, search_btn, sub_list_btn)

            bot.reply_to(message, "Hello user\n welcome to my bot \n if u dont now how 2 use it write /info command ", reply_markup=markup)
            display.reg_user(message)

        if message.text == 'Search':
            bot.reply_to(message, "Write id of group u want 2 find")  # answer on ur /search command
            bot.register_next_step_handler(message, display.search_result)  # waiting 4 user's response


        if message.text == 'Break':
            m = Model()
            m.set_isSearching(message.from_user.id, 0)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            go_btn = types.KeyboardButton('Go')
            search_btn = types.KeyboardButton('Search')
            sub_list_btn = types.KeyboardButton('My Subs')

            markup.add(go_btn, search_btn, sub_list_btn)
            bot.reply_to(message, 'ok', reply_markup=markup)


        if message.text == 'Go':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            break_btn = types.KeyboardButton('Break')
            search_btn = types.KeyboardButton('Search')
            sub_list_btn = types.KeyboardButton('My Subs')

            m = Model()
            if m.get_user(message.from_user.id)[0][5] != 1:
                markup.add(search_btn, sub_list_btn, break_btn)
                bot.reply_to(message, 'Let\'s go', reply_markup=markup)
                m.set_isSearching(message.from_user.id, 1)

        if message.text == 'My Subs':
            display.get_sublist(message)

        if message.text == 'Info':
            bot.reply_to(message, Configuration.info)

        if message.text == 'Hi' :
            bot.reply_to(message, 'Hi ' + message.from_user.first_name,   )

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

            elif call.data[0] == '!':
                markup = types.InlineKeyboardMarkup(row_width=2)

                group_id = call.data[:0] + call.data[0+1:]
                tg_id = call.message.chat.id
                user_id = model.get_user(tg_id)[0][0]  # next function require user's, so we get it fron db
                emoji = model.get_emoji_n_name(group_id, user_id)[1]  # we get emoji &
                group_name = model.get_emoji_n_name(group_id, user_id)[0]
                text = 'u chose \n' + emoji + ' ' + group_name + '\n now u can do some extra options'

                change_emoji_btn = types.InlineKeyboardButton('Change emoji', callback_data='e' + group_id  )
                unsub_btn = types.InlineKeyboardButton('Unsubscribe', callback_data='u' + group_id)
                get_feed_btn = types.InlineKeyboardButton('Get Feed', callback_data='g'  +group_id)
                cancel_btn = types.InlineKeyboardButton('Cancel', callback_data='Cancel')

                markup.add(change_emoji_btn, unsub_btn, get_feed_btn, cancel_btn)

                bot.reply_to(call.message, text, reply_markup=markup)

            elif call.data[0] == 'e':
                display.change_emoji_cash = call.data
                bot.reply_to(call.message, 'write ur emoji')
                bot.register_next_step_handler(call.message, display.change_emoji)



            elif call.data[0] == 'u':
                text = 'u unsub '
                group_id = call.data[:0] + call.data[0+1:]
                user_id = model.get_user(call.message.chat.id)[0][0]

                display.unsubscribing(group_id, user_id)
                bot.reply_to(call.message, text)


            elif call.data[0] == 'g':
                markup = types.InlineKeyboardMarkup(row_width=2)

                group_id = call.data[:0] + call.data[0 + 1:]
                tg_id = call.message.chat.id
                user_id = model.get_user(tg_id)[0][0]  # next function require user's, so we get it fron db
                emoji = model.get_emoji_n_name(group_id, user_id)[1]  # we get emoji &
                group_name = model.get_emoji_n_name(group_id, user_id)[0]
                text = 'u want 2 get feed \n' + emoji + ' ' + group_name + '\n how many posts u want'

                button_10= types.InlineKeyboardButton('10', callback_data='1' + group_id)
                button_20 = types.InlineKeyboardButton('20', callback_data='2' + group_id)
                button_50 = types.InlineKeyboardButton('50', callback_data='5' + group_id)
                button_100= types.InlineKeyboardButton('100', callback_data='0' + group_id)

                markup.add(button_10, button_20, button_50, button_100)
                bot.reply_to(call.message, text, reply_markup=markup)

            elif call.data[0] == '1':
                group_id = call.data[:0] + call.data[0 + 1:]
                display.get_group_feed(call, group_id)

            elif call.data[0] == '2':
                group_id = call.data[:0] + call.data[0 + 1:]
                display.get_group_feed(call, group_id, 20)

            elif call.data[0] == '5':
                group_id = call.data[:0] + call.data[0 + 1:]
                display.get_group_feed(call, group_id, 50)

            elif call.data[0] == '0':
                group_id = call.data[:0] + call.data[0 + 1:]
                display.get_group_feed(call, group_id, 100)


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








