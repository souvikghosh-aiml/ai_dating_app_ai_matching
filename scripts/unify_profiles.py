from database.rds_client import RDSClient

def process_profiles():
    db = RDSClient()
    profiles = db.get_unified_user_profiles_by_id(3)
    
    if not profiles:
        print("No profiles found or unified.")
        return

    print(f"Successfully unified {len(profiles)} profiles.\n")

    for p in profiles:
        summary = (
            f"User {p['name']} is a {p['gender']} interested in {p['goal']}. "
            f"Hobbies: {p['hobby_list'] or 'None'}. "
            f"Lifestyle: {p['lifestyle_list'] or 'None'}. "
            f"Bio: {p['description'] or 'No bio provided.'}"
        )
        
        print(f"[User ID: {p['id']}]")
        print(f"NAME: {p['name']}")
        print(f"RAW SUMMARY FOR AI: {summary}")
        print("-"*40)

if __name__ == "__main__":
    process_profiles()