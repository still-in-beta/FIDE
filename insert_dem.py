import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd

insdem = tk.Tk()
insdem.title('Insert Demographics')
insdem.resizable(False, False)
insdem.geometry('300x150')

insCounty = tk.Tk()
insCounty.title('Insert County')
insCounty.resizable(False, False)
insCounty.geometry('300x150')

def select_file():
    filetypes = (
        ('excel files', '*.xlsx'),
        ('csv files', '*.csv')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

def type_county():
    

open_button = ttk.Button(
    insdem,
    text='Insert Demographics',
    command=select_file
)
input_county = ttk.Button(
    insCounty,
    text='Insert County',
    command=
)

open_button.pack(expand=True)

# run the application
insdem.mainloop()
