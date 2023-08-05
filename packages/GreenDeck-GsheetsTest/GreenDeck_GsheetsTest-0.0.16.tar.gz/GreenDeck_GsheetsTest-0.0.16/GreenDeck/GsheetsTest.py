import matplotlib.pyplot as plt
import pandas as pd
from gsheets import Sheets


def login():
    sheets = Sheets.from_files('~/client_secret.json','~/storage.json')
    list_sheet(sheets)

def list_sheet(sheets):
    j=1
    all_sheets = sheets.findall()
    for i in all_sheets:
        print(str(j)+": "+str(i))
        j+=1
    choice = int(input("Enter the number whose sheets you want to access: "))
    if(choice<=j):
        plot_graph(all_sheets[choice-1])
    else:
        print("Invalid choice of sheets")
        quit()

def plot_graph(sheet):
    df = sheet.sheets[0].to_frame()
    counter = 1
    columns =df.columns
    for col in columns:
        print(str(counter)+": " + str(col))
        counter+=1
    choice_x = int(input("Enter choice of column for x-axis: "))
    if(choice_x>counter):
        print("Choice out of range")
        quit()
    choice_y = int(input("Enter choice of column for y-axis: "))
    if(choice_y>counter):
        print("Choice out of range")
        quit()

    df.plot(x=columns[choice_x-1],y=columns[choice_y-1],kind='line')
    plt.show()
login()