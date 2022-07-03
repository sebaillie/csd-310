import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "placeholder",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}\n".format(config["user"], config["host"], config["database"]))

    cursor = db.cursor()

    cursor.execute("SELECT team_id, team_name, mascot FROM team")

    teams = cursor.fetchall()

    print("-- DISPLAYING TEAM RECORDS --")
    for team in teams:
        print("Team ID: {}".format(team[0]))
        print("Team Name: {}".format(team[1]))
        print("Mascot: {}\n".format(team[2]))

    cursor.execute("SELECT player_id, first_name, last_name, team_id FROM player")

    players = cursor.fetchall()

    print("-- DISPLAYING PLAYER RECORDS --")
    for player in players:
        print("Player ID: {}".format(player[0]))
        print("Player First Name: {}".format(player[1]))
        print("Player Last Name: {}".format(player[2]))
        print("Team ID: {}\n".format(player[2]))
    
    input("\n\n Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist.")

    else:
        print(err)

finally:
    db.close()
