import streamlit as st
from src.langgraph_agent.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraph_agent.llms.groq_llm import groq_llm
from src.langgraph_agent.graph.graph_builder import graph_builder
from src.langgraph_agent.ui.streamlitui.display_ui import DisplayResultStreamlit
def load_langgraph_agentic_ai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.

    """
    ##Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe 
    else :
        user_message = st.chat_input("Enter your message:")

    # building the pipeline
    if user_message:
        try:
            # validate llm model
            obj_llm_model = groq_llm(user_controls_input=user_input)
            model = obj_llm_model.get_llm_model()
            if not model:
                st.error("Error, LLM model could not be initialised")
                return
            
            # initlaise and setup the graph along with usecases
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("no use case selected")
                return
            
            # graph buider
            builder =  graph_builder(model=model)
            try:
                graph=builder.setup_graph(usecase)
                
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed- {e}")
                return

        except Exception as e:
            raise ValueError(f"error:{e} ")