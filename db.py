import os
import psycopg2

# Does what it says on the tin. Creates a db connection from the secret and returns a connection object
def connectToDatabase():
  conn = psycopg2.connect(os.environ['db_string'])
  return conn

# Takes an active database connection, player name, a new highscore, new lifetimescore and writes the new scores to the players db record
# Ideally we'd have a player class and just pass a player object to this function to be written
def updatePlayer(conn, playerId, highscore, lifetimescore):
  with conn.cursor() as cur:
    cur.execute("UPDATE players SET (highscore, lifetimescore)=(%(hs)s, %(ls)s) WHERE id=%(id)s;", {"id":playerId, "hs":highscore, "ls":lifetimescore})
  conn.commit()
  return

# Takes active db connection, a playerId, and a name then creates a new player record.
def insertPlayer(conn, playerId, playerName):
  with conn.cursor() as cur:
    cur.execute("INSERT INTO players (id, name, highscore, lifetimescore, currentscore) VALUES (%(id)s, %(name)s, 0, 0, 0);", {"id":playerId, "name":playerName})
  conn.commit()
  return

# Takes a db connection and playerId, returns true if they exist
def doesPlayerExist(conn, playerId):
  with conn.cursor() as cur:
    cur.execute("SELECT name FROM players WHERE id=%(id)s;", {"id":playerId})
    response = cur.fetchone()
  if (response):
    return True
  return False

def selectScore(conn, playerId):
  with conn.cursor() as cur:
    cur.execute("SELECT highscore, lifetimescore, currentscore FROM players WHERE id=%(id)s;", {"id":playerId})
    highscore, lifetimescore, currentscore = cur.fetchone()
  return highscore, lifetimescore, currentscore

def isPlayerInGame(conn, playerId):
  with conn.cursor() as cur:
    cur.execute("SELECT inGame FROM players WHERE id=%(id)s;", {"id":playerId})
    response = cur.fetchone()
  return response[0]

def updateScore(conn, playerId, score):
  with conn.cursor() as cur:
    if score == 0:
      cur.execute("UPDATE players SET currentscore = 0 WHERE id=%(id)s;", {"id":playerId})
    else:
      cur.execute("UPDATE players SET currentscore = currentscore + %(score)s WHERE id=%(id)s;", {"id":playerId, "score":score})
  conn.commit()
  return

def finishGame(conn, playerId):
  highscore, lifetimescore, currentscore = selectScore(conn, playerId)
  with conn.cursor() as cur:
    if currentscore > highscore:
      cur.execute("UPDATE players SET highscore = currentscore WHERE id=%(id)s;", {"id":playerId})
    cur.execute("UPDATE players SET lifetimescore = lifetimescore + currentscore WHERE id=%(id)s;", {"id":playerId})
    cur.execute("UPDATE players SET currentscore = 0 WHERE id=%(id)s;", {"id":playerId})
  conn.commit()
  return