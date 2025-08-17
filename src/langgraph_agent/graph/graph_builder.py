from langgraph.graph import StateGraph, START, END
from src.langgraph_agent.state.state import State
from src.langgraph_agent.nodes.basic_nodes import chatbot_node
from src.langgraph_agent.tools.tools import get_tools, create_tool_node
from src.langgraph_agent.nodes.tool_node import ChatbotWithToolNode
from langgraph.prebuilt import tools_condition

class graph_builder():
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    # simple chatbot
    def basic_chatbot(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        llm = self.llm
        self.basic_chatbot = chatbot_node(model = llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    # chatbot with tools functionality
    def chatbot_with_tools(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        tools=get_tools()
        tool_node=create_tool_node(tools)

        ## Define the chatbot node
        obj_chatbot_with_node=ChatbotWithToolNode(self.llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)
        ## Add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        # Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")

    def setup_graph(self, usecase:str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot()
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools()
        return self.graph_builder.compile()