import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog
from PIL import Image, ImageDraw
import os

class PixelPainter:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Painter")
        
        self.default_width = 735
        self.default_height = 662
        
        self.canvas_width = simpledialog.askinteger("Canvas Width", "Enter canvas width:", 
                                                   initialvalue=self.default_width, minvalue=50, maxvalue=2000) or self.default_width
        self.canvas_height = simpledialog.askinteger("Canvas Height", "Enter canvas height:", 
                                                    initialvalue=self.default_height, minvalue=50, maxvalue=2000) or self.default_height
        
        # defaults; black, 18px
        self.brush_size = 18
        self.color = "#000000"  
        
        self.canvas_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
        self.canvas_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, 
                              bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        self.control_frame = tk.Frame(root)
        self.control_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.create_controls()
        
        self.setup_bindings()
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        self.last_x, self.last_y = None, None
    
    def create_controls(self):
        #select color
        self.color_button = tk.Button(self.control_frame, text="Color", command=self.choose_color, 
                                     bg=self.color, width=8)
        self.color_button.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.control_frame, text="Brush Size:").pack(side=tk.LEFT, padx=5)
        
        #brush size
        self.brush_var = tk.StringVar(value=str(self.brush_size))
        self.brush_entry = tk.Entry(self.control_frame, textvariable=self.brush_var, width=5)
        self.brush_entry.pack(side=tk.LEFT, padx=5)
        self.brush_entry.bind("<Return>", self.update_brush_size)
        
        
        #clear
        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # save
        self.save_button = tk.Button(self.control_frame, text="Save PNG", command=self.save_image)
        self.save_button.pack(side=tk.RIGHT, padx=5)
    
    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_pixel)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)
    
    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.draw_pixel(event)  
    
    def draw_pixel(self, event):
        x, y = event.x, event.y
        x1 = x - self.brush_size // 2
        y1 = y - self.brush_size // 2
        x2 = x1 + self.brush_size
        y2 = y1 + self.brush_size
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline=self.color)
        
        self.draw.rectangle([x1, y1, x2, y2], fill=self.color, outline=self.color)
        
        self.last_x, self.last_y = x, y
    
    def reset_position(self, event):
        self.last_x, self.last_y = None, None
    
    def choose_color(self):
        color = colorchooser.askcolor(initial=self.color)[1]
        if color:
            self.color = color
            self.color_button.config(bg=self.color)
    
    def update_brush_size(self, event=None):
        try:
            new_size = int(self.brush_var.get())
            if new_size > 0:
                self.brush_size = new_size
        except ValueError:
            self.brush_var.set(str(self.brush_size))
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Image As"
        )
        if file_path:
            self.image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelPainter(root)
    root.mainloop()