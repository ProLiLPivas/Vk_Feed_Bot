
#
# def m(func):
#     def wrapper(func):
#         print(1)
#         result = func()
#         print(3)
#         return result
#
#     return wrapper
# @m
# def p(q):
#     print(q)
#
# p(2)
import requests

#
# vk_parsing_Token = '11f210e411f210e411f210e4ad119d60a4111f211f210e44fc6c62c130ac70783620ab5'
#
# api_version = 5.103
#
# group_id = "stlbn"
# group_id =  "11f210e411f210e411f210e4ad119d60"
#
# response = requests.get('https://api.vk.com/method/wall.get', params={
#             'access_token': vk_parsing_Token,
#             'v': api_version,
#             'domain': group_id,
#             'count': 1
#         })
# all_data = response.json()
# print(all_data)

#
# response = requests.get('https://api.vk.com/method/groups.getById', params={
#                     'access_token' : vk_parsing_Token,
#                     'v' : api_version,
#                     'group_id' : group_id

#                 })
#
# all_data = response.json()
# print(all_data)
#
# geo = '55.75470259927 37.711414194696'
# geo = ",".join(geo.split())
#
# location = 'https://www.google.ru/maps/@' + geo
# print(location)
#
# #
#
# s = ' svavg&cv'
#
# a = s.replace('&', ' and ')
# a = s.replace('%', ' ')
#
# print(a)
# print(s)
