from database.rds_client import RDSClient
from collections import defaultdict

def print_db_inventory():
    client = RDSClient()
    rows = client.get_database_schema()
    
    if not rows:
        print("No tables found or connection failed.")
        return
    
    #print(rows)

    inventory = defaultdict(list)
    for row in rows:
        schema = row.get('TABLE_SCHEMA')
        table = row.get('TABLE_NAME')
        column = row.get('COLUMN_NAME')
        dtype = row.get('DATA_TYPE')

        table_key = f"{schema}.{table}"
        inventory[table_key].append(f"{column} ({dtype})")

    print("RDS DATABASE INVENTORY")
    for table, columns in inventory.items():
        print(f"\nTABLE: {table}")
        for col in columns:
            print(f"{col}")
    print("\n")

if __name__ == "__main__":
    print_db_inventory()