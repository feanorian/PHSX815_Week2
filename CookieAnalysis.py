"""
Name: Craig Brooks
PHSX 815 Spring 2023
HW # 4
Due Date 1/30/2023

This is the modified code for HW 4 in Computational Physics. This produces a an exponential distribution of the time between
succesive eaten cookies, calculates the 25th, 50th (median) and 75th percentiles and generates a table containing them, then plots 
the times and the averages times in a histogram. TheThe additions will be commented below in the appropriate sections. There is 
additional code that plots a box and whisker plot for the average of Nexp for each Nmeas measurement.


"""


#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# import our Random class from python/Random.py file
sys.path.append(".")
from MySort import MySort

# main function for our CookieAnalysis Python code
if __name__ == "__main__":
   
    haveInput = False

    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        InputFile = sys.argv[i]
        haveInput = True
    
    if '-h' in sys.argv or '--help' in sys.argv or not haveInput:
        print ("Usage: %s [options] [input file]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print
        sys.exit(1)
    
    Nmeas = 1
    times = []
    times_avg = []
    array = []
    
    need_rate = True
    
    with open(InputFile) as ifile:
        for line in ifile:
            if need_rate:
                need_rate = False
                rate = float(line)
                continue
            
            lineVals = line.split()
            Nmeas = len(lineVals)
            t_avg = 0
            for v in lineVals:
                t_avg += float(v)
                times.append(float(v))

            t_avg /= Nmeas
            times_avg.append(t_avg)

    Sorter = MySort()

    times = Sorter.DefaultSort(times)
    times_avg = Sorter.DefaultSort(times_avg)
    

    # try some other methods! see how long they take
    #times = Sorter.QuickSort(times)
    #times_avg = Sorter.BubbleSort(times_avg)
    #times_avg = Sorter.InsertionSort(times_avg)
    #times_avg = Sorter.QuickSort(times_avg)
    
    # ADD YOUR CODE TO PLOT times AND times_avg HERE

    # stores labels for quauntiles 
    percentile = ['25th', '50th', '75th']
    
    # creates a DataFrame that store the times and times_avg
    averages = pd.DataFrame({'Times': np.quantile(times, [.25, .50, .75]), 'Time Averages':np.quantile(times_avg, [.25, .50, .75]) })
    averages.rename(index = {0: percentile[0],1:percentile[1], 2:percentile[2]} ,inplace = True)
    averages.insert(0,'Percentile',percentile)
    #print(averages)
    

    # creates a table with the quartiles for times and times_avg
    fig0, ax0 = plt.subplots()
    ax0.axis('off')
    ax0.axis('tight')
    t = ax0.table(cellText=averages.values, colWidths = [0.5]*len(averages.columns),  colLabels=averages.columns,  loc='center')
    fig0.suptitle('IQR for Times and Time Avg')
    t.auto_set_font_size(False) 
    t.set_fontsize(8)
    fig0.tight_layout()
    
    
    # plots a histogram and KDE for all times
    fig, ax = plt.subplots()
    sns.histplot(data=times,stat='probability', color='g', ax=ax)
    ax = ax.twinx()
    sns.kdeplot(times, color = 'red', ax=ax)
    ax.set_title('Distribution of Times until Eaten Cookie')
    ax.set(xlabel='Time to Eaten Cookie (days)')
    plt.tight_layout()
    
    # plots a histogram and KDE for average times
    fig1, ax1 = plt.subplots()
    sns.histplot(data=times_avg,stat='probability' , color='blue', ax=ax1)
    ax1 = ax1.twinx()
    ax1.set_title('Distribution of Average Times until Eaten Cookie')
    ax1.set(xlabel='Time to Eaten Cookie (days)')
    sns.kdeplot(times_avg, color = 'magenta', ax=ax1)
    plt.tight_layout()
    
    # ***EXTRA*** plots a box and whisker plot for the medians of Nmeas measurements for Nexp experiments stored in the output file
    # We accomplish this by taking the mean across Nexp experiments for each measurement. We use a context manage to keep things tidy
    with open(InputFile, 'r') as my_file:
        x = my_file.readlines()

        def Convert(string):
            li = list(string.split(" "))
            return li

        for i in range(len(x)):
            array.append(Convert(x[i].strip()))
    
    
        f = pd.DataFrame(array)
        f.index = f.index + 1
        f.rename(columns={x:y for x,y in zip(f.columns,range(1,len(f.columns) + 1))})
    
        for key in f.keys():
            key = str(key)
        
        f = f.astype(float)
        f_melted = pd.melt(f)
    
        f_melted = f_melted.rename(columns={'variable': 'measurement', 'value': 'time (days)'})
        fig3, ax3 = plt.subplots()
    
        sns.boxplot(data=f_melted, x='measurement', y='time (days)')
        ax3.set_title(f'Median times to eaten cookie for {Nmeas} measurements averaged over {len(x) - 1} experiments')


    plt.show()


