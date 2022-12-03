import psycopg2


class PostgresserHelper:
    def __init__(self, DB_URI):
        self.connection = psycopg2.connect(DB_URI, sslmode='require')
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
            result = self.cursor.fetchone()
            if not result:
                self.cursor.execute(f"INSERT INTO users (user_id, status) VALUES ({user_id} {True})")
                self.connection.commit()
                return 'success adding'
            else:
                return 'existed user'

    def remove_user(self, user_id):
        with self.connection:
            self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
                self.connection.commit()
                return 'success remove'
            else:
                return 'not existed user'

    def user_exist(self, user_id):
        with self.connection:
            self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
            result = self.cursor.fetchone()
            return bool(result)

    def return_users(self):
        with self.connection:
            self.cursor.execute("SELECT user_id FROM users")
            temp = self.cursor.fetchall()
            return [x for t in temp for x in t]

    def set_state(self, user_id, state):
        with self.connection:
            self.cursor.execute("UPDATE users SET state = %s WHERE user_id = %s", (state, user_id))
            self.connection.commit()


    def check_state(self, user_id):
        with self.connection:
            self.cursor.execute(f"SELECT state FROM users WHERE user_id = {user_id}")
            state = self.cursor.fetchone()
            return state
