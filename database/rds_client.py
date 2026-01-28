import pymysql
from config.settings import settings
import datetime

class RDSClient:
    def __init__(self):
        self.config = {
            "host": settings.DB_HOST,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD.get_secret_value(),
            "database": settings.DB_NAME,
            "port": settings.DB_PORT,
            "cursorclass": pymysql.cursors.DictCursor
        }

    def get_database_schema(self):
        query = """
            SELECT table_schema, table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = %s
        """
        try:
            conn = pymysql.connect(**self.config)
            with conn.cursor() as cursor:
                cursor.execute(query, (settings.DB_NAME,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error discovering MySQL schema: {e}")
            return []
        finally:
            if 'conn' in locals(): 
                conn.close()

    def get_unified_user_profiles(self, limit: int = 100):
        query = """
            SELECT 
                u.id, u.name, u.gender, u.dob, u.location, u.description,
                GROUP_CONCAT(DISTINCT h.name SEPARATOR ', ') as hobby_list,
                GROUP_CONCAT(DISTINCT l.name SEPARATOR ', ') as language_list,
                GROUP_CONCAT(DISTINCT ls.name SEPARATOR ', ') as lifestyle_list,
                rg.name as goal,
                rel.name as religion
            FROM users u
            LEFT JOIN user_hobbies uh ON u.id = uh.user_id
            LEFT JOIN hobbies h ON uh.hobby_id = h.id
            LEFT JOIN user_languages ul ON u.id = ul.user_id
            LEFT JOIN languages l ON ul.language_id = l.id
            LEFT JOIN user_life_styles uls ON u.id = uls.user_id
            LEFT JOIN life_styles ls ON uls.life_style_id = ls.id
            LEFT JOIN user_preferences up ON u.id = up.user_id
            LEFT JOIN relationship_goals rg ON up.relationship_goals = rg.id
            LEFT JOIN religions rel ON up.religion = rel.id
            GROUP BY u.id
            LIMIT %s;
        """
        conn = None
        try:
            conn = pymysql.connect(**self.config)
            with conn.cursor() as cursor:
                cursor.execute(query, (limit,))
                rows = cursor.fetchall()

                for row in rows:
                    for key, value in row.items():
                        if isinstance(value, (datetime.date, datetime.datetime)):
                            row[key] = value.isoformat()
                return rows
        except Exception as e:
            print(f"Error unifying data: {e}")
            return []
        finally:
            if conn: conn.close()

    def get_unified_user_profiles_by_id(self, user_id: int):
        query = """
            SELECT 
                u.id, u.name, u.gender, u.description,
                GROUP_CONCAT(DISTINCT h.name SEPARATOR ', ') as hobbies,
                GROUP_CONCAT(DISTINCT l.name SEPARATOR ', ') as languages,
                GROUP_CONCAT(DISTINCT ls.name SEPARATOR ', ') as lifestyle,
                rg.name as goal,
                rel.name as religion
            FROM users u
            LEFT JOIN user_hobbies uh ON u.id = uh.user_id
            LEFT JOIN hobbies h ON uh.hobby_id = h.id
            LEFT JOIN user_languages ul ON u.id = ul.user_id
            LEFT JOIN languages l ON ul.language_id = l.id
            LEFT JOIN user_life_styles uls ON u.id = uls.user_id
            LEFT JOIN life_styles ls ON uls.life_style_id = ls.id
            LEFT JOIN user_preferences up ON u.id = up.user_id
            LEFT JOIN relationship_goals rg ON up.relationship_goals = rg.id
            LEFT JOIN religions rel ON up.religion = rel.id
            WHERE u.id = %s
            GROUP BY u.id
        """
        conn = None
        try:
            conn = pymysql.connect(**self.config)
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching user {user_id}: {e}")
            return None
        finally:
            if conn: conn.close()

    def get_all_users(self, limit: int = 50):
        query = "SELECT id, name, email, gender, location, status FROM users LIMIT %s"
        try:
            conn = pymysql.connect(**self.config)
            with conn.cursor() as cursor:
                cursor.execute(query, (limit,))
                return self.sanitize_dates(cursor.fetchall())
        finally:
            conn.close()

    def get_user_by_id(self, user_id: int):
        query = "SELECT * FROM users WHERE id = %s"
        try:
            conn = pymysql.connect(**self.config)
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return self.sanitize_dates(cursor.fetchone())
        finally:
            conn.close()

    def create_user(self, user_data: dict):
        query = """
            INSERT INTO users (name, email, gender, description, location, status, password, created_at)
            VALUES (%(name)s, %(email)s, %(gender)s, %(description)s, %(location)s, 'active', 'encoded_pw', NOW())
        """
        try:
            conn = pymysql.connect(**self.config)
            with conn.cursor() as cursor:
                cursor.execute(query, user_data)
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    def sanitize_dates(self, data):
        if isinstance(data, list):
            return [self.sanitize_dates(item) for item in data]
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    data[key] = value.isoformat()
                elif isinstance(value, (dict, list)):
                    self.sanitize_dates(value)
            return data
            
        return data