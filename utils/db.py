import sqlite3 as sq


def init():
    con = sq.connect("./db.sqlite3")
    cur = con.cursor()
    cur.execute(
            """
                CREATE TABLE IF NOT EXISTS
                    'users' (
                        'id' integer primary key AUTOINCREMENT,
                        'number' integer,
                        'name' varchar(100),
                        'surname' varchar(100),
                        'age' integer, 
                        'address' varchar(50),
                        'date' varchar(50),
                        'user_id' integer,
                        'username' varchar(100)
                    )
            """
        )
    con.close()


def get_user(user_id):
    con = sq.connect("./db.sqlite3")
    cur = con.cursor()
    user = cur.execute(
        f"""
            SELECT * FROM users WHERE user_id = {user_id}
        """
    ).fetchone()
    con.close()
    return user


def create_user(data):
    keys = tuple(data.keys())
    value = tuple(data.values())
    con = sq.connect("./db.sqlite3")
    cur = con.cursor()
    new_user = None
    try:
        new_user = cur.execute(
                f"""
                    INSERT INTO users{keys} VALUES{value}
                """
            )
        con.commit()
    except sq.Error as e:
        print(e)
    con.close()
    return new_user
