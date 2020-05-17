import sqlite3
from collections import deque

conn = sqlite3.connect('clean.sqlite')  # cleaned db for connection and true country analysis
cur = conn.cursor()
person_cur = conn.cursor()


def person_is_seller(pers_id, country):
    person_cur.execute('''SELECT tc FROM True_countries WHERE id = ?''', (pers_id,))
    tc = person_cur.fetchone()[0]
    return tc == country


graph = dict()

cur.execute('''SELECT id FROM True_countries''')
for retrieved in cur:
    cur_id = retrieved[0]
    # print(cur_id)
    person_cur.execute('''SELECT to_id FROM Follows_short WHERE from_id = ?''', (cur_id,))
    all_friends = person_cur.fetchall()
    out = [item for t in all_friends for item in t]
    graph[cur_id] = out


def search(identifier, country_to_search):
    search_queue = deque()
    search_queue += graph[identifier]
    # This array is how you keep track of which people you've searched before.
    searched = []
    while search_queue:
        person = search_queue.popleft()
        # Only search this person if you haven't already searched them.
        if person not in searched:
            if person_is_seller(person, country_to_search):
                print(person, " is from country ", country_to_search)
                return True
            else:
                search_queue += graph[person]
                # Marks this person as searched
                searched.append(person)
    return False


search(1, 9)
