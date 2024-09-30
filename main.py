from langforge_os.graph import app

if __name__ == "__main__":

    while True:

        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        for chunk in app.stream(
            {"messages": [("human", user_input)]}, stream_mode="values"
        ):
            chunk["messages"][-1].pretty_print()
