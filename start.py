
from re import sub
import tkinter as tk
from tkinter import filedialog as fd
from turtle import bgcolor
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageTk,Image

# county race data
county_race_url = 'https://api.census.gov/data/2020/dec/pl?get=NAME&for=county:*&P1_001N&P1_002N&P1_003N&P1_004N&P1_005N&P1_006N&P1_007N&P1_008N&P1_009N'
state_race_url = 'https://api.census.gov/data/2020/dec/pl?get=NAME&for=state:*&P1_001N&P1_002N&P1_003N&P1_004N&P1_005N&P1_006N&P1_007N&P1_008N&P1_009N'
us_race_url = 'https://api.census.gov/data/2020/dec/pl?get=NAME&for=us:*&P1_001N&P1_002N&P1_003N&P1_004N&P1_005N&P1_006N&P1_007N&P1_008N&P1_009N'

# input file
# filename = ''

# Stores data from api into dataframes
def store_api_data (url):
    response = requests.request("GET", url)
    return pd.DataFrame(response.json()[1:], columns=response.json()[0])

# insert_dem_btn function: opens a new window with information, and prompts you to open a file.
def demographics():
    win2 = tk.Toplevel()
    win2.title('Insert Demographics')
    info = tk.Label(win2, text="FIDE accepts CSV and Excel files. Columns for sex data should be titled \"Sex\" or \"Gender\" (not case sensitive).\n Accepted values are \"M\" or \"Male\", and \"F\" or \"Female\" (not case sensitive). For race data, please title columns\n as \"race\", and use accepted values: \"White\", \"Black\" or \"African-American\", \"Asian\", \"American Indian\" or \n \"Native American\" or \"Alaska Native\", \"Native Hawaiian\" or \"Pacific Islander\", and \"Multiracial\" or \n \"Two or more races\" (not case sensitive). Demographic data that does not fit any of these descriptions will be \n listed as \"Other\" for both sex and race.", anchor='nw', justify=tk.LEFT)
    
    info.grid(row=1, column=1)
    action_btn = tk.Button(win2, text="Upload", command=select_file)
    action_btn.grid(row=1, column=2)

