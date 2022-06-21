import sqlite3


class BotDB:

    def __init__(self, db_file):
        """Initialization connect to database"""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def post_add_user(self, user_id, login, logged=1):
        """Add new user to database"""
        self.cursor.execute("INSERT INTO 'users' (user_id, login, logged) "
                            "VALUES (?, ?, ?)", (user_id, login, logged))
        return self.conn.commit()

    def post_change_login(self, user_id, login):
        """Change login by telegram id"""
        self.cursor.execute("UPDATE 'users' SET login = ? WHERE user_id = ?", (login, user_id))
        return self.conn.commit()

    def get_user_exists(self, user_id):
        """Check user in database by telegram id"""
        result = self.cursor.execute("SELECT id FROM 'users' WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_login(self, user_id):
        """Return login from database by telegram id"""
        result = self.cursor.execute("SELECT login FROM 'users' WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def get_user_logged_status(self, user_id):
        """Return the user's authorization status"""
        result = self.cursor.execute("SELECT logged FROM 'users' WHERE user_id = ?", (user_id,))
        return bool(result.fetchone()[0])

    def post_user_logged_status(self, user_id, status):
        """Change the user's authorization status"""
        self.cursor.execute("UPDATE 'users' SET logged = ? WHERE user_id = ?", (status, user_id))
        return self.conn.commit()

    def get_user_last_login(self, user_id):
        """Check user last login in bot"""
        result = self.cursor.execute("SELECT last_login FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def post_user_last_login(self, last_login, user_id):
        """Change user last login in database"""
        self.cursor.execute("UPDATE 'users' SET last_login = ?, WHERE user_id = ?", (last_login, user_id))
        return self.conn.commit()

    def post_close(self):
        """Closing connection to database"""
        self.conn.close()
