from IPython.display import Image, display
import os
import yaml


def display_graph(graph):
    try:
        img = Image(graph.get_graph(xray=True).draw_mermaid_png())
        display(img)
        img_file_path = "graph.png"
        with open(img_file_path, "wb") as f:
            f.write(img.data)
    except Exception:
        pass


def read_config(CONFIG_PATH):
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as file:
            return yaml.safe_load(file)
    return {}


def write_config(config, CONFIG_PATH):
    with open(CONFIG_PATH, "w") as file:
        yaml.dump(config, file)


if __name__ == "__main__":
    pass
