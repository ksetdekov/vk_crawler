# SQL requests to friends.sqlite
* get all country id:
```
SELECT DISTINCT country_id FROM People ORDER by country_id

```
* list all frinds from a person:
```
SELECT * FROM People JOIN Follows On People.id = Follows.to_id WHERE Follows.from_id = 3339011 
```
