import DBcm

import platform

if "aws" in platform.uname().release:
    creds = {
        "user": "C00296036",
        "password": "wordgame4passwd",
        "host": "C00296036.mysql.pythonanywhere-services.com",
        "database": "C00296036$default",
    }
else:
    creds = {
        "user": "wordgame4user",
        "password": "wordgame4passwd",
        "host": "localhost",
        "database": "wordgame4DB",
    }

def add_to_database(t, w, s, m):
    SQL = """
        insert into leaderboard
          (time, who, sourceword, matches)
        values
            (%s, %s, %s, %s)
    """
    with DBcm.UseDatabase(creds) as db:
        db.execute(SQL, (t, w, s, m))

def get_leaderboard_data():
    SQL = f"""
        select ROW_NUMBER() OVER (order by time), l.*
        from leaderboard l
        order by time asc
        limit 10
    """
    with DBcm.UseDatabase(creds) as db:
        db.execute(SQL)
        res = db.fetchall()
    return res
