from hidden import access_token
import requests
# 'user_id':'1631159'
resp = requests.get(f'https://api.vk.com/method/friends.get?user_id=1631159&fields=country,bdate,sex&access_token={access_token}&v=5.103')
jsontype = resp.json()
# print(json.dumps(jsontype, indent=4))
print(jsontype['response']['items'][1]['country'])
print(jsontype['response']['count'])
