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

        try:
            attachments = data['items'][num]['attachments']
        except:
            try:
                more_text = data['items'][num]['copy_history'][0]['text']
                attachments = data['items'][num]['copy_history'][0]['attachments']
                text = '\n\n ' + more_text
            except:
                attachments = []
                print(data)

        attachments_list = []

        try:
            geo = data['items'][num]['geo']
            location = 'https://www.google.ru/maps/search' # + geo['coordinates']
            attachments_list.append(location)
        except:
            pass

        for element in attachments :
                if element['type'] == 'photo':
                        image = element['photo']['sizes'][-1]['url']
                        attachments_list.append(image)

                elif element['type']== 'video':
                    video = element['video']['access_key']
                    attachments_list.append(video)

                elif element['type'] == 'audio':
                    pass

                elif element['type'] == 'link':
                    url = element['link']['url']
                    description = element['link']['description']

                    if description == 'Playlist':
                        title = element['link']['title']
                        image = element['link']['photo']['sizes'][-1]['url']
                        album = title + '/n' + image + '/n/n' + url
                        attachments_list.append(album)
                    else:
                        link = url + '/n/n' + description
                        attachments_list.append(link)
                    pass

                elif element['type']== 'doc':
                    title = element['doc']['title']
                    url = element['doc']['url']
                    document = title + '/n/n' + url
                    attachments_list.append(album)

                elif element['type']== 'poll':
                    poll = 'нахуй иди мне лень с этим разбираться'
                    attachments_list.append(poll)

                else:
                    attachments_list.append(element['type'] + 'unknown type')

        cleaned_result = [gr_id, date, is_ad, text, attachments_list]
        return cleaned_result


    def parsing_response(self, group_id):
        response = requests.get('https://api.vk.com/method/wall.get', params={
            'access_token': self.Token,
            'v': self.version,
            'domain': group_id,
            'count': 3
        })
        all_data = response.json()
        cleaned_data = self.cleaning(all_data['response'], 1)
        return cleaned_data




