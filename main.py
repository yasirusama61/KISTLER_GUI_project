# -*- coding: utf-8 -*-
"""
Author: Usama Yasir Khan
Project: KISTLER FAAM Machine GUI for Data Extraction


Description:
This project creates a GUI tool that allows users to extract relevant data from multiple CSV files generated by KISTLER FAAM machines.
Users can filter the data based on batch information, timestamps, and file contents. The extracted data is displayed in tables and visualized 
with graphs. The final output, including the graphs, is saved as an Excel file.

Modules used:
- pandas
- tkinter
- glob
- os
- datetime
- plotnine
- openpyxl
- random
- time

Instructions:
1. Launch the GUI by running this script.
2. Enter the machine details (FAAM_1 or FAAM_2) and select the data range (start and end time).
3. Choose whether to filter by OK, NOK, or both results, and select the random sampling option if desired.
4. Select the time interval for graph plotting (if not using random sampling).
5. Click 'Run' to start the extraction process. The results will be saved in an Excel file with graphs embedded.
"""

import pandas as pd
import datetime
import os, stat, time
from datetime import datetime
import glob
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import random
from plotnine import *
from mizani.breaks import date_breaks
import openpyxl

def get_csv(batchFolder, fResult, Rselection, fselection, sTime, eTime):
    csv_list = list()
    range_start = time.mktime(datetime.strptime(sTime, '%Y-%m-%d_%H').timetuple())
    range_end = time.mktime(datetime.strptime(eTime, '%Y-%m-%d_%H').timetuple())

    for path, dirs, files in os.walk(batchFolder):
        for dir in dirs:
            new_path = os.path.join(path, dir)
            foldername = os.path.basename(os.path.normpath(new_path))
            foldertime = time.mktime(datetime.strptime(foldername, '%Y-%m-%d_%H').timetuple())
            if foldertime >= range_start and foldertime <= range_end:
                targetFolder = os.path.join(batchFolder, new_path)
                # Random Selection is only available for OK or All filters
                if fResult == 1:
                    csv_files = glob.glob(os.path.join(targetFolder, "*_OK.csv"))
                    no_files = len(csv_files)
                    if Rselection == 1 and int(fselection) <= no_files:
                        csv_files = random.sample(csv_files, int(fselection))
                elif fResult == 2:
                    csv_files = glob.glob(os.path.join(targetFolder, "*_NOK.csv"))
                elif fResult == 3:
                    csv_files = glob.glob(os.path.join(targetFolder, "*.csv"))
                    no_files = len(csv_files)
                    if Rselection == 1 and int(fselection) <= no_files:
                        csv_files = random.sample(csv_files, int(fselection))
                csv_list.extend(csv_files)
    return csv_list

def get_Data(file, batchNo):
    df = pd.read_csv(file, header=None, sep=";")
    filename = df[0][1].split(',')[1]
    final_result = df[0][9].split(',')[1]
    Timestamp = df[0][6].split(',')[1] + " " + df[0][7].split(',')[1]
    Timestamp = datetime.strptime(Timestamp, '%Y/%m/%d %H:%M:%S')
    EO_01 = df[0][27].split(',')[1]
    EO_02 = df[0][28].split(',')[1]
    EO_03 = df[0][29].split(',')[1]
    EO_05 = df[0][31].split(',')[1]
    EO_07 = df[0][33].split(',')[1]
    Cal_01 = df[0][27].split(',')[12]
    Cal_02 = df[0][28].split(',')[12]
    Cal_07 = df[0][33].split(',')[12]

    newLine = [batchNo, filename, final_result, Timestamp, EO_01, EO_02, EO_03, EO_05, EO_07, Cal_01, Cal_02, Cal_07]
    return newLine

def Draw(df, TimeInterval, targetFolder):
    print('Entry the Draw')

    # Organize the Data
    df['Year'] = pd.DatetimeIndex(df.Timestamp).year
    df['Month'] = pd.DatetimeIndex(df.Timestamp).month
    df['Date'] = pd.DatetimeIndex(df.Timestamp).day
    df['Hour'] = pd.DatetimeIndex(df.Timestamp).hour
    df = df.set_index(['BatchNo', 'Filename', 'Final_Result', 'Timestamp', 'EO-01', 'EO-02', 'EO-03', 'EO-05', 'EO-07', 'Year', 'Month', 'Date', 'Hour']).stack().reset_index().rename({'level_13': 'Sensor', 0: 'SensorValue'}, axis=1)

    # Plot the graphs
    # Further plotting code goes here...

    print('Graphs created successfully!')

def createInterface():
    root = Tk()
    root.title("KISTLER Extract Files")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    Machine = IntVar()
    ttk.Label(mainframe, text="1. Machine").grid(column=1, row=1, sticky=W)
    ttk.Radiobutton(mainframe, text="FAAM_1", variable=Machine, value=1).grid(column=2, row=1, sticky=(W, E), padx=10, pady=10)
    ttk.Radiobutton(mainframe, text="FAAM_2", variable=Machine, value=2).grid(column=3, row=1, sticky=(W, E), padx=10, pady=10)

    so_no = StringVar()
    ttk.Label(mainframe, text="2. SO No (e.g. 111200079020)").grid(column=1, row=5, sticky=W)
    so_no = ttk.Entry(mainframe, width=10)
    so_no.grid(column=3, row=5, sticky=(W, E), padx=10, pady=10)

    # Other form elements...

    return root, mainframe, Machine, so_no

def main():
    # Main application logic
    root, mainframe, Machine, so_no = createInterface()
    ttk.Button(mainframe, text="Run", command=lambda: print("Run process")).grid(column=1, row=14, stick=E, padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
