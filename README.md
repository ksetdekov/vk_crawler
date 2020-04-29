# vk_crawler
tool to collect data for analysis from friends

1. хотим сделать такой запрос https://vk.com/dev/friends.get?params[user_id]=1631159&params[fields]=country%2C%20bdate%2C%20sex&params[name_case]=nom&params[v]=5.103
 * field "country, bdate, sex"
 * name case "nom"
 
2. получать данные для token так  https://oauth.vk.com/authorize?client_id=IDприложения&scope=friends,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token
3. ПОчитать гайд  https://habr.com/ru/post/221251/