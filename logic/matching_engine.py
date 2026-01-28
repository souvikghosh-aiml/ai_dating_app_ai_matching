import openai
import json
from database.rds_client import RDSClient
from config.settings import settings
from utils.logger import app_logger

class MatchingEngine:
    def __init__(self):
        self.db = RDSClient()
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())
        self.logger = app_logger

    def get_matches_for_user(self, user_id: int):
        self.logger.info(f"Initiating matching for user_id: {user_id} using {self.model_name}")
        target = self.db.get_unified_user_profiles_by_id(user_id)
        if not target:
            self.logger.warning(f"Match failed: User {user_id} not found in RDS.")
            return {"error": f"User {user_id} not found."}
        
        all_candidates = self.db.get_unified_user_profiles(limit=50)
        candidates = [c for c in all_candidates if c['id'] != user_id]

        self.logger.info(f"Sending {len(candidates)} candidates to GPT-4o for ranking.")
        prompt = f"""
        You are a professional matchmaker for the JOZI dating app. 
        Your goal is to find the most compatible partners for the 'Target User' from a list of 'Candidates'.

        TARGET USER PROFILE:
        {json.dumps(target, indent=2)}

        CANDIDATE LIST:
        {json.dumps(candidates, indent=2)}

        MATCHING CRITERIA:
        - Common hobbies and lifestyle interests.
        - Complementary relationship goals (e.g., Marriage matches with Long-term).
        - Shared language or religion (if specified).

        RETURN JSON FORMAT ONLY:
        {{
            "target_user_id": {user_id},
            "matches": [
                {{
                    "candidate_id": int,
                    "name": "string",
                    "score": int (0-100),
                    "match_reason": "2-3 sentences explaining why they are compatible"
                }}
            ]
        }}
        Rank the results by score descending. Return at most 5 matches.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a precise matchmaking engine that outputs only JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        self.logger.info("AI response successfully received and parsed.")
        return json.loads(response.choices[0].message.content)