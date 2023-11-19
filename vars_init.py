from re import sub
import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageTk,Image

winit = tk.Tk()
img = ImageTk.PhotoImage(Image.open('fide_logo.jpeg'))
my_img = tk.Label(image=img)
my_img.grid(row=1,column=0)
the_text = tk.Label(winit, text='Bona FIDE diversity at a glance', ).grid(row=1, column=1)
winit.after(5000,lambda:winit.destroy())

winit.mainloop()