import mysql.connector
from mysql.connector import errorcode

# MySQL connection with user information removed
cnx = mysql.connector.connect(user=user, password=password, host='localhost')

print('opened connection')

DB_NAME = 'nba_history_and_stats'

TABLES = {}
TABLES['Team'] = (
    "CREATE TABLE `Team` ("
    "  `team_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `team` VARCHAR(20),"
    "  PRIMARY KEY(`team_id`),"
    "  INDEX USING BTREE (team)"
    ") ENGINE=InnoDB")

TABLES['Year'] = (
    "CREATE TABLE `Year` ("
    "  `year_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `year` INTEGER,"
    "  PRIMARY KEY(`year_id`),"
    "  INDEX USING BTREE (year)"
    ") ENGINE=InnoDB")

TABLES['Round'] = (
    "CREATE TABLE `Round` ("
    "  `round_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `round` Integer,"
    "  PRIMARY KEY(`round_id`),"
    "  INDEX USING BTREE (round)"
    ") ENGINE=InnoDB")

TABLES['College'] = (
    "CREATE TABLE `College` ("
    "  `college_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `college` VARCHAR(100),"
    "  PRIMARY KEY(`college_id`),"
    "  INDEX USING BTREE (college)"
    ") ENGINE=InnoDB")

TABLES['Pick'] = (
    "CREATE TABLE `Pick` ("
    "  `pick_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `pick` INTEGER,"
    "  PRIMARY KEY(`pick_id`),"
    "  INDEX USING BTREE (pick)"
    ") ENGINE=InnoDB")

TABLES['Player'] = (
    "CREATE TABLE `Player` ("
    "  `player_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `name` VARCHAR(100),"
    "  `team_id` INTEGER,"
    "  `year_id` INTEGER,"
    "  `round_id` INTEGER,"
    "  `college_id` INTEGER,"
    "  `pick_id` INTEGER,"
    "  `years_played` INTEGER,"
    "  `games_played` INTEGER,"
    "  `minutes_played` INTEGER,"
    "  `points_total` INTEGER,"
    "  `rebounds_total` INTEGER,"
    "  `assists_total` INTEGER,"
    "  `field_goal_percent` FLOAT,"
    "  `three_point_percent` FLOAT,"
    "  `min_per_game` FLOAT,"
    "  `points_per_game` FLOAT,"
    "  `rebounds_per_game` FLOAT,"
    "  `assists_per_game` FLOAT,"
    "  `win_shares` FLOAT,"
    "  `win_shares_per_48` FLOAT,"
    "  `box_score_plus_minus` FLOAT,"
    "  `value_over_replacement` FLOAT,"
    "  PRIMARY KEY(`player_id`),"
    "  INDEX USING BTREE (name),"
    "  CONSTRAINT FOREIGN KEY (`team_id`) "
    "    REFERENCES `Team` (`team_id`)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (`year_id`) "
    "    REFERENCES `Year` (`year_id`)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (`round_id`) "
    "    REFERENCES `Round` (`round_id`)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (`college_id`) "
    "    REFERENCES `College` (`college_id`)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (`pick_id`) "
    "    REFERENCES `Pick` (`pick_id`)"
    "    ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

TABLES['Season'] = (
    "CREATE TABLE `Season` ("
    "  `season_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `season` VARCHAR(20),"
    "  PRIMARY KEY(`season_id`),"
    "  INDEX USING BTREE (season)"
    ") ENGINE=InnoDB")

TABLES['League'] = (
    "CREATE TABLE `League` ("
    "  `league_id` INTEGER NOT NULL AUTO_INCREMENT,"
    "  `league` VARCHAR(20),"
    "  PRIMARY KEY(`league_id`),"
    "  INDEX USING BTREE (league)"
    ") ENGINE=InnoDB")


TABLES['Per_Year_Stats'] = (
    "CREATE TABLE Per_Year_Stats ("
    "  per_year_stats_id INTEGER NOT NULL AUTO_INCREMENT,"
    "  player_id INTEGER,"
    "  season_id INTEGER,"
    "  team_id INTEGER,"
    "  league_id INTEGER,"
    "  age INTEGER,"
    "  games_played INTEGER,"
    "  games_started INTEGER,"
    "  minutes_per_game FLOAT,"
    "  field_goals_made_per_game FLOAT,"
    "  field_goals_attempted_per_game FLOAT,"
    "  field_goal_percent FLOAT,"
    "  three_pointers_made_per_game FLOAT,"
    "  three_pointers_attempted_per_game FLOAT,"
    "  three_point_percent FLOAT,"
    "  two_pointers_made_per_game FLOAT,"
    "  two_pointers_attempted_per_game FLOAT,"
    "  two_point_percent FLOAT,"
    "  effective_field_goal_percent FLOAT,"
    "  free_throws_made_per_game FLOAT,"
    "  free_throws_attempted_per_game FLOAT,"
    "  free_throw_percent FLOAT,"
    "  offensive_rebounds_per_game FLOAT,"
    "  defensive_rebounds_per_game FLOAT,"
    "  total_rebounds_per_game FLOAT,"
    "  assists_per_game FLOAT,"
    "  steals_per_game FLOAT,"
    "  blocks_per_game FLOAT,"
    "  turnovers_per_game FLOAT,"
    "  personal_fouls_per_game FLOAT,"
    "  points_per_game FLOAT,"
    "  PRIMARY KEY(per_year_stats_id),"
    "  CONSTRAINT FOREIGN KEY (player_id) "
    "    REFERENCES Player (player_id)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (season_id) "
    "    REFERENCES Season (season_id)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (team_id) "
    "    REFERENCES Team (team_id)"
    "    ON DELETE CASCADE ON UPDATE CASCADE,"
    "  CONSTRAINT FOREIGN KEY (league_id) "
    "    REFERENCES League (league_id)"
    "    ON DELETE CASCADE ON UPDATE CASCADE"
    ") ENGINE=InnoDB")

cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try: # try to change to the databse
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR: # if database does not exist
        create_database(cursor) # create database
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

print('creating tables in the database')

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# close cursor
cursor.close()
# close connection
cnx.close()
print('closed connection')
