import tkinter as tk

def data_collection(iris_coordinate):
    CanvasWithBrush.paint(iris_coordinate)

class CanvasWithBrush(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("canvas")
        self.geometry("600x410")
        self.canvas = tk.Canvas(self, bg="white", cursor="pencil")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.brush_size = 5
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black")


if __name__ == "__main__":
    app = CanvasWithBrush()
    app.mainloop()
