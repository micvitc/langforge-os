import uuid
from langforge_os.utils import read_config, write_config

CONFIG_PATH = "config.yaml"


def get_model_name():
    config = read_config(CONFIG_PATH)
    model_name = config.get("model_name")
    if not model_name:
        model_name = input("Enter the model name: ")
        config["model_name"] = model_name
        write_config(config, CONFIG_PATH)
    return model_name


model_name = get_model_name()

if __name__ == "__main__":

    from langforge_os.graph import app

    thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_input = input("You: ")

        for event in app.stream(
            {"messages": [("human", user_input)]}, stream_mode="values", config=config
        ):
            event["messages"][-1].pretty_print()
