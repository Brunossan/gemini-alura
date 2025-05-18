#loand img as bytes to sendo to agent
def load_png(path: str):
    with open(path, "rb") as f:
        png_bytes = f.read()
    return png_bytes