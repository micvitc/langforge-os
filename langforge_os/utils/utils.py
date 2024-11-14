from IPython.display import Image, display
from ..graph import app


def display_graph(graph):
    try:
        img = Image(graph.get_graph(xray=True).draw_mermaid_png())
        display(img)
        img_file_path = "graph.png"
        with open(img_file_path, "wb") as f:
            f.write(img.data)
    except Exception:
        pass


if __name__ == "__main__":
    display_graph(app)
