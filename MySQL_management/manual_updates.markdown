these were put in manually to the mysql shell

# Change last two years of SEA drafts to OKC
```
SELECT Team.team, Team.team_id
FROM Team
WHERE Team.team = 'OKC';
```
team_id = 23 for OKC
change SEA draft in 2007 to OKC
the two players are Kevin Durant and Jeff Green
```
UPDATE Player
SET Player.team_id = 23
WHERE Player.name = 'Kevin Durant';
```
```
UPDATE Player
SET Player.team_id = 23
WHERE Player.name = 'Jeff Green';
```
change SEA draft in 2008 to OKC
```
UPDATE Player
SET Player.team_id = 23
WHERE Player.name = 'Trent Plaisted';
```
```
UPDATE Player
SET Player.team_id = 23
WHERE Player.name = 'DeVon Hardin';
```
```
UPDATE Player
SET Player.team_id = 23
WHERE Player.name = 'Sasha Kaun';
```

# Patrick O'Bryant was drafted by GSW not TOR
```
SELECT Team.team, Team.team_id
FROM Team
WHERE Team.team = 'GSW';
```
Warriors have team_id 33
```
UPDATE Player
SET Player.team_id = 33
WHERE Player.name = 'Patrick O''Bryant';
```
