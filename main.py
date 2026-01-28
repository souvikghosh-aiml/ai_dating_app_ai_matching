from fastapi import FastAPI
from routes.matching_routes import router as matching_router
from routes.user_routes import router as user_router
import uvicorn

app = FastAPI(
    title="JOZI AI Matching APP",
    description="API for AI-Dating App matching",
    version="1.0.0"
)

app.include_router(matching_router, prefix="/api/v1", tags=["Matching Engine"])
app.include_router(user_router, prefix="/api/v1", tags=["User Management"])

@app.get("/")
def health_check():
    return {"status": "online", "service": "JOZI-Matching-Engine"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)