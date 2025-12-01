#!/usr/bin/env python3

import sys
import argparse
import math
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


BASE_W = 1304
BASE_H = 780


class DoodleApp:
    def __init__(self, root, args):
        self.root = root
        self.args = args
        self.root.title("Screenshot Annotator")

        self.make_toolbar()

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

        self.image = None
        self.tk_image = None
        self.draw = None

        self.start_x = None
        self.start_y = None
        self.temp = None

        self.auto_number = 1

        self.line_width = 4
        self.font_size = 24
        self.font = None

        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        if args.file:
            self.load_image_from_path(args.file)

    def compute_scaling(self):
        """Compute line width & font size relative to image size, optionally using manual scale factor."""
        w, h = self.image.size

        if self.args.scale is not None:
            scale = self.args.scale
        else:
            scale = math.sqrt((w * h) / (BASE_W * BASE_H))

        self.line_width = max(int(4 * scale), 2)
        self.font_size = max(int(24 * scale), 14)

        self.font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            self.font_size
        )

    def make_toolbar(self):
        bar = tk.Frame(self.root)
        bar.pack(side="top", fill="x")

        tk.Button(bar, text="Open", command=self.open_image).pack(side="left")
        tk.Button(bar, text="Save", command=self.save_image).pack(side="left")

        if self.args.numbers:
            tk.Label(bar, text="Auto-numbering ON", fg="green").pack(side="right")

        if self.args.inplace and self.args.file:
            tk.Label(bar, text=f"In-place: {self.args.file}", fg="red").pack(side="right")

        if self.args.scale is not None:
            tk.Label(bar, text=f"Scale: {self.args.scale}", fg="blue").pack(side="right")

    def load_image_from_path(self, path):
        try:
            self.image = Image.open(path).convert("RGBA")
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        self.compute_scaling()
        self.draw = ImageDraw.Draw(self.image)
        self.update_canvas()

    def open_image(self):
        if self.args.inplace:
            print("Cannot open new file while using --inplace.")
            return

        path = filedialog.askopenfilename()
        if not path:
            return

        self.load_image_from_path(path)
        self.args.file = path

    def save_image(self):
        if not self.image:
            return

        if self.args.inplace and self.args.file:
            self.image.save(self.args.file)
            print(f"Saved inplace: {self.args.file}")
            return

        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.image.save(path)

    def on_press(self, event):
        if not self.image:
            return
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        if not self.image:
            return

        if self.temp:
            self.canvas.delete(self.temp)

        self.temp = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline="red", width=max(1, self.line_width - 1)
        )

    def on_release(self, event):
        if not self.image:
            return

        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y

        x0, x1 = sorted([x1, x2])
        y0, y1 = sorted([y1, y2])

        self.draw.rectangle((x0, y0, x1, y1), outline="red", width=self.line_width)

        if self.args.numbers:
            num = str(self.auto_number)
            self.auto_number += 1

            bbox = self.font.getbbox(num)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            text_x = x0 - (text_w + 10)
            text_y = y0

            self.draw.text((text_x, text_y), num, fill="red", font=self.font)

        if self.temp:
            self.canvas.delete(self.temp)
            self.temp = None

        self.update_canvas()

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)


def main():
    parser = argparse.ArgumentParser(description="Simple screenshot annotation tool.")
    parser.add_argument("file", nargs="?", help="Image file to open")
    parser.add_argument("--inplace", action="store_true",
                        help="Save changes back to the original file without prompting")
    parser.add_argument("--numbers", action="store_true",
                        help="Auto-label rectangles with auto-incrementing numbers")
    parser.add_argument("--scale", type=float, default=None,
                        help="Manual scaling factor for rectangle & font sizes (overrides automatic scaling)")
    args = parser.parse_args()

    root = tk.Tk()
    DoodleApp(root, args)
    root.mainloop()


if __name__ == "__main__":
    main()
