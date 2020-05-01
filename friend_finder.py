import json
import sqlite3
import ssl
import urllib.request

from hidden import token


# 'user_id':'1631159'
# acct = '1631159'
# resp = requests.get(
#     f'https://api.vk.com/method/friends.get?user_id={acct}&fields=country,bdate,sex&access_token={token}&v=5.103')


def friend_url(user, secret=token):
    return f'''https://api.vk.com/method/friends.get?user_id={user}\
&fields=country,bdate,sex&access_token={secret}&v=5.103'''


conn = sqlite3.connect('friends.sqlite')  # friends db
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS People (id INTEGER PRIMARY KEY, 
                                                    vk_id INTEGER UNIQUE, 
                                                    first_name TEXT,
                                                    last_name TEXT,
                                                    sex INTEGER,
                                                    country_id INTEGER,
                                                    bdate TEXT,
                                                    retrieved INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Follows
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

count = 100
for i in range(count):
    acct = ''
    # while True:
    #     acct = input('Enter a Vk id, or quit: ')
    if acct == 'quit':
        break
    if len(acct) < 1:
        cur.execute('SELECT id, vk_id FROM People WHERE retrieved=0 LIMIT 1')  # get id and name
        try:
            (u_id, acct) = cur.fetchone()
        except TypeError:
            print('No unretrieved VK accounts found')
            continue
    else:
        cur.execute('SELECT id FROM People WHERE vk_id = ? LIMIT 1',  # check if there is that person
                    (acct,))

        try:
            u_id = cur.fetchone()[0]
        except TypeError:
            cur.execute('''INSERT OR IGNORE INTO People
                        (vk_id, retrieved) VALUES (?, 0)''', (acct,))
            conn.commit()  # if person not in the table, put him there and mark not retrieved
            if cur.rowcount != 1:
                print('Error inserting account:', acct)
                continue
            u_id = cur.lastrowid  # id of the user

    url = friend_url(acct)
    print('Retrieving account', acct)
    try:
        connection = urllib.request.urlopen(url, context=ctx)
    except Exception as err:
        print('Failed to Retrieve', err)
        break

    data = connection.read().decode()
    headers = dict(connection.getheaders())

    # if incorrect json recieved
    try:
        js = json.loads(data)
    except Exception as err:
        print('Unable to parse json', err)
        print(data)
        break

    # Debugging
    # print(json.dumps(js, indent=4))

    # if no users in json
    if 'response' not in js:
        if js['error']['error_code'] == 18:
            print('Deleted user')
            cur.execute('UPDATE People SET retrieved=1 WHERE vk_id = ?', (acct,))
            continue
        elif js['error']['error_code'] == 30:
            print('Private account')
            cur.execute('UPDATE People SET retrieved=1 WHERE vk_id = ?', (acct,))
            continue
        else:
            print('Incorrect JSON received, no response tag')
            print(json.dumps(js, indent=4))
            continue

    cur.execute('UPDATE People SET retrieved=1 WHERE vk_id = ?', (acct,))
    # loop over friends
    countnew = 0
    countold = 0
    for u in js['response']['items']:
        friend = u['id']
        first_name = u['first_name']
        last_name = u['last_name']
        sex = u['sex']
        try:
            country_id = u['country']['id']
        except KeyError:
            country_id = None
        try:
            birth_date = u['bdate']
        except KeyError:
            birth_date = None
        # print(friend, u['first_name'], u['last_name'])
        cur.execute('SELECT id FROM People WHERE vk_id = ? LIMIT 1',
                    (friend,))
        try:
            friend_id = cur.fetchone()[0]
            countold = countold + 1
        except TypeError:
            cur.execute('''INSERT OR IGNORE INTO People
            (vk_id, retrieved, first_name, last_name, sex, country_id, bdate)
            VALUES (?, 0, ?, ?, ?, ?, ?)''', (friend, first_name, last_name, sex, country_id, birth_date))
            conn.commit()
            if cur.rowcount != 1:
                print('Error inserting account:', friend)
                continue
            friend_id = cur.lastrowid
            countnew = countnew + 1
        cur.execute('''INSERT OR IGNORE INTO Follows (from_id, to_id)
                    VALUES (?, ?)''', (u_id, friend_id))
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()
cur.close()
