import time
import requests
import datetime
from bot_core.model import Model
from bot_core.Config import Configuration
from VkParser.scanning import Scanner

class Feed:
    # def __init__(self):
    #     self.scanning()

    def event_loop(self):
        pass

    def print_all(self, response, group_id, tg_id): # примерное время 10 секунд
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
        ########################################################################################
        ## def print_other():                                                                 ##
        ########################################################################################

        iteration = 1
        if len(response[4]) > 1:     # this block work then post have 2 or more attachments and send it in new message, because if we have lone link telegram
            for attachment in range(1, len(response[4])):
                iteration += 1
                post_part = Configuration.URL + 'sendmessage?chat_id={}&text={}'.format(tg_id,str(iteration) + '. ' + response[4][attachment])
                requests.get(post_part)


    def scanning(self):
        while True:
            m = Model()
            users_list = m.get_all_users()
            for user in users_list:                     # waiting 4 user

                tg_id = user[0]
                subs_list = m.get_sub_list(tg_id)
                print(subs_list)

                if m.get_user(tg_id)[0][5] == 0:
                    continue
                if subs_list != []:

                    for iteration in range(0, len(subs_list)):  # waiting 4 all group
                        if m.get_user(tg_id)[0][5] == 0:
                            break
                        m.set_isSearching(tg_id, 1)
                        time.sleep(Configuration.timeout)
                        if m.get_user(tg_id)[0][5] == 0:
                            break
                        s = Scanner()

                        response = s.parsing_response(subs_list[iteration][0])          # waiting server response
                        last_bup_time = m.get_last_pub_time(subs_list[iteration][0], tg_id)[0][0]
                        print('request was made' + ' ' + str(iteration) + ' ' + str(tg_id))

                        if response[1] > last_bup_time and response[2] != 1:
                            self.print_all(response, subs_list[iteration][0], tg_id)    # waiting 4 print all
                            m.update_last_pub_time(response[1], subs_list[iteration][0], tg_id)
                else:
                    url = Configuration.URL + 'sendmessage?chat_id={}&text={}'.format(tg_id, 'Sorry u dont subscribed on any group \n write /info 2 know how 2 do it')
                    requests.get(url)
                    m.set_isSearching(tg_id, 0)



t0 = time.time()
print(t0)

feed = Feed()

response = [0,t0, 0, 'ДАаня а ты знал что ты гей', ['ДАаня а ты знал что ты гей','ДАаня а ты знал что ты гей', 'ДАаня а ты знал что ты гей' ,'ДАаня а ты знал что ты гей', 'ДАаня а ты знал что ты гей',' ДАаня а ты знал что ты гей''ДАаня а ты знал что ты гей','zsrghhhh','zhyyxzuuu']]

feed.print_all(response, 'doggyboobs', 434401613)

print(time.time() - t0)
