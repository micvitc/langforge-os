from typing import Literal

from langgraph.graph import StateGraph, MessagesState
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from langforge_os.tools import tools

memory = MemorySaver()
tool_node = ToolNode(tools)


model_with_tools = ChatOllama(
    model="llama3.1:8b-instruct-q4_0",
    temperature=0,
).bind_tools(tools)


def filter_messages(messages: list):
    return messages[-5:]


def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"


def call_model(state: MessagesState):
    messages = filter_messages(state["messages"])
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge("__start__", "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", "agent")

app = workflow.compile(checkpointer=memory)
