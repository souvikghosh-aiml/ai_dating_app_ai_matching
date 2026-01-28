import random
import pymysql
from faker import Faker
from config.settings import settings

def seed_demo_data(count=15):
    faker = Faker()
    conn = pymysql.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD.get_secret_value(),
        database=settings.DB_NAME,
        port=settings.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

    HOBBY_IDS = [1, 2, 3, 4]  # Music, Food, Travel, Tech
    LANG_IDS = [1, 2, 3]      # English, Hindi, Arabic
    LS_IDS = [i for i in range(1, 97)] # Cats, Bird watching, Gardening, Environmental
    RELIGION_IDS = [1, 2, 3, 4, 5]
    GOAL_IDS = [1, 2, 3, 4, 5, 6, 7]

    try:
        with conn.cursor() as cursor:
            print(f"--- Seeding {count} Users with Full Relations ---")
            
            for _ in range(count):
                # 1. Insert User
                gender = random.choice(['male', 'female', 'non-binary'])
                user_sql = """
                    INSERT INTO users (name, email, gender, dob, description, location, status, password, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, 'active', 'hashed_pw', NOW())
                """
                cursor.execute(user_sql, (
                    faker.name(), faker.unique.email(), gender,
                    faker.date_of_birth(minimum_age=18, maximum_age=40),
                    faker.paragraph(nb_sentences=3), faker.city()
                ))
                user_id = cursor.lastrowid

                # 2. Insert User Preferences
                pref_sql = """
                    INSERT INTO user_preferences (user_id, religion, relationship_goals, start_age, end_age, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """
                cursor.execute(pref_sql, (
                    user_id, random.choice(RELIGION_IDS), random.choice(GOAL_IDS), 
                    random.randint(18, 25), random.randint(26, 45)
                ))

                # 3. Link Hobbies (Pivot Table)
                selected_hobbies = random.sample(HOBBY_IDS, k=random.randint(1, 3))
                for h_id in selected_hobbies:
                    cursor.execute("INSERT INTO user_hobbies (user_id, hobby_id) VALUES (%s, %s)", (user_id, h_id))

                # 4. Link Languages (Pivot Table)
                selected_langs = random.sample(LANG_IDS, k=random.randint(1, 2))
                for l_id in selected_langs:
                    cursor.execute("INSERT INTO user_languages (user_id, language_id) VALUES (%s, %s)", (user_id, l_id))

                # 5. Link Life Styles (Pivot Table)
                selected_ls = random.sample(LS_IDS, k=random.randint(1, 2))
                for ls_id in selected_ls:
                    cursor.execute("INSERT INTO user_life_styles (user_id, life_style_id) VALUES (%s, %s)", (user_id, ls_id))

            conn.commit()
            print(f"Done! {count} users and all their relations are now in RDS.")
            
    except Exception as e:
        conn.rollback()
        print(f"Error seeding data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_demo_data()