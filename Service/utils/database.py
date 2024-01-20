import psycopg2

from config_reader import config

# conn = psycopg2.connect(
#     host=config.host.get_secret_value(),
#     port=config.port.get_secret_value(),
#     database=config.database.get_secret_value(),
#     user=config.user.get_secret_value(),
#     password=config.password.get_secret_value(),
# )
conn = psycopg2.connect(config.external_uri.get_secret_value(), sslmode="require")
cur = conn.cursor()


def sql_start():
    """
    Connects to database. Create table of reviews if it does not exist.
    Table consist of user_id, score and feedback fields.
    user_id - unique telegram user_id, used as primary key.
    score - user score of our app, in [1, 2, 3, 4, 5].
    feedback - user feedback on our app, text field as limit is set to 1000 chars.
    """
    if conn:
        print("Connection to db...")
        print("Db is connected")
    else:
        print("Unable connect to db")

    # cur.execute("DROP TABLE reviews;")

    cur.execute(
        """CREATE TABLE IF NOT EXISTS reviews(
        user_id VARCHAR(255) PRIMARY KEY NOT NULL,
        score INT NOT NULL,
        feedback TEXT NOT NULL
        );
        """
    )

    conn.commit()


async def add_feedback_to_db(user_id: int, score: int, feedback: str):
    """Inserts user review to our database.

    :param user_id: unique telegram user_id
    :type user_id: str
    :param score: user score of our app
    :type score: int
    :param feedback: user textual feedback on our app
    :type feedback: str
    """
    insert_query = f"INSERT INTO reviews (user_id, score, feedback) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO NOTHING;"
    record_to_insert = (user_id, score, feedback)
    cur.execute(insert_query, record_to_insert)
    conn.commit()


async def read_feedback_from_db() -> str:
    """
    Queries obtained feedback from database.
    Also calculates average score.

    :rtype: str
    :return text: average and users' reviews
    """
    cur.execute("""SELECT AVG(score)::numeric(10,2)  FROM reviews;""")
    average = "Average score: " + str(cur.fetchone()[0]) + "\n\n"
    cur.execute("""SELECT user_id, score, feedback FROM reviews;""")
    query_results = cur.fetchall()
    text = "\n\n".join(
        [
            "user_id: {}\nscore: {}\nfeedback: {}\n".format(x[0], x[1], x[2])
            for x in query_results
        ]
    )
    return average + str(text)
