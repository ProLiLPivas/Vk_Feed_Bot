import telebot
import datetime,time
from bot_core.model import Model
from VkParser.search_new_group import Search
from VkParser.scanning import Scanner
from bot_core.Config import Configuration
from telebot import types


bot = telebot.TeleBot(Configuration.TOKEN)  # Telegram bot token

# COMMANDS LIST
@bot.message_handler(content_types=['text'])
def search_request(message):
    # try:
        if message.text =='/start':
            bot.reply_to(message, "Hello user\n welcome to my bot \n if u dont now how 2 use it write /info command ")

        if message.text == '/search':
            bot.reply_to(message, "Write id of group u want 2 find")  # answer on ur /search command
            bot.register_next_step_handler(message, search_result)  # waiting 4 user's response

        if message.text == '/break':
            Configuration.working = False
            bot.reply_to(message, 'ok')

        if message.text == '/go':
            if Configuration.working != True:
                bot.reply_to(message, 'Let\'s go')
                Configuration.working = True
                scanning(message)

        if message.text == '/reg':
            pass

        if message.text == '/info':
            bot.reply_to(message, Configuration.info)

        if message.text == '/hi' :
            bot.reply_to(message, "Wake da fu*k up \n Samuray")
            print(message)
            reg_user(message)
            bot.reply_to(message, 'Hi ' + message.from_user.first_name)


    # except Exception:
    #     print(Exception)


@bot.callback_query_handler(func=lambda  call:True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'subscribe':
                bot.reply_to(call.message, "Write emoji or any symbol which will denote ur subscribed group ")
                bot.register_next_step_handler(call.message, add_emoji)

            elif call.data == 'unsubscribe':
                unsubscribing(Configuration.search_cash['group_id'],Configuration.user_id)

            elif call.data == 'Y':
                pass
            elif call.data == 'N':
                pass

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=". . . ", reply_markup=None)
    except Exception as e:
        print(e)

# ADD USER
def reg_user(message):
    telegram_id = message.from_user.id
    name = message.from_user.first_name
    token = Configuration.vk_parsing_Token
    m = Model()
    m.get_user(telegram_id, name, token)


# SUBSCRIBE
def get_buttons(message, answer, group_id):
    group_is_exist = 0
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Subscribe', callback_data='subscribe')
    button2 = types.InlineKeyboardButton('Unsubscribe', callback_data='unsubscribe')
    m = Model()
    subs_list = m.get_sub_list(Configuration.user_id)
    for group_num in range(0,len(subs_list)):
        if subs_list[group_num][0] == group_id:
            group_is_exist = 1
    if group_is_exist == 0:
        markup.add(button1)
        bot.reply_to(message, answer , reply_markup=markup)
    else:
        markup.add(button2)
        bot.reply_to(message, answer +'\n U already subscribed', reply_markup=markup)

def add_emoji(message):
    bot.reply_to(message, 'U want 2 choose this one '+ message.text)
    Configuration.search_cash['emoji']  = message.text
    continue_subscribing(message)


def continue_subscribing(message):
    emoji = Configuration.search_cash['emoji']
    print(emoji)
    subscribing(Configuration.search_cash['group_id'], Configuration.search_cash['group_name'], emoji,
                Configuration.user_id)
    bot.reply_to(message, "u r successfully subscribe on " + Configuration.search_cash['group_name'])



def subscribing(group_id, group_name, emoji, User_id):
    m = Model()
    m.add_group(group_id, group_name, emoji, User_id)
    m.update_amount(1, User_id)


def unsubscribing(group_id, User_id):
    m = Model()
    m.delete_group(group_id, User_id)
    m.update_amount(-1, User_id)


# GROUPS SEARCH
# def get_group_id(message):      # collect user's response
#     group_id = message.text
#     Search.group_id = group_id      # set group_id
#     search_result(message)      # causes group_id processing


def search_result(message):     # making result and return parsed groups data
    try:

        response = Search(message)
        server_response = response.search_response()[0]
        group_name = response.search_response()[1]
        group_photo = response.search_response()[2]
        group_id = response.search_response()[3]

        Configuration.search_cash['group_name'] = group_name
        Configuration.search_cash['group_id'] = group_id
        Configuration.search_cash['User_id'] = Configuration.user_id
        Configuration.search_cash['emoji'] = '.'
        print(Configuration.search_cash)
        if server_response == 200:
            answer = 'эта та группа что вы искали? \n \n' + group_name + '\n' + group_photo
            get_buttons(message, answer, group_id)

        else:
            answer = '404 not found'
            bot.reply_to(message, answer)
    except Exception:
        print(Exception)


#GET FEED
def print_all(message, response, group_id, user_id):
    m = Model()
    name = m.get_emoji_n_name(group_id, user_id)[0]
    emoji = m.get_emoji_n_name(group_id, user_id)[1]
    time = response[1]
    text = response[3]
    first_image = response[4][0]

    value = datetime.datetime.fromtimestamp(time)
    time = value.strftime('%d-%m   %H:%M')

    result = emoji + name + '\n' +str(time) + '\n\n' + str(text) + '\n ' + first_image
    bot.reply_to(message, result)

    if len(response[4]) > 1 :
        for image in range(1, len(response[4])):
            bot.reply_to(message, response[4][image])


def scanning(message):
    while Configuration.working :
        m = Model()
        subs_list = m.get_sub_list(Configuration.user_id)
        for iteration in range(0,len(subs_list)):
            if Configuration.working == False:
                break
            Configuration.working = True
            time.sleep(0.3)
            if Configuration.working == False:
                break
            s = Scanner()
            response = s.parsing_response(subs_list[iteration][0])
            last_bup_time = m.get_last_pub_time(subs_list[iteration][0])[0][0]
            print('request was made' + ' ' + str(iteration) )

            if response[1] > last_bup_time and response[2] != 1 :
                print_all(message, response, subs_list[iteration][0], Configuration.user_id)
                m.update_last_pub_time(response[1], subs_list[iteration][0], Configuration.user_id)


def event_loop():
    pass


# Running
bot.polling(none_stop=True)

