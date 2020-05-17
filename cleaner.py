# done create a list of countries:
import json
import sqlite3
import ssl
import urllib.request

from hidden import token


def countries_url(vk_country_id, secret=token):
    return f'''https://api.vk.com/method/database.getCountriesById?country_ids={vk_country_id}\
&access_token={secret}&v=5.103'''


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

countries_list = list()
for i in range(1, 500):
    countries_list.append(i)
url = countries_url(','.join(map(str, countries_list)))

conn = sqlite3.connect('clean.sqlite')  # cleaned db for connection and true country analysis
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Countries ''')
cur.execute('''DROP TABLE IF EXISTS True_countries ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Countries
            (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS True_countries
            (id INTEGER PRIMARY KEY, tc INTEGER)''')

try:
    connection = urllib.request.urlopen(url, context=ctx)
except Exception as err:
    print('Failed to Retrieve', err)
    quit()

data = connection.read().decode()
try:
    js = json.loads(data)
except Exception as err:
    print('Unable to parse json', err)
    print(data)
    quit()

# print(js)
n = 0
for c in js['response']:
    cid = c['id']
    country_name = c['title']
    if country_name == '':
        continue
    # print(cid, country_name)
    n += 1
    cur.execute('''INSERT OR IGNORE INTO Countries
                    (id, name)
                    VALUES (?, ?)''', (cid, country_name))
conn.commit()
print(n, 'countries imported')

# done - write a function, that finds the most common friend's countries

conn_f = sqlite3.connect('friends.sqlite')  # cleaned db for connection and true country analysis
cur_f = conn_f.cursor()


def true_country(people_id):
    cur_f.execute('''SELECT country_id FROM People JOIN Follows On People.id = Follows.to_id
    WHERE Follows.from_id = ?
    and country_id NOTNULL
    GROUP BY country_id
    ORDER BY COUNT(*) DESC
    LIMIT 1;''', (people_id,))
    try:
        result = cur_f.fetchone()[0]
    except TypeError:
        result = None
    return result


cur_total = conn_f.cursor()
cur_total.execute('''SELECT id, vk_id, first_name, last_name, sex, country_id, bdate FROM People WHERE retrieved = 1''')

for retrieved in cur_total:
    person_id = retrieved[0]
    true_country_res = true_country(person_id)

    print(retrieved[2:4], true_country_res)
    cur.execute('''INSERT OR IGNORE INTO True_countries
                    (id, tc)
                    VALUES (?, ?)''', (person_id, true_country_res))

conn.commit()

cur.close()
cur_f.close()
cur_total.close()

# todo convert to a graph

# todo implement поиск в ширину
