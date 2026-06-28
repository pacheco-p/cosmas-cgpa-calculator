import bcrypt
from database import conn,cursor

def signup(username,email,password):

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (
                username,
                email,
                hashed
            )
        )

        conn.commit()

        return True

    except:

        return False


def login(username,password):

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    data = cursor.fetchone()

    if data:

        if bcrypt.checkpw(
            password.encode(),
            data[0]
        ):

            return True

    return False
