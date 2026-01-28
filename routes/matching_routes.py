from fastapi import APIRouter, HTTPException
from logic.matching_engine import MatchingEngine
from utils.logger import app_logger

router = APIRouter()
engine = MatchingEngine()

@router.get("/matches/{user_id}")
async def get_user_matches(user_id: int):
    try:
        app_logger.info(f"API Request: GET /matches/{user_id}")
        results = engine.get_matches_for_user(user_id)
        
        if "error" in results:
            raise HTTPException(status_code=404, detail=results["error"])
            
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))