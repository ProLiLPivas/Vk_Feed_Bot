import time
from bot_core.controller import bot
from bot_core.Config import Configuration
from VkParser.search_new_group import Search
from VkParser.scanning import Scanner
from telebot import types

# GROUPS SEARCH



def search_result(message):     # making result and return parsed groups data
    response = Search()
    if response.search_response()[0] == 200:
        answer = 'эта та группа что вы искали? \n \n' + response.search_response()[1] + '\n' + response.search_response()[2]
        group_numb = get_buttons(message,answer,response.search_response()[3])

        Scanner.group_id = response.search_response()[3]
        Scanner.emoji = '⚫'
        Scanner.group_number = group_numb
    else:
        answer = '404 not found'
        bot.reply_to(message, answer)



# SUBSCRIBE
def get_buttons(message,answer, group_id):
    group_is_exist = 0
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Subscribe', callback_data='subscribe')
    button2 = types.InlineKeyboardButton('Unsubscribe', callback_data='unsubscribe')
    for group_num in range(0,len(Scanner.subs_list)):
        if Scanner.subs_list[group_num] == group_id:
            group_is_exist = 1
            group_number = group_num
    if group_is_exist == 0:
        markup.add(button1)
    else:
        markup.add(button2)
    bot.reply_to(message, answer+'\n вы уже подписанны на эту группу', reply_markup=markup)
    return group_number

def subscribing(group_id, emoji):
    Scanner.subs_list.append(group_id)
    Scanner.last_pub_time.append(0)
    Scanner.emoji_list.append(emoji)
    #Scanner.subscribing_limit += 1

def unsubscribing(group_number):
    del Scanner.subs_list[group_number]
    del Scanner.last_pub_time[group_number]
    del Scanner.emoji_list[group_number]
    #subscribing_limit -= 1

def get_data():
    pass

#GET FEED
def print_all(message, response, i):
    Search.group_id = Scanner.subs_list[i]
    name = Search()
    name = name.search_response()[1]
    emoji = str(Scanner.emoji_list[i])
    result = emoji + name + '\n' +str(response[1]) + '\n\n' + str(response[3]) + '\n ' + response[4][0]
    bot.reply_to(message, result)
    if len(response[4]) > 1 :
        for image in range(1, len(response[4])):
            bot.reply_to(message, response[4][image])

def scanning(message):
    while Configuration.working :
        for iteration in range(0,len(Scanner.subs_list)):
            if Configuration.working == False:
                break
            Configuration.working = True
            time.sleep(2)
            if Configuration.working == False:
                break
            print('request was made' + ' ' + str(iteration))
            response = Scanner()
            response= response.parsing_response(Scanner.subs_list[iteration])

            if response[1] > Scanner.last_pub_time[iteration] and response[2] !=1 :
                print_all(message, response, iteration)

                Scanner.last_pub_time[iteration] = response[1]
