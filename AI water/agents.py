from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY=os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.5-flash", temperature=0.5)

class WaterTrackerAgent:
    def __init__(self):
        self.history = []

    def analyze_water_intake(self,intake_ml):

        prompt = f"""You are a hydration assistant. A user has consumed {intake_ml} ml of water today. Provide feedback on their hydration status and suggest if they need to drink more water based on general health guidelines."""        
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
if __name__ == "__main__":
    agent = WaterTrackerAgent()
    print(agent.analyze_water_intake(1500)) 