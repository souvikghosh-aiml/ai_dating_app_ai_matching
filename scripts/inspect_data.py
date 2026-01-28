from database.rds_client import RDSClient
import json

def inspect_relevant_data():
    db = RDSClient()

    tables_to_inspect = [
        #"users",
        #"user_preferences",
        #"hobbies",
        #"languages",
        #"life_styles",
        #"races",
        #"relationship_goals",
        "religions"
        #"users"
    ]
    
    print("=== RDS DATA PREVIEW ===")
    
    for table in tables_to_inspect:
        print(f"\n[ TABLE: {table} ]")

        query = f"SELECT * FROM `{table}`;"
        
        try:
            import pymysql
            conn = pymysql.connect(**db.config)
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if not rows:
                    print("  (Empty Table)")
                else:
                    for row in rows:
                        print(json.dumps(row, indent=2, default=str))
                        print("  " + "-"*15)
        except Exception as e:
            print(f"  Error fetching {table}: {e}")
        finally:
            if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    inspect_relevant_data()