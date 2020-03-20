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
        '''this func gonna work after "My Subs" command
        user get full list of groups he subscribed
        he can get more group options if he choose one of them
        '''

        sub_list = types.InlineKeyboardMarkup(row_width=2)

        model = Model()
        count = 0
        tg_id = message.from_user.id
        groups = model.get_sub_list(message.from_user.id)

        for group in groups:
            count += 1                                                  # counter which count number of group
            user_id = model.get_user(message.from_user.id)[0][0]        # next function require user's, so we get it fron db
            emoji = model.get_emoji_n_name(group[0], user_id)[1]        # we get emoji &
            group_name =  model.get_emoji_n_name(group[0], user_id)[0]  # & group name from data base. We need them to form message 4 user

            button_text = str(count)+'. ' + emoji + ' ' + group_name
            group_btn = types.InlineKeyboardButton(button_text , callback_data='!' + group[0])
            sub_list.add(group_btn)

        self.bot.reply_to(message, 'u subscribe on {} groups'.format(count) ,reply_markup=sub_list)


    # SUBSCRIBE
    def add_emoji(self, message):
        self.bot.reply_to(message, 'U want 2 choose this one ' + message.text)
        Configuration.search_cash['emoji'] = message.text[0]
        self.continue_subscribing(message)

    def continue_subscribing(self, message):
        emoji = Configuration.search_cash['emoji']
        user_id = Configuration.search_cash['user_id']
        group_name = Configuration.search_cash['group_name']
        group_id = Configuration.search_cash['group_id']
        tg_id = message.from_user.id

        self.subscribing( group_id ,group_name, emoji, user_id, tg_id)
        self.bot.reply_to(message, "u r successfully subscribe on " + group_name)


    def subscribing(self, group_id, group_name, emoji, User_id, tg_id):
        m = Model()
        sub_list = m.get_sub_list(tg_id)
        for group in sub_list:
            for group in sub_list:
                if group[0] == group_id:
                    break
                else:
                    continue
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
            if server_response == 200:
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

                if is_closed == 0:
                    answer = 'эта та группа что вы искали? \n \n' + group_name + '\n' + group_photo
                    self.search_get_buttons(message, answer, group_id)
                else:
                    answer = 'Sorry this croup is closed, u cant sub it \n \n' + group_name + '\n' + group_photo
                    self.bot.reply_to(message, answer)
            elif server_response == 404:
                answer = '404 not found'
                self.bot.reply_to(message, answer)
        except Exception:
            print('searching error')


    # GET FEED
    def print_all(self, response, group_id, tg_id):
        ''' this function was made 2 arrange all information got from vk group send it 2 users tg chat '''
        m = Model()
        user_id = m.get_user(tg_id)[0][0]
        name = m.get_emoji_n_name(group_id, user_id)[0].replace('&', ' and ')
        emoji = m.get_emoji_n_name(group_id, user_id)[1]
        time = response[1]
        text = response[3]
        if response[4] != []:
            first_attachment = response[4][0]
        else:
            first_attachment = ' '  # if post dont have any attachment we write empty string

        value = datetime.datetime.fromtimestamp(time)
        time = value.strftime('%d-%m   %H:%M')

        result = emoji + name + '\n' + str(time) + '\n\n' + str(text) + '\n ' + first_attachment
        print(result)
        url = Configuration.URL + 'sendmessage?chat_id={}&text={}'.format(tg_id, result)
        requests.get(url)
        iteration = 1
        if len(response[4]) > 1:    # this block work then post have 2 or more attachments and send it in new message, because if we have lone link telegram
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

    # UPDATE EMOJI
    def continue_change(self):
        pass

    change_emoji_cash = None

    def change_emoji(self, message):
        model = Model()
        emoji = message.text[0]
        group_id = self.change_emoji_cash[:0] + self.change_emoji_cash[0 + 1:]
        user_id = model.get_user(message.chat.id)[0][0]
        model.update_emoji(group_id, user_id, emoji)
        self.bot.reply_to(message, 'u change emoji on '+ emoji)



    # GET FEED FROM ONE GROUP


    def get_group_feed(self, call, group, amount=10):
        m = Model()
        s = Scanner()
        groups = m.get_sub_list(call.message.chat.id)
        print(groups)
        try:
            gr = groups[groups.index((group,))]
            response = s.parsing_group(gr , amount)
            try:
                for post in response:
                    self.print_all(post, group, call.message.chat.id)
            except Exception:
                self.bot.reply_to(call.message, 'It was last post in this group')
        except Exception:
            self.bot.reply_to(call.message, 'Sorry u dont sub this group ')





    def event_loop(self):
        pass


