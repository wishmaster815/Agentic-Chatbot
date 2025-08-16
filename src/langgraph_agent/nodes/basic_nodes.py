from src.langgraph_agent.state.state import State

class chatbot_node():
    def __init__(self, model):
        self.llm = model
    
    def process(self, state:State)->dict:
        return{
            "messages":self.llm.invoke(state["messages"])
        }