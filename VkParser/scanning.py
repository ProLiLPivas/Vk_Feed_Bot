import requests
from bot_core.Config import Configuration


class Scanner:
    '''     '''
    Token = Configuration.vk_parsing_Token
    version = Configuration.api_version


    def cleaning(self, data, num):
        gr_id = data['items'][num]['id']
        date = data['items'][num]['date']
        is_ad = data['items'][num]['marked_as_ads']
        text = data['items'][num]['text']
        attachments = data['items'][num]['attachments']
        attachments_list = []
        # print(attachments)
        for element in attachments :
            if element['type'] == 'photo':
                attachments_list.append(element['photo']['sizes'][2]['url'])
            elif element['type']== 'video':
                attachments_list.append(element['video']['access_key'])
            elif element['type'] == 'audio':
                pass
            elif element['type']== 'poll':
                pass
            else:
                attachments_list.append(element['type'] + 'unknown type')

        cleaned_result = [gr_id, date, is_ad, text, attachments_list]
        return cleaned_result


    def parsing_response(self, group_id):
        response = requests.get('https://api.vk.com/method/wall.get', params={
            'access_token': self.Token,
            'v': self.version,
            'domain': group_id,
            'count': 2
        })
        all_data = response.json()
        cleaned_data = self.cleaning(all_data['response'], 0)
        return cleaned_data









