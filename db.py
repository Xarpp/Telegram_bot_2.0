import sqlite3


class BotDB:

    def __init__(self, db_file):
        """Initialization connect to database"""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def post_add_user(self, user_id, login):
        self.cursor.execute("INSERT INTO 'users' (user_id, login, logged) VALUES (?, ?, ?)", (user_id, login, 1))
        return self.conn.commit()

    def get_user_exists(self, user_id):
        """Check user in database by telegram id"""
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_login(self, user_id):
        """Return login from database by telegram id"""
        result = self.cursor.execute("SELECT 'login' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result

    def get_user_logged(self, user_id):
        """Check login in telegram bot"""
        result = self.cursor.execute("SELECT 'logged' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result

    def post_user_logout(self, user_id):
        """Logout user from telegram bot"""
        self.cursor.execute("UPDATE 'users' SET 'logged' = 0 WHERE 'user_id' = ?", (user_id,))
        return self.conn.commit()

    def get_user_last_login(self, user_id):
        """Check user last login in bot"""
        result = self.cursor.execute("SELECT 'last_login' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result

    def post_close(self):
        """Closing connection to database"""
        self.conn.close()
