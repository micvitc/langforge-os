from typing import Literal, Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import AnyMessage, add_messages
from langforge_os.tools import tools
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END
from langchain_openai import ChatOpenAI


from main import model_name, base_url, api_key

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful support assistant. "
            " Use the provided tools to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up.",
        ),
        ("placeholder", "{messages}"),
    ]
)


memory = MemorySaver()
tool_node = ToolNode(tools)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


try:
    model_with_tools = ChatOpenAI(
        model=model_name, base_url=base_url, api_key=api_key
    ).bind_tools(tools)
except Exception as e:
    print("Error loading model:", e)
    print("Please check the model name in the config file.")


def filter_messages(messages: list):
    return messages[-5:]


def ask_human(state: State):
    response = input("What do you think?: ")
    return {"messages": [("human", response)]}


def should_continue(state: State) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        messages[-1].pretty_print()
        user_input = input("Approve the tool call? (y/n): ")
        if user_input.lower() == "y":
            return "continue"
        else:
            return "ask_human"


runnable = assistant_prompt | model_with_tools.bind_tools(tools)


def call_model(state: State):
    messages = filter_messages(state["messages"])
    response = runnable.invoke({"messages": messages})
    return {"messages": [response]}


workflow = StateGraph(State)

workflow.add_node("assistant", call_model)
workflow.add_node("tools", tool_node)
workflow.add_node("ask_human", ask_human)
workflow.add_edge(START, "assistant")
workflow.add_conditional_edges(
    "assistant",
    should_continue,
    {
        "ask_human": "ask_human",
        "continue": "tools",
        "end": END,
    },
)
workflow.add_edge("ask_human", "assistant")
workflow.add_edge("tools", "assistant")

app = workflow.compile(checkpointer=memory)