# accept input for demographics
def select_file():
    global df_user_dem
    global filename
    filetypes = (
        ('Excel Microsoft Office Open XML Format Spreadsheet files', '*.xlsx'),
        ('Excel Spreadsheet (Excel 97-2003 workbook) files', '*.xls'),
        ('CSV files', '*.csv'),
        ('all files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    df_user_dem = read_usr_data()
    print(filename)


def select_loc():
    global us_state
    global us_county
    win3 = tk.Toplevel()
    win3.title('Input State and County')
    win3.geometry('100x100')
    clicked = tk.StringVar()
    
    statedrop = tk.OptionMenu(win3, clicked, 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana,', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming')
    statedrop.grid(row=1,column=1)


def read_usr_data():
    
    if(filename.endswith('.xlsx') or filename.endswith('.xls')):
        df_dem = pd.DataFrame(pd.read_excel(filename))
    else:
        df_dem = pd.DataFrame(pd.read_csv(filename))
    return df_dem

def graph(df):
    # graph_win = tk.Toplevel()
    # graph_win.title('Results')
    
    white = int(df.iat[0,3])
    black = int(df.iat[0,4])
    native = int(df.iat[0,5])
    asian = int(df.iat[0,6])
    pacific = int(df.iat[0,7])
    other = int(df.iat[0,8])
    multi = int(df.iat[0,9])
    
    labels = ['White', 'Black/African American', 'Native American', 'Asian', 'Pacific Islander', 'Other Races', '2+ Races']
    vals = np.array([white, black, native, asian, pacific, other, multi])
    percent = 100.*vals/vals.sum()
    fig = plt.figure(figsize=(2,2))
    ax1 = fig.add_axes([0, .25, .5, .5], aspect=1)
    ax1.set_xlim([0.5,4.5])
    ax1.set_ylim([0.5,100])
    patches, texts = ax1.pie(vals, radius = 2)
    if(place.get() == 'us'):
        ax1.set_title('Racial Demographic Breakdown of the United States of America',pad=50)
    elif(place.get() == 'state'):
        ax1.set_title('Racial Demographic Breakdown of ' + clicked_state.get(),pad=50)
    else:
        ax1.set_title('Racial Demographic Breakdown of ' + clicked_county.get() + ', ' + clicked_state.get(),pad=50)
    leg_labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, percent)]
    
    patches, leg_labels, dummy =  zip(*sorted(zip(patches, leg_labels, vals),
                                            key=lambda labels: labels[2],
                                            reverse=True))

    plt.legend(patches, leg_labels, loc='upper right', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
    ax2 = fig.add_axes([0.5, 0.25, 0.5, 0.5], aspect=1)
    white = int(df_user_dem.iat[0,1])
    black = int(df_user_dem.iat[0,2])
    native = int(df_user_dem.iat[0,3])
    asian = int(df_user_dem.iat[0,4])
    pacific = int(df_user_dem.iat[0,5])
    other = int(df_user_dem.iat[0,6])
    multi = int(df_user_dem.iat[0,7])
    vals = np.array([white, black, native, asian, pacific, other, multi])
    
    percent2 = 100.*vals/vals.sum()
    patches2, texts2 = ax2.pie(vals, radius = 2)
    ax2.set_title('Racial Demographic Breakdown of Your Institution',pad=50)
    leg_labels2 = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, percent2)]
    
    patches2, leg_labels2, dummy2 =  zip(*sorted(zip(patches2, leg_labels2, vals),
                                            key=lambda labels: labels[2],
                                            reverse=True))

    plt.legend(patches2, leg_labels2, loc='upper right', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

    # ax2.pie(vals, labels=labels, radius = 1.2)
    # ax2.set_title('Racial Demographic Breakdown of Your Institution')
    plt.tight_layout()
    plt.show()

    # if(subject == 'race'):
    #     if(place == 'us'):
    #         # ax.set_title('Racial Demographic Breakdown in the United States')
    #     elif(place == 'state'):
    #         # ax.set_title('Racial Demographic Breakdown in ' + clicked_state)
    #     else:
    #         # ax.set_title('Racial Demographic Breakdown in ' + clicked_county + ', ' + clicked_state)
    # plt.show()
# def read_census_data(state, county):

window = tk.Tk()
window.geometry("1600x900")
# Title and input data buttons
# title = tk.Label(text="FIDE", font=('Arial', 60))
img = ImageTk.PhotoImage(Image.open('fide_logo.jpeg'))
my_img = tk.Label(image=img)
my_img.grid(row=0,column=1)
the_text = tk.Label(window, text='   Bona FIDE diversity \n at a glance', font=('Segoe Script', 40)).grid(row=0, column=2)
# title.grid(row=0, column=1)

insert_dem_btn = tk.Button(text="Insert Demographics", font=('Times', 20), bg='#bdbdbd', command=demographics)
insert_dem_btn.grid(row=1, column=0, padx=10, pady=10)

# select_cty_btn = tk.Button(text = "Select County and State", font=('Arial', 20), bg='#5a5a5a', command=select_loc)
# select_cty_btn.grid(row=1, column=2, padx=10,pady=10)
clicked_state = tk.StringVar()
clicked_state.set('Select State')

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
statedrop = tk.OptionMenu(window, clicked_state, *states)
statedrop.grid(row=1,column=1)
# if(clicked_state.get() != 'Select State'):
clicked_county = tk.StringVar()
clicked_county.set('Select County')

counties = ['county1', 'county2', 'county3']
# countydrop = tk.OptionMenu(window, clicked_county, *counties)
countydrop = tk.Entry(window, width=60)

countydrop.insert(0, "Type Your County")
countydrop.grid(row=1, column=2)

place = tk.StringVar(value='us')
tk.Radiobutton(window, text="United States", variable=place, value='us', font=('Times', 15)).grid(row=3,column=0)
tk.Radiobutton(window, text="Your State", variable=place, value='state', font=('Times', 15)).grid(row=3, column=1)
tk.Radiobutton(window, text="Your County", variable=place, value='county', font=('Times', 15)).grid(row=3, column=2)

subject = tk.StringVar(value='race')
tk.Radiobutton(window, text='Race Data', variable=subject, value='race', font=('Times', 15)).grid(row=4, column=1)
tk.Radiobutton(window, text='Gender Data', variable=subject, value='gender', font=('Times', 15)).grid(row=4, column=2)
def lastly():
    clicked_county.set(countydrop.get())
    df_us_race_data = store_api_data(us_race_url)
    df_state_race_data = store_api_data(state_race_url)
    df_state_race_data = df_state_race_data.loc[df_state_race_data['NAME'] == clicked_state.get()]
    df_county_race_data = store_api_data(county_race_url)
    df_county_race_data = df_county_race_data.loc[df_county_race_data['NAME'] == clicked_county.get() + ', ' + clicked_state.get()]
    
    # winLast = tk.Toplevel()
    # winLast.title('Results')
    if(subject.get() == 'race'):
        if(place.get() == 'us'):
            graph(df_us_race_data)
        elif(place.get() == 'state'):
            graph(df_state_race_data)
        else:
            graph(df_county_race_data)


graph_btn = tk.Button(text='See Results',command=lastly, font=('Times', 20), bg='#869ef7').grid(row=5, column=2)

window.mainloop()
# def addr_null(address):
#     if(address is None):
#         return "Unknown"
#     else:
#         return address
# add_addr_b = tk.Button(text=("Change County (" + addr_null(vars_init.addr) + ")"), font=('Arial', 20), bg='#bcc3c4')
# add_addr_b.grid(row=2,column=0)

# def when_comp_dem_b_clicked():
#     os.system('python insert_dem.py')
# comp_dem_b = tk.Button(text='Update demographics', font=('Arial', 20), bg='#bcc3c4', command=when_comp_dem_b_clicked)
# comp_dem_b.grid(row=3,column=0, padx=10, pady=10)

# window.mainloop()