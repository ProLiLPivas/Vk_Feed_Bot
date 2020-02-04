import requests


class Search:
    '''

    '''


    vk_parsing_Token = '11f210e411f210e411f210e4ad119d60a4111f211f210e44fc6c62c130ac70783620ab5'
    api_version = 5.103
    group_id = None


    def parse_response(self):                                                  # parsing data from page and sending it 2 bot core
        response = requests.get('https://api.vk.com/method/groups.getById', params={
            'access_token' : self.vk_parsing_Token,
            'v' : self.api_version,
            'group_id' : self.group_id
        })

        all_data = response.json()
        cleaned_data = (200, all_data['response'][0]['name'], all_data['response'][0]['photo_200'], self.group_id)
        return cleaned_data



    def search_response(self):                                                  # cheking page existence
        if self.group_id != None:
            response = requests.get('https://vk.com/'+ self.group_id)
            if response.status_code == 200:
                generated_response = self.parse_response()
                return generated_response
            else:
                return (404, 'name not found','photo not found', self.group_id )










