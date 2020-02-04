import requests

from bot_core.Config import Configuration

class Scanner:
    subs_list = ['konturgusya', 'stlbn', 'leprazo']
    last_pub_time = [0 , 0, 0]
    emoji_list = ['🦆', '🥑', '😱']
    subscribing_limit = 3

    # ento prosto kostil' otsan'te
    group_id = None
    group_number = None
    emoji = None

    Token = Configuration.vk_parsing_Token
    version = Configuration.api_version


    def cleaning(self, data, num):
        id = data['items'][num]['id']
        date = data['items'][num]['date']
        is_ad = data['items'][num]['marked_as_ads']
        text = data['items'][num]['text']
        attachments = data['items'][num]['attachments']
        attachments_list = []

        for element in attachments :
             attachments_list.append(element['photo']['sizes'][2]['url'])

        cleaned_result = [id, date, is_ad, text, attachments_list]
        return cleaned_result


    def parsing_response(self, group_id):
        response = requests.get('https://api.vk.com/method/wall.get', params={
            'access_token': self.Token,
            'v': self.version,
            'domain': group_id,
            'count': 2
        })
        all_data = response.json()
        cleaned_data = self.cleaning(all_data['response'], 1)
        return cleaned_data









