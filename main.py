import uuid
from langforge_os.graph import app


if __name__ == "__main__":
    thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_input = input("You: ")

        for event in app.stream(
            {"messages": [("human", user_input)]}, stream_mode="values", config=config
        ):
            event["messages"][-1].pretty_print()
