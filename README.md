# vk_crawler
Tool to collect data for analysis about friends from open public data of social network http://vk.com/



* This Crawler starts from one ID and pull all the friends of this person in a JSON response using the official API.
    * One must create their own hidden.py file, that contains a valid API token in a format:
    `token = 'token_string' `
* Additional fields collected with each friend list request:
    * Country
    * Birth date
    * Sex
* Name in a nominative case "nom"
 
## Additional info 
1. For it to work, ir requires an App to be created inside a Developer section of the website https://vk.com/dev and https://vk.com/apps?act=manage
2. How I received an authorisation token  https://oauth.vk.com/authorize?client_id=IDприложения&scope=friends,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token
3. One of the guides I used  https://habr.com/ru/post/221251/