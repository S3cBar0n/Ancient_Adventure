import os
import sqlite3

# Creates a new sqlite database if one doesn't already exist
def createDatabase():
    conn = sqlite3.connect('ancient_adventure.db')
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS players ([id] TEXT PRIMARY KEY, [name] TEXT, [highscore] INTEGER, [lifetimescore] INTEGER, [currentscore] INTEGER)")
    conn.close()

# Does what it says on the tin. Creates a db connection and returns a connection object
def connectToDatabase():
    conn = sqlite3.connect('ancient_adventure.db')
    return conn

# Takes active db connection, a playerId, and a name then creates a new player record.
def insertPlayer(conn, playerId, playerName):
    with conn:
        conn.execute("INSERT INTO players (id, name, highscore, lifetimescore, currentscore) VALUES (:id, :name, 0, 0, 0);", {"id":playerId, "name":playerName})

# Takes a db connection and playerId, returns true if they exist
def doesPlayerExist(conn, playerId):
    cur = conn.cursor()
    cur.execute("SELECT name FROM players WHERE id=:id;", {"id":playerId})
    response = cur.fetchone()
    if response:
            return True
    return False

# Takes a db connection and playerId, returns the players high score, lifetime score, and current score
def selectScore(conn, playerId):
    cur = conn.cursor()
    cur.execute("SELECT highscore, lifetimescore, currentscore FROM players WHERE id=:id;", {"id":playerId})
    highscore, lifetimescore, currentscore = cur.fetchone()
    return highscore, lifetimescore, currentscore

# Takes a db connection, playerId, and score. If the supplied score is 0, it sets the players current score to 0. Otherwise it adds the supplied integer to the players current score.
def updateScore(conn, playerId, score):
    with conn:
        if score == 0:
            conn.execute("UPDATE players SET currentscore = 0 WHERE id=:id;", {"id":playerId})
        else:
            conn.execute("UPDATE players SET currentscore = currentscore + :score  WHERE id=:id;", {"id":playerId, "score":score})

# Takes a db connection and playerId, updates the players lifetime score, high score (if applicable),  and sets current score back to zero
def finishGame(conn, playerId):
    highscore, lifetimescore, currentscore = selectScore(conn, playerId)
    with conn:
        if currentscore > highscore:
            conn.execute("UPDATE players SET highscore = currentscore WHERE id=:id;", {"id":playerId})
        conn.execute("UPDATE players SET lifetimescore = lifetimescore + currentscore WHERE id=:id;", {"id":playerId})
        conn.execute("UPDATE players SET currentscore = 0 WHERE id=:id;", {"id":playerId})
