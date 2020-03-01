import datetime,time
import requests
import telebot
from bot_core.model import Model
from VkParser.search_new_group import Search
from VkParser.scanning import Scanner
from bot_core.Config import Configuration
from telebot import types


class Display:

    bot =  telebot.TeleBot(Configuration.TOKEN)

    # ADD USER
    def reg_user(self, message):
        m = Model()
        users = m.get_all_users()
        is_exist = False
        for user in users:
            if user[0] == message.from_user.id:
                print(1)
                is_exist = True
        if not is_exist:
            telegram_id = message.from_user.id
            name = message.from_user.first_name
            token = Configuration.vk_parsing_Token
            m.set_user(telegram_id, name, token)

    # SUB_LIST
    def get_sublist(self, message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        unsub_btn = types.InlineKeyboardButton('unsub', callback_data='u')
        change_emoji_btn = types.InlineKeyboardButton('change emoji', callback_data='e')
        cancel_btn = types.InlineKeyboardButton('cancel', callback_data='c')

        model = Model()
        count = 0
        groups = model.get_sub_list(message.from_user.id)
        markup.add(unsub_btn, change_emoji_btn, cancel_btn)
        for group in groups:
            count +=1
            user_id = model.get_user(message.from_user.id)[0][0]
            info = model.get_emoji_n_name(group[0], user_id)
            self.bot.reply_to(message, str(count)+'. ' + info[1] + ' ' +info[0] , reply_markup=markup)

    # SUBSCRIBE
    def add_emoji(self, message):
        self.bot.reply_to(message, 'U want 2 choose this one ' + message.text)
        Configuration.search_cash['emoji'] = message.text
        self.continue_subscribing(message)


    def continue_subscribing(self, message):
        emoji = Configuration.search_cash['emoji']
        user_id = Configuration.search_cash['user_id']
        group_name = Configuration.search_cash['group_name']
        group_id = Configuration.search_cash['group_id']

        print(emoji)

        self.subscribing( group_id ,group_name, emoji, user_id)
        self.bot.reply_to(message, "u r successfully subscribe on " + group_name)


    def subscribing(self, group_id, group_name, emoji, User_id):
        m = Model()
        m.add_group(group_id, group_name, emoji, User_id)
        m.update_amount(1, User_id)

    def unsubscribing(self, group_id, User_id):
        m = Model()
        m.delete_group(group_id, User_id)
        m.update_amount(-1, User_id)

    #  SEARCH
    def search_get_buttons(self, message, answer, group_id):
        group_is_exist = 0
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('Subscribe', callback_data='subscribe')
        button2 = types.InlineKeyboardButton('Unsubscribe', callback_data='unsubscribe')
        m = Model()
        tg_id = message.from_user.id
        subs_list = m.get_sub_list(tg_id)
        for group_num in range(0, len(subs_list)):
            if subs_list[group_num][0] == group_id:
                group_is_exist = 1
        if group_is_exist == 0:
            markup.add(button1)
            self.bot.reply_to(message, answer, reply_markup=markup)
        else:
            markup.add(button2)
            self.bot.reply_to(message, answer + '\n U already subscribed', reply_markup=markup)

    def search_result(self, message):  # making result and return parsed groups data
        try:
            m = Model()
            response = Search(message)
            server_response = response.search_response()[0]
            group_name = response.search_response()[1]
            group_photo = response.search_response()[2]
            group_id = response.search_response()[3]
            is_closed = response.search_response()[4]
            tg_id = message.from_user.id
            user_id = m.get_user(tg_id)[0][0]


            Configuration.search_cash['group_name'] = group_name
            Configuration.search_cash['group_id'] = group_id
            Configuration.search_cash['user_id'] = user_id
            Configuration.search_cash['emoji'] = '.'
            print(Configuration.search_cash)
            if server_response == 200:
                if is_closed == 0:
                    answer = 'эта та группа что вы искали? \n \n' + group_name + '\n' + group_photo
                    self.search_get_buttons(message, answer, group_id)
                else:
                    answer = 'Sorry this croup is closed, u cant sub it \n \n' + group_name + '\n' + group_photo
                    self.bot.reply_to(message, answer)
            else:
                answer = '404 not found'
                self.bot.reply_to(message, answer)
        except Exception:
            print('searching error')

    # GET FEED

    def print_all(self, response, group_id, tg_id):
        m = Model()
        user_id = m.get_user(tg_id)[0][0]
        name = m.get_emoji_n_name(group_id, user_id)[0].replace('&', ' and ')
        emoji = m.get_emoji_n_name(group_id, user_id)[1]
        time = response[1]
        text = response[3]
        if response[4] != []:
            first_attachment = response[4][0]
        else:
            first_attachment = ' '

        value = datetime.datetime.fromtimestamp(time)
        time = value.strftime('%d-%m   %H:%M')

        result = emoji + name + '\n' + str(time) + '\n\n' + str(text) + '\n ' + first_attachment
        print(result)
        url = Configuration.URL + 'sendmessage?chat_id={}&text={}'.format(tg_id, result)
        requests.get(url)
        iteration = 1
        if len(response[4]) > 1:
            for attachment in range(1, len(response[4])):
                iteration += 1
                post_part = Configuration.URL + 'sendmessage?chat_id={}&text={}'.format(tg_id, str(iteration)+ '. ' + response[4][attachment])
                requests.get(post_part)


    def scanning(self):
        while True:
            m = Model()
            users_list = m.get_all_users()
            for user in users_list:

                tg_id = user[0]
                subs_list = m.get_sub_list(tg_id)
                print(subs_list)

                if m.get_user(tg_id)[0][5] == 0:
                    continue
                if subs_list != []:

                    for iteration in range(0, len(subs_list)):
                        if m.get_user(tg_id)[0][5] == 0:
                            break
                        m.set_isSearching(tg_id, 1)
                        time.sleep(Configuration.timeout)
                        if m.get_user(tg_id)[0][5] == 0:
                            break
                        s = Scanner()

                        response = s.parsing_response(subs_list[iteration][0])
                        last_bup_time = m.get_last_pub_time(subs_list[iteration][0], tg_id)[0][0]
                        print('request was made' + ' ' + str(iteration) + ' ' + str(tg_id))

                        if response[1] > last_bup_time and response[2] != 1:
                            self.print_all(response, subs_list[iteration][0], tg_id)
                            m.update_last_pub_time(response[1], subs_list[iteration][0], tg_id)
                else:
                    url = Configuration.URL + 'sendmessage?chat_id={}&text={}'.format(tg_id,'Sorry u dont subscribed on any group \n write /info 2 know how 2 do it')
                    requests.get(url)
                    m.set_isSearching(tg_id, 0)

    def event_loop(self):
        pass


