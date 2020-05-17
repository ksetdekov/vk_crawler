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
                return person
            else:
                search_queue += graph[person]
                # Marks this person as searched
                searched.append(person)
    return False


end = search(1, 220)
print(end)


# def find_path(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return path
#     if start not in graph:
#         return None
#     for node in graph[start]:
#         if node not in path:
#             newpath = find_path(graph, node, end, path)
#             if newpath: return newpath
#     return None


# find_path(graph, 1, end)

def bfs_shortest_path(graph, start, goal):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        return "That was easy! Start = goal"

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)

    # in case there's no path between the 2 nodes
    return "So sorry, but a connecting path doesn't exist :("


print(len(bfs_shortest_path(graph, 1, end)) - 1)
