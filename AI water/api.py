from fastapi import FastAPI
from pydantic import BaseModel
from agents import WaterTrackerAgent
from database import log_water_intake, get_intake_history
from logger import log_info, log_error

app = FastAPI()
agent = WaterTrackerAgent()
class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int

@app.post("/log_intake")
async def log_intake(request: WaterIntakeRequest):
    try:
        log_water_intake(request.user_id, request.intake_ml)
        feedback = agent.analyze_water_intake(request.intake_ml)
        log_info(f"Logged {request.intake_ml} ml for user {request.user_id}")
        return {"status": "success", "feedback": feedback}
    except Exception as e:
        log_error(f"Error logging intake: {e}")
        return {"status": "error", "message": str(e)}
    
@app.get("/history/{user_id}")
async def history(user_id: str):
    try:
        records = get_intake_history(user_id)
        log_info(f"Fetched history for user {user_id}")
        return {"status": "success", "history": records}
    except Exception as e:
        log_error(f"Error fetching history: {e}")
        return {"status": "error", "message": str(e)}