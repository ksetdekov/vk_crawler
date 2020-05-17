# SQL requests to friends.sqlite
* get all country id:
```
SELECT DISTINCT country_id FROM People ORDER by country_id

```
* list all frinds from a person:
```
SELECT * FROM People JOIN Follows On People.id = Follows.to_id WHERE Follows.from_id = 3339011 
```

# SQL requests to clean.sqlite
* table of countries:
```
SELECT name, steps FROM Countries JOIN Steps on Countries.id = Steps.id ORDER by steps
```