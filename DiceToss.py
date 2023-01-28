"""
Name: Craig Brooks
PHSX 815 Spring 2023
HW # 3
Due Date 1/27/2023

This is the modified code for HW 3 in Computational Physics. This produces a multinomial distribution based on an unfair 6-sided die. The additions will be commented
below in the appropriate sections. the original code for the output is commented out


"""


#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# import our Random class from python/Random.py file
sys.path.append(".")
from Random import Random

# main function for our coin toss Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-seed number]" % sys.argv[0])
        print
        sys.exit(1)

    # default seed
    seed = 56878

    # default single coin-toss probability for "1"
    prob = [.05,.1,.05,.2, .1, .50]

    
    # default number of coin tosses (per experiment)
    Ntoss = 10000

    # default number of experiments
    #Nexp = 4

    # an array that stores the outcomes of the dice tosses
    outcomes = []
    
    # output file defaults
    doOutputFile = False

    # read the user-provided seed from the command line (if there)
    if '-seed' in sys.argv:
        p = sys.argv.index('-seed')
        seed = sys.argv[p+1]
    if '-prob' in sys.argv:
        p = sys.argv.index('-prob')
        ptemp = float(sys.argv[p+1])
        if ptemp >= 0 and ptemp <= 1:
            prob = ptemp
    if '-Ntoss' in sys.argv:
        p = sys.argv.index('-Ntoss')
        Nt = int(sys.argv[p+1])
        if Nt > 0:
            Ntoss = Nt
            
    #if '-Nexp' in sys.argv:
    #    p = sys.argv.index('-Nexp')
    #    Ne = int(sys.argv[p+1])
    #    if Ne > 0:
    #        Nexp = Ne
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        doOutputFile = True

    # class instance of our Random class using seed
    random = Random(seed)
    
    
   
  
    # simulates dice rolls by passing the number of rolls and the probability. Here, I set the number of rolls to 10000
    occurences = random.Category(Ntoss, prob)[0]
    for i in range(len(occurences)):
        outcomes += str(i+1)*occurences[i]
    # converts the strings to ints to plot in the histogram
    count_list = [int(i) for i in outcomes]
    # store the outcomes of n die roll simulations in a dictionary
    summary_dic = {'1':occurences[0], '2': occurences[1], '3':occurences[2], '4':occurences[4], '5':occurences[4], '6':occurences[5]}
    #store the count for each face occurance
    one, two, three, four, five, six = occurences[0], occurences[1], occurences[2], occurences[3],occurences[4], occurences[5]
    # counts the total rolls of the die
    count = sum(occurences)
    success_list = [one/count, two/count, three/count, four/count, five/count,six/count]
    
    # creates a table to store the count and success rate for each side
    df = pd.DataFrame(summary_dic.items(), columns = ['Side', 'Count'])
    df['Success Rate'] = success_list
    
    
    
   

    
    # prints the number of occurences for each side and their probabilities in a file if doOutputFile = True and prints a table when False

    if doOutputFile:
        outfile = open('rolls.txt', 'w')
        #for e in range(0,Nexp):
        outfile.write(str(occurences)+" ")
        outfile.write(str(success_list)+" ")
        
        outfile.close()
    else:
   
        print(df)
    
    # plots the historgram and Kernel density estimate of the die rolls
    
    
    fig, ax = plt.subplots()
    sns.histplot(data=count_list, bins=6, stat='count', color='b', discrete=True, ax=ax)
    ax2 = ax.twinx()
    sns.kdeplot(count_list, color = 'y', ax=ax2)
    plt.tight_layout()
    plt.show()
