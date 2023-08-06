# normplot: normal distribution plot

# -*- coding: utf-8 -*-
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
    
def normplot(x, *args):

    ''' 
    
    normplot: normal distribution plot
    [] = normplot(X, tag)
    
    INPUT
    X [n x 1] <numpy.ndarray>
        n samples
    tag [n x 1] <list>
        (optional input)
        tag for each datapoint (ie name)
    
    OUTPUT
    plot
        
    '''

    #Label points
    if len(args) != 0:
        point_labels = list(args[0])
    else:
        point_labels = list(range(0, max(x.shape))) 

    # Sort x but keep track of the order of the observations
    order = np.arange(0, len(x), 1)
    order = (order[np.newaxis]).T
    xorder = np.concatenate((x,order), axis=1)
    xorder = xorder[xorder[:,0].argsort()]
    x = xorder[:,0]
    order = xorder[:,1]
    o = []
    for i in range(len(order)):
        o.append(int(order[i]))
    
    point_labels = [point_labels[i] for i in o]


    x = np.squeeze(x)
    
    # Calculate quantiles and least-square-fit curve
    (quantiles, values), (slope, intercept, r) = stats.probplot(x, dist='norm')
    
    plt.figure()  
    plt.plot(values, quantiles,'ob')
        
     
    
    for i, label in enumerate(point_labels): 
        plt.text (values[i], quantiles[i], label, fontsize=15).set_color('black') 
    
    
     
    plt.plot(quantiles * slope + intercept, quantiles, 'r',linewidth=0.5)
    
    
    #define ticks
    ticks_perc=[1, 5, 10, 20, 50, 80, 90, 95, 99]
    
    #transfrom them from precentile to cumulative density
    ticks_quan=[stats.norm.ppf(i/100.) for i in ticks_perc]
    
    #assign new ticks
    plt.yticks(ticks_quan,ticks_perc)

    plt.xlabel('x',fontsize=20)
    plt.ylabel('probability',fontsize=20)

    #show plot
    plt.tight_layout()
    plt.show()
