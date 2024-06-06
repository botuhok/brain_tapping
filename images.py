#  Этот модуль определяет разрешение экрана и подгоняет размер фотографий под него
#  Отсюда импортируются все фотки и размеры экрана в модуль main

import tkinter as tk
import os
import sys
from tkinter import ttk
from PIL import Image, ImageTk

res_dir = os.path.abspath('res')

# определяем размеры экрана
root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()


image = Image.open(os.path.join(res_dir, "1-1.png"))
img1_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "1-2.png"))
img1_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-1.png"))
img2_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-2.png"))
img2_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-3.png"))
img2_3 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-4.png"))
img2_4 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-5.png"))
img2_5 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-6.png"))
img2_6 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-7.png"))
img2_7 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "2-8.png"))
img2_8 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "3-1.png"))
img3_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "3-2.png"))
img3_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "4-1.png"))
img4_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "4-2.png"))
img4_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)


image = Image.open(os.path.join(res_dir, "5-1.png"))
img5_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "5-2.png"))
img5_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "6.png"))
img6 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "7.png"))
img7 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "9.png"))
img9 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "8.png"))
img8 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "10.png"))
img10 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "11.png"))
img11 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "12-1.png"))
img12_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "12-2.png"))
img12_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "17-1.png"))
img17_1 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)

image = Image.open(os.path.join(res_dir, "17-2.png"))
img17_2 = image.resize((WIDTH,HEIGHT), Image.Resampling.LANCZOS)






